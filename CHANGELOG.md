# 5.1.6 - 2023 Jan 9

* a bug in accountsmanager was preventing any change (in accounts or keys)
  from being propagated in /etc/passwd or .ssh/authorized_keys


# 5.1.5 - 2022 Dec 12

* remove residual bug in `pdu`, when turning off a port
  the retcod is -1 when success (go figure..)

# 5.1.4 - 2022 Dec 11

* update list of commands available as e.g. rhubarbe-script

# 5.1.3 - 2022 Dec 10

* all 4 `pdu-list`, `pdu-status`, `pdu-on` and `pdu-off`
  commands are available through `rhubarbe script`
# 5.1.2 is broken (scripts are not packaged)

# 5.1.1 - 2022 Dec 9

* fixed the `pdu-list` command for fedora 37 for now
  the other 3 will follow shortly, and will be merge into
  the single pdu command

# 5.1.0 - 2022 Dec 9

* rhubarbe script command arg .. args
  allows to invoke one of the commands in rhubarbe/scripts
  and these can be configured in the [script] section of rhubarbe.conf

# 5.0.3 - 2022 Dec 2

* for python-3.11 (fedora37)
  requires telnetlib3-2.0.0
  tweak was needed in telnet.py to remove the log paramater
  to the call to telnetlib3.open_connection

# 5.0.2 - 2022 Mar 10

* adapt to a change in the return type of
  websockets.uri.parse_uri that is no longer a unpackable
  was affecting monitorphones mostly

# 5.0.1 - 2022 Mar 9

* after upgrading the testbed to f35 / monterey
  the adb binary for the phones is now expected to be
  brew-installed and thus in /usr/local/bin

# 5.0.0 - 2021 Nov 6

* for r2dock-empowered nodes
  monitornodes reports 3 more fields for nodes that are ssh-reachable
  docker_version, container_running, and container_image

# 4.0.9 - 2021 Jul 5

* bugfix, better handling of unreadable images

# 4.0.8 - 2021 May 31

* default ssh_timeout is now 2s; nodes sometimes need more time
  to answer about their versions and all the material requested
  by the monitor

# 4.0.7 - 2020 Nov 13

* no longer specify a protocol when creating a SSLContext
  object for connecting to a plcapi endpoint, useful when
  plcapi runs on f33/python3.9


# 4.0.6 - 2020 Nov 7

* remove asyncssh INFO messages in rhubarbe wait

# 4.0.5 - 2020 Jun 25

* bugfix in monitor nodes, monitor was hanging on nodes
  that got killed at the wrong time

# 4.0.4 - 2020 Jun 15

* fixed missing f-string
* use Makefile.pypi to publish on pypi

# 4.0.3 - 2019 Nov 22

* fix an alien bug with Path.glob() that does not behave as expected
  replaced with glob.glob()
* PS: a bug was filed in the Python repo here https://bugs.python.org/issue38894 

# 4.0.2 - 2019 Nov 21

* Monitor knows how to spot and report nodes running centos

# 4.0.1 - 2019 Jun 11

* micro fix for nightly.py: Frisbeed to accept ImagePath image

# 4.0.0 - 2019 Jun 1

* move to using telnetlib3 v1.x
* refactored telnet code so as to capture cases  when imagezip
  or frisbee fail to run on the node as part of load/save operations

# 3.1.6 - 2019 Mar 28

* fix for when an actual filename is provided to either load or resolve

# 3.1.5 - 2019 Mar 21

* rhubarbe share works on a plain filename too
* intermediate versions were all broken

# 3.1.1 - 2019 Mar 20

* rewrote the images repository, i.e. images, resolve and share subcommands
* default for images is now to list all images (not only the labeled ones, use -l for that)
* also default is to display the full path (use -n/--narrow to cut that off)
* 3.1.0 broken

# 3.0.6 - 2019 Feb 14

* default is to use fedora style for netcat

# 3.0.5 - 2019 Jan 29

