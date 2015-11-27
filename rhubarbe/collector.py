import asyncio

from logger import logger

class Collector:
    def __init__(self, image, message_bus):
        self.image = image
        self.message_bus = message_bus
        #
        self.subprocess = None
    
    @asyncio.coroutine
    def feedback(self, field, msg):
        yield from self.message_bus.put({field: msg})

    def feedback_nowait(self, field, msg):
        self.message_bus.put_nowait({field: msg})

    @asyncio.coroutine
    def start(self):
        """
        Start a collector instance; returns a port_number
        """
        from config import the_config
        netcat = the_config.value('frisbee', 'netcat')
        local_ip = the_config.local_control_ip()
        # should use default.ndz if not provided
        # use shell-style as we rather have bash handle the redirection
        # we instruct bash to exec nc; otherwise when cleaning up we just kill the bash process
        # but nc is left lingering behind
        # WARNING: it is intended that format contains {port} for future formatting
        command_format = "exec {} -d -l {} {{port}} > {} 2> /dev/null"\
                        .format(netcat, local_ip, self.image)

        nb_attempts = int(the_config.value('networking', 'pattern_size'))
        pat_port = the_config.value('networking', 'pattern_port')
        for i in range(1, nb_attempts+1):
            pat = str(i)
            port = str(eval(pat_port.replace('*', pat)))
            command = command_format.format(port=port)
            self.subprocess = \
              yield from asyncio.create_subprocess_shell(command)
            yield from asyncio.sleep(1)
            # after such a short time, frisbeed should not have returned yet
            # if is has, we try our luck on another couple (ip, port)
            command_line = command
            if self.subprocess.returncode is None:
                logger.info("collector started: {}".format(command_line))
                yield from self.feedback('info', "image collector server started")
                self.port = port
                return port
            else:
                logger.warning("failed to start collector with {}".format(command_line))
        logger.critical("Could not find a free port to start collector")
        raise Exception("Could not start collector server")

    @asyncio.coroutine
    def stop(self):
        self.stop_nowait()
        
    def stop_nowait(self):
        # make it idempotent
        if self.subprocess:
            # when everything is running fine, nc will exit on its own
            try:
                self.subprocess.kill()
            except:
                pass
            self.subprocess = None
            logger.info("collector (on port {}) stopped".format(self.port))
            self.feedback_nowait('info', "image collector server (on port {}) stopped".format(self.port))
