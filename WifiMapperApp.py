""" System """
from __future__ import print_function
import sys
import os
import signal

import gi
gi.require_version('Gtk', '3.0')


""" Kivy """
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')
""" Removes right clicks dots on gui """
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.clock import Clock
Clock.max_iteration = 20

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
if not Window:
    sys.exit("Please get an interface")

""" Our stuff """
from frontend_wifi_mapper.Card import Card
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

    def pause_input(self):
        r = self.pcapthread.pause_input()
        self.manager.set_input_pause(r)

    def resume_input(self):
        r = self.pcapthread.resume_input()
        self.manager.set_input_pause(r)

    def is_input(self):
        return self.pcapthread.is_input()

    def build(self):
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

    def get_focus(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed,
                self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'shift':
            self.shift = False
        if keycode[1] == 'alt':
            self.alt = False

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.paused:
            return
        ret = False
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
        if keycode[1] == 'escape':
            self.stop()
            return True
        if keycode[1] == 'shift':
            self.shift = True
            return True
        if keycode[1] == 'alt':
            self.alt = True
            return True
        ret = self.manager.keyboard_down(keyboard, keycode, text, modifiers)
        return ret

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)
        else:
            print(s, **kwargs)

    def on_pause(self):
        self.paused = True

    def on_resume(self):
        self.paused = False

    def onstop(self):
        self._say("leaving app - stopping threads")
        stop_threads(self.pcapthread, self.channelthread)
        self._say("stopped")
