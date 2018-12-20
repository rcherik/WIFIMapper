""" System """
from __future__ import print_function
import sys
import os
import signal

import gi
gi.require_version('Gtk', '3.0')

""" Kivy """
import kivy
from kivy.app import App
if kivy.__version__ >= "1.9.1":
    import matplotlib
    matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

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
import WMConfig
from PcapThread import PcapThread
from ChannelHopThread import ChannelHopThread
from frontend_wifi_mapper.CardListScreen import CardListScreen
#from frontend_wifi_mapper.CardInfoScreen import CardInfoScreen
from frontend_wifi_mapper.WMScreenManager import WMScreenManager
from frontend_wifi_mapper.WMUtilityClasses import \
        WMPanelHeader, WMTabbedPanel, WMConfirmPopup

def stop_threads():
    app = App.get_running_app()
    app._say("stopping threads")
    app.stop_pcap_thread()
    app.stop_channel_thread()
    sys.exit(0)

class WifiMapper(App):

    def __init__(self, args, **kwargs):
        App.__init__(self)
        self.panel = None
        self.args = args
        self.manager = None
        self.paused = False
        self.popup = None
        """ Thread """
        self.pcap_thread = PcapThread(args)
        self.pcap_thread.set_application(self)
        self.channel_thread = None
        if not args.pcap and not args.no_hop:
            self.channel_thread = ChannelHopThread(args=args)
            self.channel_thread.set_application(self)
            self.pcap_thread.set_channel_hop_thread(self.channel_thread)
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
        r = self.pcap_thread.stop_input()
        self.manager.set_input_stop(r)

    def resume_input(self):
        r = self.pcap_thread.resume_input()
        self.manager.set_input_stop(r)

    def is_input(self):
        return self.pcap_thread.is_input()

    def build(self):
        self.icon = WMConfig.conf.app_icon 
        self.version = WMConfig.conf.version
        self.title = "Wifi Mapper (%s)" % self.version
        self.manager = WMScreenManager(app=self,
                args=self.args,
                pcap_thread=self.pcap_thread)
        ap_tab = WMPanelHeader(text="Access Points",
                args=self.args,
                content=self.manager,
                #background_color=(0, 128, 128, 0.25),
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
        self._say("keycode: %s" % keycode[1])
        if keycode[1] == 'shift':
            self.shift = False
        if keycode[1] == 'alt':
            self.alt = False
        if self.popup:
            return True
        if self.manager.keyboard_up(keyboard, keycode):
            return True
        if keycode[1] >= "1" and keycode[1] <= "9":
            n = int(keycode[1])
            for header in reversed(self.panel.tab_list):
                n -= 1
                if n == 0:
                    self.panel.switch_to(header)
                    return True
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
        return True

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if self.paused:
            return True
        if not self.popup\
            and self.manager.keyboard_down(keyboard, keycode, text, modifiers):
            return True
        if keycode[1] == 'shift':
            self.shift = True
            return True
        if keycode[1] == 'alt':
            self.alt = True
            return True
        if keycode[1] == 'enter':
            if self.popup:
                self.popup.confirm()
            return True
        if keycode[1] == 'escape':
            if not self.popup:
                self.popup = WMConfirmPopup(text="Do you really want to quit ?")
                self.popup.bind(on_dismiss=self._confirm_popup_stop)
                self.popup.open()
            else:
                self.popup.dismiss()
            return True
        return True

    def _confirm_popup_stop(self, widget):
        if self.popup.confirmed():
            self.stop()
        self.popup = None

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
        stop_threads(self.pcap_thread, self.channel_thread)
        self._say("stopped")

    def stop_pcap_thread(self):
        self.pcap_thread.stop = True
        if self.pcap_thread.started:
            self.pcap_thread.join(timeout=1)
            self._say("Pcap thread stopped")
            os.kill(self.pcap_thread.pid, signal.SIGKILL)

    def stop_channel_thread(self):
        if not self.channel_thread:
            return
        self.channel_thread.stop = True
        if self.channel_thread.started:
            self.channel_thread.join(timeout=1)
            self._say("Channel thread stopped")
            os.kill(self.channel_thread.pid, signal.SIGKILL)