* report to websockets-backed sidecar service, drop socket-io
* earler 3.0.x all more or less broken

# 2.1.1 - 2019 Jan 16

* a few more bugfixes, including more sensible log scheme

# 2.1.0 - 2019 Jan 16

* monitor becomes monitornodes
* slowly becoming more friendly to nightly script

# 2.0.3 - 2019 Jan 15

* the various main() functions that create a Scheduler object
  were written at a time where the default was critical=False
  restore this default behaviour here; some of these tools are
  used in the nightly check done on R2lab

# 2.0.2 - 2018 Nov 26

* flush a couple ops-oriented changes
  * make sure accountsmanager is always running even in case of temporary glitch
  * 'make infra' to also restart monitorphones
  * clean up of setup.py

# 2.0.1 - 2018 May 21

* bugfix in accountsmanager:
  * consider only login entries that have a valid homedir
  * protect replace_file_with_string against non-existing dir

# 2.0.0 - 2018 May 21

* new access policy; we now have three of them which are
  * `open`: all slices can enter at any time
  * `leased` : only the slice that currently has the lease can enter
    (formerly known as `closed`)
  * `closed` : no slice can enter at any time
* use setuptools instead of distutils for setup.py
* no more runner script bin/rhubarbe, see rhubarbe/__main__.py instead
* `/etc/rhubarbe/rhubarbe.conf` no longer used, ships as a resource (under config/)
* new subcommand template to expose the json templates
  instead of storing them in `/etc/rhubarbe`


# 1.8.1 - 2018 May 18

* emergency fix for a few lingering calls to orchestrate(timeout=timeout)
* configurable access policy; only 'open' and 'closed' supported for now
* for preplabs: configurable list of accounts that do not need a lease;
  this extends the previously hard-wired 'root' account, and by default
  it comes with 'root' and 'guest'
* thoroughly made pylint-friendly

# 1.7.3 - 2017 Nov 8

* another bugfix; rhubarbe leases --check displayed current login name as None

# 1.7.2 - 2017 Nov 8

* bugfixes

# 1.7.1 - 2017 Nov 8

* more tweaks in the leases area for r2lab's nightly

# 1.7.0 - 2017 Nov 3

* new feature rhubarbe bye (formerly known as all-off)
* new class Action that can send a CMC verb to a selector of nodes
* slight tweaks in lease management to allow r2lab to write a new nightly

# 1.6.0 - 2017 Oct 9

* bugfix for collecting images on a fedora box

# 1.5.4 - 2017 May 23

* we require telnetlib3 in version 0.5.0 at this point, as 1.0 breaks our code

# 1.5.3 - 2017 May 23

* bugfix: mainloop would crash if duration > period
  which happens e.g. upon network failures

# 1.5.2 - 2017 Mar 27

* 2 more fixes for that move to aiohttp 2.x
  that was obviously too hasty

# 1.5.1 - 2017 Mar 27

* fixed the adaptation to aiohttp 2.x that was too rough
  * http response needed to be stripped
  * and encoding is not returned by the CMC card in http header

# 1.5.0 - 2017 Mar 26

* for running against aiohttp 2.x

# 1.4.5 - 2017 Mar 26

* bugfix in monitor that was leaking ssh connections and thus
  was ending up showing all nodes in green instead of ON
* slightly longer monitor timeouts
* preplab runs on etourdi

# 1.4.4 - 2017 Mar 9

* targets the new preplab box (etourdi) that runs f25
* added installation notes for fedora
* tweaks for running on fedora; see netcat_style in config
* also checks for the presence of required binaries frisbeed and netcat

# 1.4.3 - 2017 Jan 19

* bugfix for connecting to sidecar over https

# 1.4.2 - 2017 Jan 19

* merged monitorphones capability from r2lab/
* rhubarbe.conf
  * new config category [sidecar]
  * + various renamingsfor consistency
