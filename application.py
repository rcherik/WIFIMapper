#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function
import argparse
import sys
import signal
import os
""" Our Stuff """
from PcapThread import PcapThread
from ChannelHopThread import ChannelHopThread
from backend_wifi_mapper.find_iface import find_iface

def parse_args():
    """ Create arguments """
    parser = argparse.ArgumentParser(prog='WifiMapper',
            usage='%(prog)s [options]')
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

if __name__ == '__main__':
    args = parse_args()
    if not args.pcap and os.geteuid():
        sys.exit('Please run as root')
    signal.signal(signal.SIGINT, signal_handler)

    args.interface = find_iface() if not args.interface else args.interface

    if args.test:
        import pkts_test
        pkts_test.test(args.interface)

    if args.interface is None and not args.pcap:
        sys.exit("Interface not found")

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
