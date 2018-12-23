""" System """
from __future__ import print_function
import sys
import os
import signal
import time

from functools import partial

import gi
gi.require_version('Gtk', '3.0')

""" Addon """
import psutil

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
Config.set('input', 'mouse', 'mouse,disable_multitouch,disable_on_activity')
Config.set('kivy', 'exit_on_escape', 0)
Config.set('kivy', 'pause_on_minimize', 1)
Config.set('kivy', 'desktop', 1)
Config.set('kivy', 'log_enable', 1)
#Config.set('kivy', 'log_name', "WMLog.log")

from kivy.clock import Clock
Clock.max_iteration = 20

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
if not Window:
    sys.exit("Please get an interface")

""" Our stuff """
import WMConfig
from PcapThread import PcapThread
from ChannelHopThread import ChannelHopThread
from frontend_wifi_mapper.CardListScreen import CardListScreen
from frontend_wifi_mapper.WMScreenManager import WMScreenManager
from frontend_wifi_mapper.WMUtilityClasses import \
        WMPanelHeader, WMTabbedPanel, WMConfirmPopup
from frontend_wifi_mapper.WMOptions import WMOptions

Window.set_icon(WMConfig.conf.app_icon)
Window.icon = WMConfig.conf.app_icon
Config.set('kivy', 'window_icon', WMConfig.conf.app_icon)

def stop_app():
    app = App.get_running_app()
    app._say("stopping app")
    app.exit()

class WifiMapper(App):

    def __init__(self, args, **kwargs):
        App.__init__(self)
        self.args = args
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.process = psutil.Process(os.getpid())
        Config.set('kivy', 'log_level', 'debug' if args.debug else 'info')
        Config.set('kivy', 'log_dir', os.path.join(self.path, "logs"))
        self.panel = None
        self.manager = None
        self.paused = False
        self.popup = None
        """ Thread """
        self.pcap_thread = PcapThread(interface=self.args.interface,
                                        pcap_file=self.args.pcap,
                                        no_hop=self.args.no_hop,
                                        debug=self.args.debug,
                                        app=self)
        """ Keyboard """
        self.shift = False
        self.alt = False
        self.get_focus()
        """ Signal """
        signal.signal(signal.SIGINT, self.signal_handler)
        """ Drag """
        Window.bind(on_dropfile=self.confirm_dragged_file)
        self.dragged = None

    """ Dragged file """

    def _dismiss_dragged_file(self, widget):
        if widget.confirmed():
            self.start_reading_pcap(self.dragged)
        else:
            self.dragged = None
        self.popup = None

    def confirm_dragged_file(self, window, path):
        self._say("Dragged: %s" % path)
        self.dragged = path
        self._open_popup_confirm("Do you want to start parsing %s" % path,
                self._dismiss_dragged_file, auto_dismiss=False)

    """ Options """

    def _options_popup_dismiss(self, widget):
	super(WMOptions, widget).on_dismiss()
        self.popup = None

    def open_options(self):
        if self.popup:
            self.popup.dismiss()
        self.popup = WMOptions(self)
        self.popup.bind(on_dismiss=self._options_popup_dismiss)
        self.popup.open()

    """ Header global """

    def start_sniffing(self, ifaces):
        if self.pcap_thread.sniffing\
                and self.pcap_thread.ifaces == ifaces:
            self._say("Already sniffing")
            return
        self.stop_pcap_thread()
        self.pcap_thread = PcapThread(interface=ifaces,
                                        no_hop=self.args.no_hop,
                                        debug=self.args.debug,
                                        app=self)
        self.pcap_thread.start()

    def start_reading_pcap(self, path):
        self.stop_pcap_thread()
        self.pcap_thread = PcapThread(pcap_file=path,
                                        debug=self.args.debug,
                                        app=self)
        self.pcap_thread.start()

    def app_ready(self):
        if self.pcap_thread.no_purpose():
            self.open_options()

    def change_header(self, key, txt):
        self.panel.change_header(key, txt)

    def add_header(self, text, key, screen, **kwargs):
        Clock.schedule_once(partial(self.panel.add_header,
                                    text, key, screen, **kwargs))
        #self.panel.add_header(text, key, screen, **kwargs)

    def remove_header(self, key):
        self.panel.remove_header(key)

    def open_card_link(self, which, key):
        self.manager.open_card_link(which, key)

    """ Dispatch stop/resume """

    def stop_input(self):
        r = self.pcap_thread.stop_input()
        self.manager.set_input_stop(r)

    def resume_input(self):
        r = self.pcap_thread.resume_input()
        self.manager.set_input_stop(r)

    def is_input(self):
        return self.pcap_thread.is_input()

    """ Build """

    def build(self):
        self.icon = WMConfig.conf.app_icon 
        self.version = WMConfig.conf.version
        self.title = "Wifi Mapper (%s)" % self.version
        self.start_time = time.time()
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

    """ Keyboard """

    def get_focus(self, *args):
        self._keyboard = Window.request_keyboard(self._keyboard_closed,
                self.root)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    """ Kivy app methods """

    def on_pause(self):
        self._say("On pause")
        self.paused = True
        return True

    def on_resume(self):
        self._say("On resume")
        self.paused = False

    def onstop(self):
        self._say("leaving app - stopping threads")
        self.stop_pcap_thread()
        self._say("stopped")

    def _on_keyboard_up(self, keyboard, keycode):
        if self.paused:
            return True
        #self._say("keycode: %s" % keycode[1])
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
            self.panel.go_to(n)
            return True
        if not self.alt and keycode[1] == 'tab':
            if self.shift:
                self.panel.go_back()
            else:
                self.panel.go_forth()
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
            self._open_popup_confirm("Do you really want to quit ?",
                    self._confirm_popup_stop)
            return True
        return True

    """ Confirm Popup """

    def _open_popup_confirm(self, text, fun, **kwargs):
        if not self.popup:
            self.popup = WMConfirmPopup(text=text, **kwargs)
            self.popup.bind(on_dismiss=fun)
            self.popup.open()
        else:
            if isinstance(self.popup, WMConfirmPopup):
                #TODO maybe cancel() for release
                self.popup.confirm()
            else:
                self.popup.dismiss()

    def _confirm_popup_stop(self, widget):
        if self.popup.confirmed():
            self.exit()
        self.popup = None

    """ Utility """

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and hasattr(self.args, "debug")\
                and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)

    """ Stopping methods """

    def signal_handler(self, sig, frame):
        self.exit()

    def exit(self):
        self.stop_pcap_thread()
        self.stop()

    def stop_pcap_thread(self):
        if not self.pcap_thread:
            return
        """
        if self.pcap_thread.channel_thread:
            self.pcap_thread.channel_thread.stop = True
            self.pcap_thread.channel_thread.join(timeout=1)
            self.pcap_thread.channel_thread = None
        """
        self.pcap_thread.stop_thread()
        if self.pcap_thread.started:
            self.pcap_thread.join(timeout=3)
            self._say("Pcap thread stopped")
            self.pcap_thread = None
