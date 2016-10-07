#/usr/bin/env python3

import os.path

import asyncio
import aiohttp

from rhubarbe.logger import logger
from rhubarbe.config import Config
from rhubarbe.inventory import Inventory
from rhubarbe.frisbee import Frisbee
from rhubarbe.imagezip import ImageZip

class Node:

    """
    This class allows to talk to various parts of a node
    created from the cmc hostname for convenience
    the inventory lets us spot the other parts (control, essentially)
    """
    def __init__(self, cmc_name, message_bus):
        self.cmc_name = cmc_name
        self.message_bus = message_bus
        self.status = None
        self.action = None
        self.mac = None
        # for monitor
        self.id = int("".join([x for x in cmc_name if x in "0123456789"]))

    def __repr__(self):
        return "<Node {}>".format(self.control_hostname())

    def is_known(self):
        return self.control_mac_address() is not None

    def control_mac_address(self):
        the_inventory = Inventory()
        return the_inventory.attached_hostname_info(self.cmc_name, 'control', 'mac')

    def control_ip_address(self):
        the_inventory = Inventory()
        return the_inventory.attached_hostname_info(self.cmc_name, 'control', 'ip')

    def control_hostname(self):
        the_inventory = Inventory()
        return the_inventory.attached_hostname_info(self.cmc_name, 'control', 'hostname')

    async def get_status(self):
        """
        returns self.status
        either 'on' or 'off', or None if something wrong is going on
        """
        result = await self._get_cmc_verb('status')
        return result

    async def turn_on(self):
        """
        turn node on; expected result would be 'ok' if it goes fine
        """
        result = await self._get_cmc_verb('on')
        return result

    async def turn_off(self):
        """
        turn node on; expected result would be 'ok' if it goes fine
        """
        result = await self._get_cmc_verb('off')
        return result

    async def do_reset(self):
        """
        turn node on; expected result would be 'ok' if it goes fine
        """
        result = await self._get_cmc_verb('reset')
        return result

    async def get_info(self):
        """
        turn node on; expected result would be 'ok' if it goes fine
        """
        result = await self._get_cmc_verb('info', strip_result=False)
        return result

    async def get_usrpstatus(self):
        """
        returns self.usrpstatus
        either 'on' or 'off', or None if something wrong is going on
        """
        result = await self._get_cmc_verb('usrpstatus')
        return result

    async def turn_usrpon(self):
        """
        turn on node's USRP; expected result would be 'ok' if it goes fine
        """
        result = await self._get_cmc_verb('usrpon')
        return result

    async def turn_usrpoff(self):
        """
        turn off node's USRP; expected result would be 'ok' if it goes fine
        """
        result = await self._get_cmc_verb('usrpoff')
        return result

    async def _get_cmc_verb(self, verb, strip_result=True):
        """
        verb typically is 'status', 'on', 'off' or 'info'
        """
        url = "http://{}/{}".format(self.cmc_name, verb)
        try:
            client_response = await aiohttp.get(url)
        except Exception as e:
            setattr(self, verb, None)
            return None
        try:
            text = await client_response.text()
            if strip_result:
                text = text.strip()
            setattr(self, verb, text)
        except Exception as e:
            import traceback
            traceback.print_exc()
            setattr(self, verb, None)
        return getattr(self, verb)

    ####################
    # what status to expect after a message is sent
    expected_map = {
        'on' : 'on',
        'reset' : 'on',
        'off' : 'off'
    }
        
    async def send_action(self, message="on", check = False, check_delay=1.):
        """
        Actually send action message like 'on', 'off' or 'reset'
        if check is True, waits for check_delay seconds before checking again that
        the status is what is expected, i.e.
        | message  | expected |
        |----------|----------|
        | on,reset | on       |
        | off      | off      |

        return value stored in self.action
        * if check is false
          * True if request can be sent and returns 'ok', or None if something goes wrong
        * otherwise:
          * True to indicate that the node is correctly in 'on' mode after checking
          * False to indicate that the node is 'off' after checking
          * None if something goes wrong
        """
        url = "http://{}/{}".format(self.cmc_name, message)
        try:
            client_response = await aiohttp.get(url)
        except Exception as e:
            self.action = None
            return self

        try:
            text = await client_response.text()
            ok = text.strip() == 'ok'
        except Exception as e:
            self.action = None
            return self
    
        if not check:
            self.action = ok
            return self
        else:
            await asyncio.sleep(check_delay)
            await self.get_status()
            self.action = self.status == self.expected_map[message]
            return self

    ####################
    message_to_reset_map = { 'on' : 'reset', 'off' : 'on' }

    async def feedback(self, field, message):
        await self.message_bus.put(
            {'ip': self.control_ip_address(), field: message})

    async def ensure_reset(self):
        if self.status is None:
            await self.get_status()
        if self.status not in self.message_to_reset_map:
            await self.feedback('reboot',
                                     "Cannot get status at {}".format(self.cmc_name))
        message_to_send = self.message_to_reset_map[self.status]
        await self.feedback('reboot',
                                 "Sending message '{}' to CMC {}"
                                 .format(message_to_send, self.cmc_name))
        await self.send_action(message_to_send, check=True)
        if not self.action:
            await self.feedback('reboot',
                                     "Failed to send message {} to CMC {}"
                                     .format(message_to_send, self.cmc_name))


    ##########
    # used to be a coroutine but as we need this when dealing by KeybordInterrupt
    # it appears much safer to just keep this a traditional function
    def manage_nextboot_symlink(self, action):
        """
        Messes with the symlink in /tftpboot/pxelinux.cfg/
        Depending on 'action'
        * 'cleanup' or 'harddrive' : clear the symlink corresponding to this CMC
        * 'frisbee' : define a symlink so that next boot will run the frisbee image
        see rhubarbe.conf for configurable options
        """

        the_config = Config()
        root = the_config.value('pxelinux', 'config_dir')
        frisbee = the_config.value('pxelinux', 'frisbee_image')
        
        # of the form 01-00-03-1d-0e-03-53
        mylink = "01-" + self.control_mac_address().replace(':', '-')
        source = os.path.join(root, mylink)
        dest = os.path.join(root, frisbee)

        if action in ('cleanup', 'harddrive'):
            if os.path.exists(source):
                logger.info("Removing {}".format(source))
                os.remove(source)
        elif action in ('frisbee'):
            if os.path.exists(source):
                os.remove(source)
            logger.info("Creating {}".format(source))
            os.symlink(frisbee, source)
        else:
            logger.critical("manage_nextboot_symlink : unknown action {}".format(action))

    ##########
    async def wait_for_telnet(self, service):
        ip = self.control_ip_address()
        if service == 'frisbee':
            self.frisbee = Frisbee(ip, self.message_bus)
            await self.frisbee.wait()
        elif service == 'imagezip':
            self.imagezip = ImageZip(ip, self.message_bus)
            await self.imagezip.wait()
            pass
        
    async def reboot_on_frisbee(self, idle):
        self.manage_nextboot_symlink('frisbee')
        await self.ensure_reset()
        await self.feedback('reboot',
                                 "idling for {}s".format(idle))
        await asyncio.sleep(idle)

    async def run_frisbee(self, ip , port, reset):
        await self.wait_for_telnet('frisbee')
        self.manage_nextboot_symlink('cleanup')
        result = await self.frisbee.run(ip, port)
        if reset:
            await self.ensure_reset()
        else:
            await self.feedback('reboot',
                                'skipping final reset')
        return result

    async def run_imagezip(self, port, reset, radical, comment):
        await self.wait_for_telnet('imagezip')
        self.manage_nextboot_symlink('cleanup')
        result = await self.imagezip.run(port, self.control_hostname(), radical, comment)
        if reset:
            await self.ensure_reset()
        else:
            await self.feedback('reboot',
                                'skipping final reset')
        return result
