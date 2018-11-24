""" System """
from __future__ import print_function
import sys
import os
import time
import threading
import subprocess
""" Our stuff """
from backend_wifi_mapper.find_iface import find_iface

WAIT_TIME = 0.25

class ChannelHopThread(threading.Thread):
    def __init__(self, args):
	threading.Thread.__init__(self)  
        self.pid = os.getpid()
        self.args = args
        self.started = False
	self.stop = False
        self.app = None
        self.iface = args.interface or (find_iface() if not args.pcap else None)
        self.bad_channels = set()
        self.current_chan = 0
        if args.channels:
            self.channels = [int(chan) for chan in args.channels.split(';')]
        else:
            self.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    def run(self):
        self.started = True
        self._say("starting to chan hop on interface %s" % self.iface)
        while not self.stop:
            for channel in self.channels:
                if self.stop:
                    return
                try:
                    ret = subprocess.call([
                        '/sbin/iwconfig',
                        self.iface,
                        'channel',
                        str(channel)
                        ])
                except Exception as e:
                    self._say("exception sniffing: " + e.message)
                    continue
                if ret != 0 and channel not in self.bad_channels:
                    self._say("bad channel {chan} - ret: {ret}"\
                            .format(ret=ret, chan=channel))
                    self.bad_channels.add(channel)
                else:
                    #self._say("hopped to %s" % channel)
                    self.current_chan = channel
                time.sleep(WAIT_TIME)

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)

    def _wait_for_gui(self):
        """ Check if all screen are loaded """
        if not self.app or not hasattr(self.app, "manager"):
            self._say("app not well initialized")
            sys.exit(1)
        while not self.stop and not self.app.manager.is_ready():
            pass
        return True

    def set_application(self, app):
        """ To be able to call Kivy from thread """
        self.app = app

    def _app_shutdown(self):
        """ Stops thread and app """
        self._wait_for_gui()
        self.app.stop()
        sys.exit(1)
