#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function
import argparse
import sys
import signal
import os

""" Forces kivy to not interpret args """
os.environ['KIVY_NO_ARGS'] = "1"

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')

""" Our Stuff """
from backend_wifi_mapper.find_iface import find_iface
from PcapThread import PcapThread
from ChannelHopThread import ChannelHopThread

def parse_args():
    """ Create arguments """
    parser = argparse.ArgumentParser(prog='WifiMapper')
    parser.add_argument("-i", "--interface",
            type=str,
            help="Choose an interface")
    parser.add_argument("-p", "--pcap",
            type=str,
            help="Parse info from a pcap file; -p <pcapfilename>")
    parser.add_argument("-c", "--channels",
            type=str,
            help="Listen on specific channels; -c <channel1;channel2;...>")
    parser.add_argument("-n", "--no-hop",
            action='store_true',
            help="No channel hopping")
    parser.add_argument("-d", "--debug",
            action='store_true',
            help="Print some debug infos")
    parser.add_argument("-t", "--test",
            action='store_true',
            help="Print packets for your monitoring then quits")
    parser.add_argument("-l", "--live-update",
            type=int,
            help="Packets sniffed before gui update; -l <number>")
    parser.add_argument("-r", "--read-update",
            type=int,
            help="Time between each pkts read in ms; -r <number>")
    return parser.parse_args()

def application_runtime_error(pcapthread, channelthread, err):
    import traceback
    traceback.print_exc()
    print("RuntimeError : " + err.message)
    WifiMapperApp.stop_threads(pcapthread, channelthread)
    sys.exit(1)

def signal_handler(signal, frame):
    global g_pcapthread
    global g_channelthread
    from kivy.app import App
    app = App.get_running_app()
    app._say("CTRL+C signal")
    app.stop()

def is_interface_up(iface):
    """
        http://lxr.free-electrons.com/source/include/uapi/linux/if_arp.h

        Managed Mode: Type = 1 (ARPHRD_ETHER)
        Monitor Mode: Type = 803 (ARPHRD_IEEE80211_RADIOTAP)
    """
    if os.name == 'posix':
        with open('/sys/class/net/%s/type' % iface, 'r') as f:
            t = int(f.read())
            if t == 1:
                return False
            elif t == 803:
                return True
        return False
    return False

def list_interfaces():
    lst = []
    wireless_lst = []
    if os.name == 'posix':
        for dir in os.listdir('/sys/class/net'):
            lst.append(dir)
        for iface in lst:
            if os.path.isdir('/sys/class/net/%s/wireless' % iface):
                wireless_lst.append(iface)
    return wireless_lst, lst

def say(s, **kwargs):
    print("WifiMapper: %s" % s, **kwargs)

if __name__ == '__main__':
    args = parse_args()
    if not args.pcap and os.geteuid():
        say("Please run as root")
        sys.exit(1)
    signal.signal(signal.SIGINT, signal_handler)

    wireless_lst, iface_lst = list_interfaces()

    args.interface = find_iface() if not args.interface else args.interface

    if not args.pcap and (args.interface not in iface_lst):
        say("Interface%s not found"\
                % (" " + args.interface if args.interface else ""))
        if iface_lst:
            say("Found interfaces: %s" % iface_lst)
        if wireless_lst:
            say("Wireless interfaces: %s" % wireless_lst)
        sys.exit(1)

    if args.test:
        import pkts_test
        pkts_test.test(args.interface)

    if not args.pcap and not is_interface_up(args.interface):
        say("Interface %s not monitoring" % args.interface)
        say("to monitor: make monitor")
        say("to rollback: make managed")
        sys.exit(1)

    if not args.pcap and args.interface not in wireless_lst:
        say("Interface %s not wireless" % args.interface)
        say("Wireless interfaces: %s" % wireless_lst)
        sys.exit(1)

    """ Threads """
    pcapthread = PcapThread(args)
    g_pcapthread = pcapthread
    channelthread = None
    if not args.pcap and not args.no_hop:
        channelthread = ChannelHopThread(args)
        pcapthread.set_channel_hop_thread(channelthread)
    g_channelthread = channelthread

    """ App """
    import  WifiMapperApp
    app = WifiMapperApp.WifiMapper(args,
            pcapthread=pcapthread,
            channelthread=channelthread)
    try:
        app.run()
    except Exception as err:
        application_runtime_error(pcapthread, channelthread, err)
    WifiMapperApp.stop_threads(pcapthread, channelthread)