* inventory config files are now
  * inventory_path = /etc/rhubarbe/inventory-nodes.json
  * inventory_phones_path = /etc/rhubarbe/inventory-phones.json
* 1.4.0 has a broken setup
* 1.4.1 was broken too; commands like status would hang

# 1.3.7 - 2017 Jan 18

* set sidecar url in monitor.service
* garbage obsolete monitor.sh

# 1.3.6 - 2017 Jan 18

* monitor config : sidecar_url replaces sidecar_hostname and sidecar_port
* default is now on port 999

# 1.3.5 - 2017 Jan 10

* protect accountsmanager against a plcapi being down

# 1.3.4 - 2017 Jan 4

* rhubarbe accounts -c 0 means to run it only once
* minor bugfix in rhubarbe share with no alias

# 1.3.3 - 2016 Dec 20

* cleanup wrt omf-related code
* updated readme

# 1.3.2 - 2016 Dec 19

* new function 'monitor-accounts' that can run as a service
  that keeps the set of unix accounts in sync with the plcapi
* default config is to use plcapi
* 1.3.[01] are broken

# 1.2.3 - 2016 Dec 17

* fix MonitorLeases that still exposes leases in
  a way similar to what we had with omf

# 1.2.2 - 2016 Dec 16

* rhubarbe accounts manages accounts from plcapi
* still rustic : runs one shot at a time

# 1.2.1 - 2016 Dec 15

* create PlcApiProxy from a url instead of a hostname and port
* for r2lab.inria.fr that uses this class

# 1.2.0 - 2016 Dec 14

* has support for getting leases at a plcapi instance
* although for now it will run on r2lab in omf mode

# 1.1.1 - 2016 Nov 21

* rhubarbe leases —check is verbose

# 1.1.0 - 2016 Nov 21

* use asynciojobs 0.4.0, with engine renamed into scheduler


# 1.0.5 - 2016 Nov 14

* rhubarbe images -v shows all images
* rhubarbe images show only images that have a symlink

# 1.0.4 - 2016 Nov 14

* rshare now has a -a/--alias option
* remove option -v for rimages
* remove option -d for rshare
* bugfix for rimages in case of a dangling symlink

# 1.0.3 - 2016 Nov 5

* bugfix to make selection like -a ~1 work as expected

# 1.0.2 - 2016 Nov 2

* big bugfix in monitor

# 1.0.1 - 2016 Nov 2

* monitor shows # of emitted messages

# 1.0.0 - 2016 Oct 26

* use new channel names like 'info:nodes' or 'request:nodes'
* expose more details on nodes, like
  * usrp_on_off
  * gnuradio_release (used to be in os_release)
  * uname

# 0.9.27 - 2016 Oct 25

* bugfix in collecting `image_radical` that used
  to be trimmed at dots or other characters

# 0.9.26 - 2016 Oct 10

* rhubarbe share --clean
* rhubarbe images -e -> rhubarbe resolve
* refactoring in the imagesrepo area
* 0.9.24 and 0.9.25 are broken

# 0.9.23 - 2016 Oct 7

* more robust exit code, esp. regarding missing leases
* nicer error message in case of misformed range
* 0.9.22 is broken

# 0.9.21 - 2016 Oct 4

* nicer way to display multiple matches

# 0.9.20 - 2016 Sep 30

* imagefile=$(rhubarbe images -e name) allows to resolve a name
  (as if passed to load -i)
* in case of several matches **the most recent** is used
* don't use 0.9.19

# 0.9.18 - 2016 Sep 29

* stdout and stderr use line buffering
* hopefully when running through ssh this will make a noticable change

# 0.9.17 - 2016 Sep 29

* share -f to force overwriting an already existing image

# 0.9.16 - 2016 Sep 24

* rework of rhubarbe wait
* rework of rhubarbe on/off/reset/status/info/usrp*
* both are now more efficient
* both now use an asynciojobs engine
* don't use 0.9.14 - load was broken
* ran into trouble when uploading 0.9.15 onto pypi

