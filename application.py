#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function
import os

""" Forces kivy to not interpret args """
os.environ['KIVY_NO_ARGS'] = "1"

import argparse
import sys
""" Kivy """
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')
""" Removes right clicks dots on gui """
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.clock import Clock
Clock.max_iteration = 20

from kivy.uix.tabbedpanel import TabbedPanel
from kivy.core.window import Window
""" Our Stuff """
from PcapThread import PcapThread
from frontend_wifi_mapper.Card import Card
from frontend_wifi_mapper.CardListScreen import CardListScreen
from frontend_wifi_mapper.CardInfoScreen import CardInfoScreen
from frontend_wifi_mapper.WMUtilityClasses import WMScreenManager,\
        WMPanelHeader, WMTabbedPanel

class WifiMapper(App):

    def __init__(self, args, thread):
	App.__init__(self)
        self.panel = None
        self.args = args
        self.manager = None
        self.thread = thread
        self.shift = False
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def add_header(self, key, screen, **kwargs):
        self.panel.add_header(key, screen, **kwargs)

    def remove_header(self, string):
        self.panel.remove_header(string)

    def build(self):
        self.manager = WMScreenManager(app=self, thread=self.thread)
        ap_tab = WMPanelHeader(text="Access Points",
                content=self.manager,
                screen="ap",
                can_remove=False)
        station_tab = WMPanelHeader(text="Stations",
                content=self.manager,
                screen="station",
                can_remove=False)
        self.panel = WMTabbedPanel(manager=self.manager,
                ap=ap_tab,
                station=station_tab,
                default_tab=ap_tab)
	return self.panel

    def _keyboard_closed(self):
	self._keyboard.unbind(on_key_down=self._on_keyboard_down)
	self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'shift':
            self.shift = False

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'tab':
            found = False
            direction = -1 if not self.shift else 1
            for header in self.panel.tab_list[::direction]:
                if found:
                    self.panel.switch_to(header)
                    return True
                if header == self.panel.current_tab:
                    found = True
            if found:
                self.panel.switch_to(self.panel.tab_list[direction])
        if keycode[1] == 'escape':
            self.stop()
        if keycode[1] == 'shift':
            self.shift = True
	return True

    def onstop(self):
        self.thread.stop = True
        self.thread.join()

def parse_args():
    """ Create arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface",
            help="Choose an interface")
    parser.add_argument("-p", "--pcap",
            help="Parse info from a pcap file; -p <pcapfilename>")
    parser.add_argument("-d", "--debug",
            help="Print some debug infos")
    return parser.parse_args()

def application_runtime_error(thread, err):
    import traceback
    traceback.print_exc()
    print("Error : " + err.message)
    thread.stop = True
    if thread.started:
        thread.join()
    sys.exit(1)

if __name__ == '__main__':
    args = parse_args()
    if not args.pcap and os.geteuid():
        sys.exit('Please run as root')
    pkts = None
    thread = PcapThread(args)
    app = WifiMapper(args, thread)
    thread.set_application(app)
    try:
        app.run()
    except Exception as err:
        application_runtime_error(thread, err)
    thread.stop = True
    if thread.started:
        thread.join()
