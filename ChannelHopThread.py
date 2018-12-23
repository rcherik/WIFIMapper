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

    def __init__(self, iface=None, channels=None, debug=None, app=None):
	threading.Thread.__init__(self)  
        self.pid = os.getpid()
        self.app = app
        self.debug = debug
        self.app = app
        self.iface = iface
        self.started = False
	self.stop = False
        self.bad_channels = set()
        self.current_chan = -1
        self.hop_time = WMConfig.conf.channel_hop_time
        if channels and isinstance(channels, basestring):
            self.channels = [int(chan) for chan in channels.split(';')]
        else:
            self.channels = WMConfig.conf.channels

    def set_interface(self, iface):
        if not isinstance(iface, basestring):
            return
        self._say("Changed interface to %s" % iface)
        self.stop = 1
        self.iface = iface
        timer_thread = threading.Timer(self.hop_time, self.run)
        timer_thread.start()

    def reset_channels(self):
        self.set_channel(WMConfig.conf.channels)

    def set_channel(self, chan):
        self._say("eee")
        if isinstance(chan, int):
            chan = list(chan)
        if self.channels == chan:
            return
        self.stop = 1
        if isinstance(chan, (list, tuple)):
            self.channels = chan
        self._say("Changed channels to %s" % self.channels)
        timer_thread = threading.Timer(self.hop_time, self.run)
        timer_thread.start()

    def change_channel(self, channel):
        if self.current_chan == channel:
            return False
        try:
            ret = subprocess.call(['/sbin/iwconfig', self.iface,
                'channel', str(channel)])
        except Exception as e:
            self._say("%s exception sniffing: %s"\
                    % (e.__class__.__name__ , e.message))
            import traceback
            traceback.print_exc()
            self.stop = True
        if ret != 0:
            if channel not in self.bad_channels:
                self._say("bad channel {chan} - ret: {ret}"\
                        .format(ret=ret, chan=channel))
                self.bad_channels.add(channel)
            self.stop = True
        else:
            #self._say("hopped to %s" % channel)
            self.current_chan = channel
        return True

    def run(self):
        self.stop = False
        self.started = True
        self._say("starting to chan hop on interface %s" % self.iface)
        while not self.stop:
            if self.bad_channels and self.bad_channels.issubset(self.channels):
                self._say("Removing bad channels : %s" % self.bad_channels)
                self.channels = [chan for chan in self.channels\
                        if chan not in self.bad_channels]
            for channel in self.channels:
                if self.stop:
                    return
                self.change_channel(channel)
                time.sleep(self.hop_time)

    def _say(self, s, **kwargs):
        if self.debug:
            s = "%s: " % (self.__class__.__name__) + s
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
