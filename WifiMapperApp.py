""" System """
from __future__ import print_function
import sys
import os
import signal

import gi
gi.require_version('Gtk', '3.0')

""" Forces kivy to not interpret args """
os.environ['KIVY_NO_ARGS'] = "1"

""" Kivy """
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')
""" Removes right clicks dots on gui """
Config.set('input', 'mouse', 'mouse,disable_multitouch')

Config.set('kivy', 'window_icon', os.path.join('Static', 'images', 'icon.png'))
Config.set('kivy', 'exit_on_escape', 0)
Config.set('kivy', 'pause_on_minimize', 1)

from kivy.clock import Clock
Clock.max_iteration = 20

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
if not Window:
    sys.exit("Please get an interface")
Window.set_icon(os.path.join('Static', 'images', 'icon.png'))
Window.icon = os.path.join('Static', 'images', 'icon.png')

""" Our stuff """
from frontend_wifi_mapper.CardListScreen import CardListScreen
from frontend_wifi_mapper.CardInfoScreen import CardInfoScreen
from frontend_wifi_mapper.WMUtilityClasses import WMScreenManager,\
        WMPanelHeader, WMTabbedPanel

def stop_threads(pcapthread, channelthread):
    app = App.get_running_app()
    app._say("stopping threads")
    if channelthread:
        channelthread.stop = True
        if channelthread.started:
            channelthread.join(timeout=1)
            app._say("channel stopped")
            os.kill(channelthread.pid, signal.SIGKILL)
    pcapthread.stop = True
    if pcapthread.started:
        pcapthread.join(timeout=1)
        app._say("pcap stopped")
        os.kill(pcapthread.pid, signal.SIGKILL)
    sys.exit(0)

class WifiMapper(App):

    def __init__(self, args, **kwargs):
        App.__init__(self)
        self.panel = None
        self.args = args
        self.manager = None
        self.paused = False
        """ Thread """
        self.pcapthread = kwargs['pcapthread']
        self.pcapthread.set_application(self)
        self.channelthread = kwargs.get('channelthread', None)
        if self.channelthread:
            self.channelthread.set_application(self)
        """ Keyboard """
        self.shift = False
        self.alt = False
        self.get_focus()

    def change_header(self, key, txt):
        self.panel.change_header(key, txt)

    def add_header(self, key, screen, **kwargs):
        self.panel.add_header(key, screen, **kwargs)

    def remove_header(self, string):
        self.panel.remove_header(string)

    def stop_input(self):
        r = self.pcapthread.stop_input()
        self.manager.set_input_stop(r)

    def resume_input(self):
        r = self.pcapthread.resume_input()
        self.manager.set_input_stop(r)

    def is_input(self):
        return self.pcapthread.is_input()

    def build(self):
        self.icon = os.path.join('Static', 'images', 'icon.png')
        self.version = "0.5"
        self.title = "Wifi Mapper (%s)" % self.version
        self.manager = WMScreenManager(app=self,
                args=self.args,
                pcapthread=self.pcapthread)
        ap_tab = WMPanelHeader(text="Access Points",
                args=self.args,
                content=self.manager,
                screen="ap",
                can_remove=False)
        self.panel = WMTabbedPanel(manager=self.manager,
                args=self.args,
                default_tab=ap_tab)
        return self.panel

    def get_focus(self, *args):
        self._keyboard = Window.request_keyboard(self._keyboard_closed,
                self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        if self.paused:
            return True
        if self.manager.keyboard_up(keyboard, keycode):
            return True
        if not self.alt and keycode[1] == 'tab':
            found = False
            direction = -1 if not self.shift else 1
            loop = -1 if direction == -1 else 0
            for header in self.panel.tab_list[::direction]:
                if found:
                    self.panel.switch_to(header)
                    return True
                if header == self.panel.current_tab:
                    found = True
            if found:
                self.panel.switch_to(self.panel.tab_list[loop])
            return True
        if keycode[1] == 'shift':
            self.shift = False
        if keycode[1] == 'alt':
            self.alt = False
        return True

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.paused:
            return True
        if self.manager.keyboard_down(keyboard, keycode, text, modifiers):
            return True
        if keycode[1] == 'shift':
            self.shift = True
            return True
        if keycode[1] == 'alt':
            self.alt = True
            return True
        if keycode[1] == 'escape':
            self.stop()
            return True
        return True

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)
        else:
            print(s, **kwargs)

    def on_pause(self):
        self._say("On pause")
        self.paused = True
        return True

    def on_resume(self):
        self._say("On resume")
        self.paused = False

    def onstop(self):
        self._say("leaving app - stopping threads")
        stop_threads(self.pcapthread, self.channelthread)
        self._say("stopped")
