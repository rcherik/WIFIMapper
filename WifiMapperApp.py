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

# Window settings
Config.set('graphics', 'width', '1330')
Config.set('graphics', 'height', '800')
# Removes right clicks dots on gui
Config.set('input', 'mouse', 'mouse,disable_multitouch,disable_on_activity')
# Handle escape behavior ourselves
Config.set('kivy', 'exit_on_escape', 0)
# Handle pause behavior
Config.set('kivy', 'pause_on_minimize', 1)
Config.set('kivy', 'desktop', 1)
Config.set('kivy', 'log_enable', 1)
#FPS at all time + input
#Config.set('modules', 'monitor', '')

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
from frontend_wifi_mapper.APCardInfoScreen import APCardInfoScreen
from frontend_wifi_mapper.StationCardInfoScreen import StationCardInfoScreen
from frontend_wifi_mapper.WMScreenManager import WMScreenManager
from frontend_wifi_mapper.WMUtilityClasses import \
        WMPanelHeader, WMTabbedPanel, WMConfirmPopup
from frontend_wifi_mapper.WMMainMenu import WMMainMenu
from frontend_wifi_mapper.toast import toast

Window.set_icon(WMConfig.conf.app_icon)
Window.icon = WMConfig.conf.app_icon
Config.set('kivy', 'window_icon', WMConfig.conf.app_icon)

