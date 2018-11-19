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
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

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
from kivy.graphics import Color, Rectangle
""" Scapy """
from scapy.all import sniff, rdpcap
from scapy.error import Scapy_Exception
""" Our Stuff """
from wifi_mapper import parse_pkt

Builder.load_file("build.kv")

READ_TIME = 0.0005

class PcapThread(threading.Thread):
    def __init__(self, args, pkts=None):
	threading.Thread.__init__(self)  
	self.counter = 0
	self.stop = False
        self.app = None
        if args.pcap:
            self.iface = None
        else:
            self.iface = args.interface or self.find_iface()
        self.pcap_file = args.pcap or None
        self.pkts = pkts
	self.dic = {}
	self.old_dic = {'AP': {}, 'Station': {}, 'Traffic': {}}
	self.vendor_dict = {}
        try:
            with open('./mac_list') as f:
                lines = f.readlines()
	        for l in lines:
		    t = l.split('\t')
		    self.vendor_dict[t[0]] = t[1]
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
                manager.screen.update_gui(self.old_dic, self.vendor_dict)

    def wait_for_gui(self):
        """ Check if all screen are loaded """
        if not self.app or not hasattr(self.app, "managers"):
            print("Thread: app not well initialized")
            return False
        gui_loaded = False
        while not gui_loaded:
            if self.stop:
                return False
            for manager in self.app.managers:
                if not manager.screen.ready:
                    gui_loaded = False
                    break
                else:
                    gui_loaded = True
        return True

    def run(self):
        """ Thread either sniff or waits """
        if not self.pcap_file:
            self.wait_for_gui()
            print("Thread: screens are ready - Starts sniffing")
	    sniff(self.iface, prn=self.callback,
                    stop_filter=self.callback_stop, store=0)
        else:
            self.pkts = self.read_pkts(self.pcap_file)
            self.wait_for_gui()
            print("Thread: screens are ready - Starts reading")
            for pkt in self.pkts:
                if self.stop:
                    return
                self.callback(pkt)
                time.sleep(READ_TIME)
            print("Thread: has finished reading")

    def read_pkts(self, name):
        """ Load pkts from file """
        print("Thread: reading file {name}".format(name=name))
        start_time = time.time()
        try:
                packets = rdpcap(name)
        except (IOError, Scapy_Exception) as err:
                print("rdpcap: error: {}".format(err),
                        file=sys.stderr)
                self.app_shutdown()
        except NameError as err:
                print("rdpcap error: not a pcap file ({})".format(err),
                        file=sys.stderr)
                self.app_shutdown()
        except KeyboardInterrupt:
                self.app_shutdown()
        read_time = time.time()
        print("Thread: took {0:.3f} seconds".format(read_time - start_time))
        return packets

    def set_application(self, app):
        """ To be able to call Kivy from thread """
        self.app = app

    def app_shutdown(self):
        self.wait_for_gui()
        self.app.stop()
        sys.exit(1)

class AppScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        """ Add screen for thread accessibility """
        super(AppScreenManager, self).__init__(**kwargs)
        self.app = kwargs.get('app', None)
        self.screen = ScrollScreen(**kwargs)
        self.add_widget(self.screen)

