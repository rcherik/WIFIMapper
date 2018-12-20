""" System """
from __future__ import print_function
import sys
import os
import time
import threading
import subprocess
""" Our stuff """
import WMConfig

class ChannelHopThread(threading.Thread):

    def __init__(self, iface=None, args=None):
	threading.Thread.__init__(self)  
        self.pid = os.getpid()
        self.args = args
        self.started = False
	self.stop = False
        self.app = None
        self.iface = iface if iface else (args.interface if args else None)
        self.bad_channels = set()
        self.current_chan = -1
        self.hop_time = WMConfig.conf.channel_hop_time
        if args and args.channels:
            self.channels = [int(chan) for chan in args.channels.split(';')]
        else:
            self.channels = WMConfig.conf.channels

    def reset_channels(self):
        self.set_channel(WMConfig.conf.channels)

    def set_channel(self, chan):
        self.stop = 1
        if isinstance(chan, int):
            self.channels = list(chan)
        elif isinstance(chan, (list, tuple)):
            self.channels = chan
        timer_thread = threading.Timer(self.WAIT_TIME, self.run)
        timer_thread.start()

    def change_channel(self, channel):
        if self.current_chan == channel:
            return False
        try:
            ret = subprocess.call([
                '/sbin/iwconfig',
                self.iface,
                'channel',
                str(channel)
                ])
        except Exception as e:
            self._say("exception sniffing: " + e.message)
            return False
        if ret != 0 and channel not in self.bad_channels:
            self._say("bad channel {chan} - ret: {ret}"\
                    .format(ret=ret, chan=channel))
            self.bad_channels.add(channel)
        else:
            #self._say("hopped to %s" % channel)
            self.current_chan = channel
        return True

    def run(self):
        self.stop = False
        self.started = True
        self._say("starting to chan hop on interface %s" % self.iface)
        while not self.stop:
            for channel in self.channels:
                if self.stop:
                    return
                self.change_channel(channel)
                time.sleep(self.hop_time)

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
