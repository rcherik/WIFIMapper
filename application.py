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
from kivy.app import App, runTouchApp

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')
""" Removes right clicks dots on gui """
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
""" Our Stuff """
from PcapThread import PcapThread
from frontend_wifi_mapper.Card import Card
from frontend_wifi_mapper.MainScreen import MainScreen
from frontend_wifi_mapper.WMUtilityClasses import WMScreenManager, WMPanelHeader

class WifiMapper(App):

    def __init__(self, args, thread):
	App.__init__(self)
        self.panel = None
        self.managers = []
        self.panel_dic = {}
        self.args = args
        self.thread = thread

    def add_panel(self, string, content):
        if string not in self.panel_dic:
            panel = WMPanelHeader(master=self.panel, text=string)
            panel.content = content
            self.panel_dic[string] = panel
            self.panel.add_widget(panel)

    def build(self):
        """
            Build a panel that contains WMScreenManagers

            self.managers contains every WMScreenManagers
            self.panel_dic contains every Panels
        """
	self.ap_manager = WMScreenManager(app=self, ap=True)
	self.station_manager = WMScreenManager(app=self, station=True)
        self.managers.append(self.ap_manager)
        self.managers.append(self.station_manager)

        self.panel= TabbedPanel(tab_width=150)
        self.panel.default_tab_text = "Access Points"
        self.panel.default_tab_content = self.ap_manager
        self.panel_dic["AP"] = self.panel
        self.add_panel("Station", self.station_manager)

        thread.start()

	return self.panel

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
    return parser.parse_args()

def application_runtime_error(thread, err):
    import traceback
    traceback.print_exc()
    print("Error : " + err.message)
    thread.stop = True
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
    thread.join()