class Card(BoxLayout):

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.id = kwargs['id']
        self.elem_lst = {}
        self.width = 0
        self.connected = False
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
        self.create(**kwargs)

    def get_args(self, **kwargs):
        self.text = kwargs.get('text', None)
        self.ap = kwargs.get('ap', None)
        self.station = kwargs.get('station', None)
        self.vendor = kwargs.get('vendor', None)

    def create(self, **kwargs):
        self.get_args(**kwargs)
        if self.text:
            self.create_text()
        elif self.ap:
            self.create_ap()
        elif self.station:
            self.create_station()
	    self.is_connected()

    def add_label(self, key, text, max_height):
        text = text or ""
        l = len(text)
        label = Label(text=text,
                    size_hint=(1, max_height))
        self.width = l * 10 if self.width < l * 10 else self.width
        self.elem_lst[key] = label
        self.add_widget(label)

    def create_ap(self):
        self.max_height = 0.33
        s = "ssid: " + (self.ap.ssid or "")
        self.add_label("ssid", s, self.max_height)
        s = "bssid: " + (self.ap.bssid or "")
        self.add_label("bssid", s, self.max_height)
        self.add_label("vendor", self.vendor, self.max_height)

    def create_station(self):
        self.max_height = 0.2
        s = "ssid: " + (self.station.station or "")
        self.add_label("station", s, self.max_height)
        s = "ap: " + (self.station.bssid or "")
        self.add_label("bssid", s, self.max_height)
        s = "probes: " + self.station.get_probes()
        self.add_label("probes", s, self.max_height)
        self.add_label("vendor", self.vendor, self.max_height)

    def create_text(self):
        infos = self.text.split(';')
        self.max_height = 1.0 / len(infos)
        for i, info in enumerate(infos):
           self.add_label(str(i), info, self.max_height)
 
    def update(self, **kwargs):
        self.get_args(**kwargs)
        if self.text:
            self.update_text()
        elif self.ap:
            self.update_ap()
        elif self.station:
            self.is_connected()
            self.update_station()

    def update_label(self, key, value):
        if not value or self.elem_lst[key].text == value:
            return
        l = len(value)
        self.width = l * 10 if self.width < l * 10 else self.width
        self.elem_lst[key].text = value

    def update_ap(self):
        s = "ssid: " + (self.ap.ssid or "")
        self.update_label("ssid", s)
        s = "bssid: " + (self.ap.bssid or "")
        self.update_label("bssid", s)
        self.update_label("vendor", self.vendor)

    def update_station(self):
        s = "ssid: " + (self.station.station or "")
        self.update_label("station", s)
        s = "ap: " + (self.station.bssid or "")
        self.update_label("bssid", s)
        s = "probes: " + self.station.get_probes()
        self.update_label("probes", s)
        self.update_label("vendor", self.vendor)

    def update_text(self):
        infos = self.text.split(';')
        for i, info in enumerate(infos):
            self.update_label(str(i), info)

    def on_touch_down(self, touch):
        #TODO open a tab with card infos
        if self.collide_point(*touch.pos):
            print("Card: Touched !")
            self.pressed = touch.pos
            App.get_running_app().add_panel(str(self.id), self)
            return True
        return super(Card, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('Card: pressed at {pos}'.format(pos=pos))

    def is_connected(self):
        if not self.connected and self.station and self.station.bssid:
            self.connected = True
            self.draw_background(self, self.pos)
        elif self.connected and self.station and not self.station.bssid:
            self.connected = False
            self.draw_background(self, self.pos)

    def draw_background(self, widget, prop):
        self.canvas.before.clear()
	with self.canvas.before:
            if self.connected:
	        Color(0, 1, 0, 0.25)
            else:
	        Color(1, 1, 1, 0.1)
	    Rectangle(pos=self.pos, size=self.size)

class ScrollScreen(Screen):

    view = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Delays view creation """
	super(ScrollScreen, self).__init__(**kwargs)
        self.ready = False
	self.card_dic = {}
        self.app = kwargs.get('app', None)
        self.show_ap = kwargs.get('ap', False)
	self.show_station = kwargs.get('station', False)

        """ Python background color """
	with self.canvas.before:
	    Color(0, 0, 0, 0)
	    self.rect = Rectangle(size=self.size, pos=self.pos)
	self.bind(size=self._update_rect, pos=self._update_rect)

	Clock.schedule_once(self.create_view)

    def _update_rect(self, instance, value):
        """ Update background color """
	self.rect.pos = instance.pos
	self.rect.size = instance.size

    def create_view(self, dt):
        """ Create layout """
        self.layout = StackLayout(orientation="lr-tb",
                padding=10,
                spacing=10,
                size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.view.add_widget(self.layout)
        self.ready = True

    def add_ap_card(self, mac, ap, vendor):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = Card(id=mac, ap=ap, vendor=vendor)
            self.layout.add_widget(card)
            self.card_dic[mac] = card
        else:
            self.card_dic[mac].update(id=mac, ap=ap, vendor=vendor)

    def add_station_card(self, mac, station, vendor):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = Card(id=mac, station=station, vendor=vendor)
            self.layout.add_widget(card)
            self.card_dic[mac] = card
        else:
            self.card_dic[mac].update(id=mac, station=station, vendor=vendor)

    def add_card(self, mac, s, vendor):
        """ Add button or update it """
        if mac not in self.card_dic:
            s = s or ""
            card = Card(id=mac, text=s, vendor=vendor)
            self.layout.add_widget(card)
            self.card_dic[mac] = card
        else:
            self.card_dic[mac].update(id=mac, text=s, vendor=vendor)

    def update_gui(self, dic, vendor_dic):
        """ Update GUI """
        if self.show_ap:
            ap = dic['AP']
            for key, value in ap.iteritems():
                vendor = vendor_dic.get(key[:8].upper(), "")
                self.add_ap_card(key, ap[key], vendor)
        if self.show_station:
            sta = dic['Station']
            for key, value in sta.iteritems():
                probes = sta[key].get_probes()
                s = "%s;%s;%s" % (key, probes, key)
                vendor = vendor_dic.get(key[:8].upper(), "")
                self.add_station_card(key, sta[key], vendor)

class WMPanelHeader(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super(WMPanelHeader, self).__init__(**kwargs)
        self.master = kwargs.get('master', None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Panel: Touched ! " + touch.button)
            self.pressed = touch.pos
            if touch.button == "right" and self.text != "Station":
                self.master.remove_widget(self)
                return True
        return super(WMPanelHeader, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('Panel: pressed at {pos}'.format(pos=pos))

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
            Build a panel that contains AppScreenManagers

            self.managers contains every AppScreenManagers
            self.panel_dic contains every Panels
        """
	self.ap_manager = AppScreenManager(app=self, ap=True)
	self.station_manager = AppScreenManager(app=self, station=True)
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
