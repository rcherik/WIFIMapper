#!/usr/bin/python
#coding: utf-8

# System
from __future__ import print_function
import os

""" Force kivy not to interpret args """
os.environ['KIVY_NO_ARGS'] = "1"

import argparse
import sys
import time
import threading
from subprocess import Popen, PIPE
# Kivy
from kivy.app import App, runTouchApp

from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '800')

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
# Scapy
from scapy.all import sniff, rdpcap
from scapy.error import Scapy_Exception
# Our stuff
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
        self.pkt_idx = 0

    def find_iface(self):
        """ Fine internet interface and returns it """
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
	if self.app and self.app.layout:
            self.app.layout.parse_pkt(pkt)

    def read_one(self):
        """ Read one pkt from file """
        pkt = self.pkts[self.pkt_idx]
        self.pkt_idx += 1
        self.callback(pkt)

    def run(self):
        """ Thread either sniff or waits """
        if self.pcap_file:
            while not self.stop:
                pass
        else:
	    sniff(self.iface, prn=self.callback,
                    stop_filter=self.callback_stop, store=0)

    def set_application(self, app):
        """ To be able to call Kivy from thread """
        self.app = app

class MainLayout(StackLayout):
    def __init__(self, **kwargs):
        """ If --pcap specified, will parse a pcap file """
	super(MainLayout, self).__init__(**kwargs)
	self.btn_dic = {}
	self.dic = {}
	self.old_dic = {'AP': {}, 'Station': {}, 'Traffic': {}}
        self.thread = kwargs['thread']
        self.thread.start()
        if self.thread.pcap_file:
            Clock.schedule_interval(self.pcap_read_file, 0.01)

    def pcap_read_file(self, clock):
        """ Parse one packet from file """
        self.thread.read_one()

    def parse_pkt(self, pkt):
        """ Parse one packet """
        parse_pkt(self.old_dic, pkt)
        self.update_gui()

    def update_pkt(self, mac):
	self.btn_dic[mac].text = pkt + '| ' + str(self.dic[mac])

    def new_pkt(self, mac):
	btn = Button(text=mac + '| 1', width=30, size_hint=(0.30, 0.30))
	self.btn_dic[mac] = btn
	self.add_widget(btn)

    def add_btn(self, id, s="No name"):
	btn = Button(text=s, width=30, size_hint=(0.30, 0.30))
        self.btn_dic[id] = btn
        self.add_widget(btn)

    def update_gui(self):
        """ Update packet on GUI """
        ap = self.old_dic['AP']
        sta = self.old_dic['Station']
        for key, value in ap.iteritems():
            self.add_btn(key, "AP: %s - %s" % (key, ap[key].ssid))
        for key, value in sta.iteritems():
            s = sta[key].recv if hasattr(sta[key], 'recv') else "None"
            self.add_btn(key, "Sta: %s - %s" % (key, s))

class Wifi_mapper(App):
    def __init__(self, args, thread):
	App.__init__(self)
	self.thread = thread
	self.layout = None

    def build(self):
	self.layout = MainLayout(thread=self.thread)
	return self.layout

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
    print("Reading file {}".format(name))
    start_time = time.time()
    try:
            packets = rdpcap(name)
    except (IOError, Scapy_Exception) as err:
            print("Pcap parser error: {}".format(err),
                    file=sys.stderr)
            sys.exit(1)
    except NameError as err:
            print("Pcap parser error: not a pcap file ({})".format(err),
                    file=sys.stderr)
            sys.exit(1)
    except KeyboardInterrupt:
            sys.exit(1)
    read_time = time.time()
    print("Took {0:.3f} seconds".format(read_time - start_time))
    return packets

if __name__ == '__main__':
    if os.geteuid():
        sys.exit('Please run as root')

    args = parse_args()
    pkts = None
    if args.pcap:
        pkts = read_pkts(args.pcap)
    thread = Thread(args, pkts)
    app = Wifi_mapper(args, thread)
    thread.set_application(app)

    try:
        app.run()
    except Exception as err:
        import traceback
        traceback.print_exc()
        print("Error : " + err.message)
        thread.stop = True
        thread.join()
        sys.exit(0) 
    thread.stop = True
    thread.join()