# 0.9.13 - 2016 Sep 23

* revisited `rhubarbe wait` to make it use a 1s timeout when trying to ssh connect
* in the mix, rwait now works with --curses, and has a new --silent
* wait uses asyniojobs to nicely handle the endless display task

# 0.9.12 - 2016 Sep 5

* use exclusively python-3.5 asyncio syntax
* i.e. no more `yield from` nor `@asyncio.coroutine`

# 0.9.11 - 2016 June 10

* fix image name as parsed by monitor
* more robust omfsfaproxy

# 0.9.10 - 2016 June 1

* rename JSON field 'imagename' into 'image_radical' for naming consistency
  before this propagates too far

# 0.9.9 - 2016 May 31

* monitor to probe for /etc/rhubarbe-image an to expose last found name in
  the new 'imagename' field of its JSON output

# 0.9.8 - 2016 May 30

* images named in saving* can be referred to as their mere radical
* rsave accepts a --comment option for making /etc/rhubarbe-image
  more helpful

# 0.9.7 - 2016 May 19

* rhubarbe save now adds a line to /etc/rhubarbe-image that
  gives details on date, node, image name and unix account
* rhubarbe share now available. Permissions to use needs to
  be granted on an unix account basis in sudoers.
  On faraday this is done in `/etc/sudoers.d/rhubarbe-share`

# 0.9.6 - 2016 May 17

* bugfix for when saving an image triggers the global timeout
* ship experimental feature share
* forgetting -i in e.g. rload 12 ubuntu results in early failure

# 0.9.5 - 2016 May 11

* long overdue: on, off, reset, usrpon and usrpoff also require a reservation

# 0.9.4 - 2016 May 9

* support for usrpon, usrpoff and usrpstatus

# 0.9.3 - 2016 Apr 28

* can load local image without specifying abs. path

# 0.9.2 - 2016 Apr 27

* improvements in rhubarbe images: can filter on names, plus minor tweaks

# 0.9.1 - 2016 Apr 20

* add config flag user_auto_prefixes to locate users

# 0.9.0 - 2016 Mar 17

* reports all even wlans as wlan0 and odd as wlan1

# 0.8.9 - 2016 Mar 16

* bugfix - rhubarbe leases was broken

# 0.8.8 - 2016 Mar 8

* bugfix - when pingable but not ssh-able, we forgot to turn off control_ssh
  this in turn resurrects the mid-size green blog in livemap

# 0.8.7 - 2016 Mar 8

* tweaks timers so that the back-channel traffic can be handled
  other changes are made to liveleases so that we should get fewer
  such messages

# 0.8.6 - 2016 Mar 7

* ditto again

# 0.8.5 - 2016 Mar 7

* bugfixes - was badly broken

# 0.8.4 - 2016 Mar 4

* new subcommands on, off, reset and info
* new subcommand nodes, so in particular
* rhubarbe nodes -a allows to see the list of all nodes declared in rhubarbe.conf

# 0.8.3 - 2016 Feb 23

* monitor & synchroneous wait:
  * wait less (now a configurable amount, default 1ms)
  * but more often (each 'leases_step')

# 0.8.2 - 2016 Feb 23

* any message sent on the 'chan-leases-request' backchannel puts
  the lease-acquisition phase on fast-track

# 0.8.1 - 2016 Feb 16

* split the Leases class in two
  * new class OmfSfaProxy to be re-used in r2lab.inria.fr

# 0.8.0 - 2016 Feb 16

* an attempt to fix imperfect packaging

# 0.7.9 - 2016 Feb 15

* bugfix, method name change had not properly propagated

# 0.7.8 - 2016 Feb 12

* more robust code for dealing with leases

# 0.7.7 - 2016 Feb 9

* monitor to also advertise to sidecar current leases on chan-leases
* new CHANGELOG.md
* new MANIFEST.in (for now only COPYING and README.md)
