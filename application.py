#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function
import os

""" Forces kivy to not interpret args """
os.environ['KIVY_NO_ARGS'] = "1"

import argparse
import sys
import time
import threading
from subprocess import Popen, PIPE
""" Kivy """
from kivy.app import App, runTouchApp

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.properties import ObjectProperty
from kivy.clock import Clock
""" Scapy """
from scapy.all import sniff, rdpcap
from scapy.error import Scapy_Exception
""" Our Stuff """
from wifi_mapper import parse_pkt

Builder.load_file("build.kv")

class Thread(threading.Thread):
    def __init__(self, args, pkts=None):
	threading.Thread.__init__(self)  
	self.counter = 0
	self.stop = False
        self.app = None
        self.iface = args.interface or self.find_iface()
        self.pcap_file = args.pcap or None
        self.pkts = pkts
	self.dic = {}
	self.old_dic = {'AP': {}, 'Station': {}, 'Traffic': {}}
	self.mac_dict = {}
        try:
            with open('./mac_list') as f:
                lines = f.readlines()
	        for l in lines:
		    t = l.split('\t')
		    self.mac_dict[t[0]] = t[1]
    	except Exception as e:
            print("Thread: error creating mac_list: %s " % e)


    def find_iface(self):
        """ Find internet interface and returns it """
        try:
            dn = open("/dev/NULL", 'w')
        except IOError:
            dn = None
        try:
            ipr = Popen(['/sbin/ip', 'route'], stdout=PIPE, stderr=dn)
            dn.close()
            for line in ipr.communicate()[0].splitlines():
                if 'default' in line:
                    l = line.split()
                    iface = l[4]
                    return iface
        except Exception as e:
            if dn and not dn.closed:
                dn.close()
            sys.exit('Could not find interface: ' + e.message)

    def callback_stop(self, i):
        """ Callback check if sniffing over """
	return self.stop

    def callback(self, pkt):
        """ Callback when packet is sniffed """
        parse_pkt(self.old_dic, pkt)
        if self.app and hasattr(self.app, "managers"):
            for manager in self.app.managers:
                manager.screen.update_gui(self.old_dic, self.mac_dict)

    def wait_for_gui(self):
        """ Check if all screen are loaded """
        gui_loaded = False
        while not gui_loaded:
            if self.app and hasattr(self.app, "managers"):
                for manager in self.app.managers:
                    if not manager.screen.ready:
                        gui_loaded = False
                        break
                    else:
                        gui_loaded = True

    def run(self):
        """ Thread either sniff or waits """
        self.wait_for_gui()
        print("Thread: screens are ready - Starts ", end="")
        if not self.pcap_file:
            print("sniffing")
	    sniff(self.iface, prn=self.callback,
                    stop_filter=self.callback_stop, store=0)
        else:
            print("reading")
            for pkt in self.pkts:
                self.callback(pkt)
                time.sleep(0.0001)
            print("Thread: has finished reading")

    def set_application(self, app):
        """ To be able to call Kivy from thread """
        self.app = app

class AppScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        """ Add screen for thread accessibility """
        super(AppScreenManager, self).__init__(**kwargs)
        self.screen = ScrollScreen(**kwargs)
        self.add_widget(self.screen)

class ScrollScreen(Screen):

    view = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Delays view creation """
	super(ScrollScreen, self).__init__(**kwargs)
        self.ready = False
	self.btn_dic = {}
        self.show_ap = kwargs.get('ap', False)
        self.show_station = kwargs.get('station', False)
        Clock.schedule_once(self.create_view)

    def create_view(self, dt):
        """ Create layout """
        self.layout = StackLayout(orientation="lr-tb",
                                    size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.view.add_widget(self.layout)
        self.ready = True

    def add_btn(self, id, s="No name"):
        """ Add button or update it """
        if id not in self.btn_dic:
            btn = Button(text=s,
                    size=(len(s) * 10, 50),
                    size_hint=(None, None))
            self.btn_dic[id] = btn
            self.layout.add_widget(btn)
        else:
            self.btn_dic[id].text = s
            self.btn_dic[id].size = (len(s) * 10, 50)

    def update_gui(self, dic, mac_dic):
        """ Update GUI """
        if self.show_ap:
            ap = dic['AP']
            for key, value in ap.iteritems():
                mac = mac_dic.get(key[:8].upper(), "")
                self.add_btn(key, "AP: %s - %s | %s" % (key, ap[key].ssid, mac))
        if self.show_station:
            sta = dic['Station']
            for key, value in sta.iteritems():
                s = sta[key].get_probes()
                mac = mac_dic.get(key[:8].upper(), "").upper()
                self.add_btn(key, "Sta: %s - %s | %s" % (key, s, mac))

class WifiMapper(App):

    def __init__(self, args, thread):
	App.__init__(self)
        self.panel = None
        self.managers = []
        self.panel_lst = []
        self.args = args
        self.thread = thread

    def build(self):
        """
            Build a panel that contains AppScreenManagers

            self.managers contains every AppScreenManagers
            self.panel_lst contains every Panels
        """
	self.ap_manager = AppScreenManager(ap=True)
	self.station_manager = AppScreenManager(station=True)
        self.managers.append(self.ap_manager)
        self.managers.append(self.station_manager)

        self.panel= TabbedPanel()
        self.panel.default_tab_text = "Access Points"
        self.panel.default_tab_content = self.ap_manager
        th_station = TabbedPanelHeader(text="Station")
        th_station.content = self.station_manager

        self.panel_lst.append(self.panel)
        self.panel_lst.append(th_station)
        self.panel.add_widget(th_station)

        g_thread.start()

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

def read_pkts(name):
    """ Load pkts from file """
    print("WifiMapper: reading file {}".format(name))
    start_time = time.time()
    try:
            packets = rdpcap(name)
    except (IOError, Scapy_Exception) as err:
            print("rdpcap: error: {}".format(err),
                    file=sys.stderr)
            sys.exit(1)
    except NameError as err:
            print("rdpcap error: not a pcap file ({})".format(err),
                    file=sys.stderr)
            sys.exit(1)
    except KeyboardInterrupt:
            sys.exit(1)
    read_time = time.time()
    print("WifiMapper: took {0:.3f} seconds".format(read_time - start_time))
    return packets

if __name__ == '__main__':
    if os.geteuid():
        sys.exit('Please run as root')

    args = parse_args()
    pkts = None
    if args.pcap:
        pkts = read_pkts(args.pcap)
    g_thread = Thread(args, pkts)
    app = WifiMapper(args, g_thread)
    g_thread.set_application(app)

    try:
        app.run()
    except Exception as err:
        import traceback
        traceback.print_exc()
        print("Error : " + err.message)
        g_thread.stop = True
        g_thread.join()
        sys.exit(0) 
    g_thread.stop = True
    g_thread.join()