def stop_app():
    app = App.get_running_app()
    if app.started:
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
        self.pcap_thread = None
        self.started = False
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
            self.parse_file(self.dragged)
        else:
            self.dragged = None
        self.popup = None

    def confirm_dragged_file(self, window, path):
        self._say("Dragged: %s" % path)
        self.dragged = path
        if self.popup:
            self.popup.dismiss()
        self._open_popup_confirm("Do you want to start parsing %s" % path,
                self._dismiss_dragged_file, auto_dismiss=False)

    """ Main Menu """

    def _main_menu_popup_dismiss(self, widget):
	super(WMMainMenu, widget).on_dismiss()
        self.popup = None

    def open_main_menu(self):
        if self.popup:
            if isinstance(self.popup, WMMainMenu):
                self.popup.dismiss()
                return
            self.popup.dismiss()
        self.popup = WMMainMenu(self)
        self.popup.bind(on_dismiss=self._main_menu_popup_dismiss)
        self.popup.open()

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

    def parse_file(self, path):
        if path.endswith('.pcap'):
            self._start_reading_pcap(path)
        elif path.endswith(WMConfig.conf.wm_extension):
            self._load_data(path)
        else:
            toast("Wifi Mapper does not support this file extension", True)

    def _load_data(self, path):
        self.pcap_thread.load_data(path)

    def _start_reading_pcap(self, path):
        self.stop_pcap_thread()
        self.pcap_thread = PcapThread(pcap_file=path,
                                        debug=self.args.debug,
                                        app=self)
        self.pcap_thread.start()

    """ No args app """

    def app_ready(self):
        if self.pcap_thread and self.pcap_thread.no_purpose():
            self.open_main_menu()

    """ Header global """

    def change_header(self, key, txt):
        self.panel.change_header(key, txt)

    def add_header(self, screen, **kwargs):
        #TODO bugged ?
        Clock.schedule_once(partial(self.panel.add_header,
                                    screen, **kwargs))
        #self.panel.add_header(text, key, screen, **kwargs)

    def remove_header(self, key):
        self.panel.remove_header(key)

    def open_screen(self, which, key):
        cls = None
        if which.lower() in ("sta", "station"):
            cls = StationCardInfoScreen
            obj = self.pcap_thread.get_station(key)
        elif which.lower() in ('ap', 'accesspoint'):
            cls = APCardInfoScreen
            obj = self.pcap_thread.get_ap(key)
        if not cls:
            toast("%s not found" % which, False)
            return
        if not obj:
            toast("% key not found" % key, False)
            return
        screen = cls.from_obj(obj)
        self.add_header(screen)

    """ Dispatch stop/resume """

    def stop_input(self):
        r = self.pcap_thread.stop_input()
        self.manager.set_input_stop(r)

    def resume_input(self):
        r = self.pcap_thread.resume_input()
        self.manager.set_input_stop(r)

    def is_input(self):
        return self.pcap_thread.is_input()

    """ Config """

    def build_config(self, config):
        config.adddefaultsection('General')
        config.setdefault('General', 'Version', WMConfig.conf.version)
        config.setdefault('General', 'IsFajo', "Vrai")#######TODO

        config.adddefaultsection('GUI')
        config.setdefault('GUI', 'UpdateTime',
                WMConfig.conf.gui_update_time)
        config.setdefault('GUI', 'AppIcon',
                WMConfig.conf.app_icon)
        config.setdefault('GUI', 'CardsPerScreen',
                WMConfig.conf.max_card_per_screen)

        config.adddefaultsection('Sniffer')
        config.setdefault('Sniffer', 'Hop',
                'Off' if self.args.no_hop else 'On')
        config.setdefault('Sniffer', 'HopTime',
                WMConfig.conf.channel_hop_time)
        config.setdefault('Sniffer', 'Channels',
                ', '.join(str(c) for c in WMConfig.conf.channels))

        config.adddefaultsection('Attack')
        config.setdefault('Attack', 'ChannelWaitTime',
                WMConfig.conf.channel_wait_time)
    def on_config_change(self, config, section, key, value):
        self._say("Changing conf obj in section %s with key %s value %s"\
                % (section, key, value))

    """ Setting """

    def build_settings(self, settings):
        settings.add_json_panel(
            'General Fajo', self.config, data='''[
                    { "type": "title",
                    "title": "Remi"},

                    {"type": "options",
                    "title": "Remi status",
                    "desc": "Est-ce que remi est un fajo",
                    "section": "General",
                    "key": "IsFajo",
                    "options": ["Vrai", "Faux", "Fuccbois"]}
            ]''')

        settings.add_json_panel(
            'Graphical User Interface', self.config, data='''[
                    { "type": "title",
                    "title": "Refresh"},

                    {"type": "numeric",
                    "title": "GUI update time",
                    "desc": "Time between each GUI refresh",
                    "section": "GUI",
                    "key": "UpdateTime"},

                    { "type": "title",
                    "title": "Card List Screen"},

                    {"type": "numeric",
                    "title": "Cards per screen",
                    "desc": "Number of cards listed before paging",
                    "section": "GUI",
                    "key": "CardsPerScreen"}

                    ]''')

        settings.add_json_panel(
            'Wifi Sniffer', self.config, data='''[
                    { "type": "title",
                    "title": "Channel Hopping"},

                    { "type": "bool",
                    "title": "Channel Hopping",
                    "desc": "Activate channel switching on interface",
                    "section": "Sniffer",
                    "key": "Hop",
                    "values": ["Off", "On"]},

                    {"type": "numeric",
                    "title": "Channel Hop Time",
                    "desc": "Time between channel hopping",
                    "section": "Sniffer",
                    "key": "HopTime"},

                    {"type": "string",
                    "title": "Channels",
                    "desc": "Comma separated channels to hop on",
                    "section": "Sniffer",
                    "key": "Channels"},
                    
                    { "type": "title",
                    "title": "Other TODO"}
            ]''')
        settings.add_json_panel(
            'Wifi Offensive', self.config, data='''[
                    { "type": "title",
                    "title": "Time"},

                    {"type": "numeric",
                    "title": "Channel Wait Time",
                    "desc": "Time waiting in a channel when an attack is sent",
                    "section": "Attack",
                    "key": "ChannelWaitTime"}
            ]''')

    """ Build """

    def build(self):
        self.started = True
        self.icon = WMConfig.conf.app_icon 
        self.version = WMConfig.conf.version
        self.title = "Wifi Mapper (%s)" % self.version
        self.start_time = time.time()
        """ Thread """
        self.pcap_thread = PcapThread(interface=self.args.interface,
                                        pcap_file=self.args.pcap,
                                        no_hop=self.args.no_hop,
                                        debug=self.args.debug,
                                        dump_file=self.args.wmdump,
                                        sniff=self.args.sniff,
                                        app=self)
        """ Screen Manager """
        self.manager = WMScreenManager(app=self,
                args=self.args,
                pcap_thread=self.pcap_thread)
        """ Panel Header """
        ap_tab = WMPanelHeader(text="Access Points",
                args=self.args,
                content=self.manager,
                #background_color=(0, 128, 128, 0.25),
                screen="ap",
                can_remove=False)
        """ Tabbed Panel Header """
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

    def _is_settings_open(self):
        win = self._app_window
        if win:
            settings = self._app_settings
            if settings in win.children:
                return True
        return False

    def _on_keyboard_up(self, keyboard, keycode):
        if self.paused:
            return True
        #self._say("keycode: %s" % keycode[1])
        if keycode[1] == 'shift':
            self.shift = False
        if keycode[1] == 'alt':
            self.alt = False
        if keycode[1] == 'f1':
            if not self._is_settings_open():
                self.open_settings()
            else:
                self.close_settings()
            return True
        if keycode[1] == 'm':
            self.open_main_menu()
        """ Not parsed if popup """
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
            if self._is_settings_open():
                self.close_settings()
            else:
                self._open_popup_confirm("Do you really want to quit ?",
                        self._confirm_popup_stop)
            return True
        return True

    """ Kivy app methods """

    def on_pause(self):
        self._say("On pause")
        self.paused = True
        return True

    def on_resume(self):
        self._say("On resume")
        self.paused = False

    def on_stop(self):
        self._say("On stop")
        self.stop_pcap_thread()

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

    """ Attack Methods """

    def send_packet(self, packet, iface=None, **kwargs):
        t = self.pcap_thread
        if t:
            return t.send_packet(packet, iface=iface, **kwargs)
        return False

    def stay_on_channel(self, channel, stay=0):
        t = self.get_channel_thread()
        if not t:
            return False
        if stay:
            ret = t.temporary_set_channel(channel, stay)
            if ret:
                time.sleep(t.hop_time)
            return ret
        return t.set_channel(channel)

    """ Utility """

    def get_channel_thread(self):
        if self.pcap_thread:
            return self.pcap_thread.channel_thread
        return None

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and hasattr(self.args, "debug")\
                and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)

    def error_emergency_dump(self):
        try:
            input = raw_input
        except NameError:
            pass
        if Window:
            Window.close()
        crash_dir = os.path.join(self.path, 'crash_dump')
        t = time.time()
        time_str = time.strftime("%d-%m-%Y_%H:%M:%S", time.gmtime(t))
        self._say("Entering save mode")
        if PcapThread.sniffed_pkt_list:
            answer = input("You had saved packets for a pcap file, "\
                "would you like to save them ? [y/N] ")
            if answer == 'y':
                if not os.path.exists(crash_dir):
                    os.makedirs(crash_dir)
                filename = os.path.join(crash_dir, 'emergency_pcap_{}.pcap'\
                        .format(time_str))
                try:
                    PcapThread.static_write_pcap(PcapThread.sniffed_pkt_list,
                                                                    filename)
                    self._say("Wrote pcap {}".format(filename))
                except IOError as e:
                    self._say("{}".format(e))
            else:
                self._say("Not saved")
        if PcapThread.check_if_data(PcapThread.wm_pkt_dict):
            answer = input("You had data to dump, "\
                "would you like to save them ? [y/N] ")
            if answer == 'y':
                if not os.path.exists(crash_dir):
                    os.makedirs(crash_dir)
                filename = os.path.join(crash_dir, 'emergency_dump_{}{}'\
                        .format(time_str, WMConfig.conf.wm_extension))
                try:
                    PcapThread.static_dump_data(PcapThread.wm_pkt_dict,
                                                                filename)
                    self._say("Wrote dump {}".format(filename))
                except IOError as e:
                    self._say("{}".format(e))
            else:
                self._say("Not saved")

    """ Stopping methods """

    def signal_handler(self, sig, frame):
        self.exit()

    def exit(self):
        self.stop_pcap_thread()
        self.stop()

    def stop_pcap_thread(self):
        if not self.pcap_thread:
            return
        self.pcap_thread.stop_thread()
        if self.pcap_thread.started:
            self.pcap_thread.join(timeout=3)
            self._say("Pcap thread stopped")
            if self.pcap_thread.sniffing or self.pcap_thread.reading:
                self.pcap_thread._stop_channel_thread()
                self._say("Killing App")
                os.kill(os.getpid(), signal.SIGKILL)
            self.pcap_thread = None
