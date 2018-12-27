#!/usr/bin/python
#coding: utf-8

""" System """
from __future__ import print_function
import argparse
import sys
import os
import signal

""" Forces kivy to not interpret args """
os.environ['KIVY_NO_ARGS'] = "1"

""" Our Stuff """
import interface_utilities

def parse_args():
    """ Create arguments """
    parser = argparse.ArgumentParser(prog='WifiMapper')
    parser.add_argument("-i", "--interface",
            type=str,
            default=None,
            help="Choose interfaces to sniff on; -i <iface1;iface2;...>")
    parser.add_argument("-p", "--pcap",
            type=str,
            default=None,
            help="Parse info from a pcap file; -p <pcapfilename>")
    """
    parser.add_argument("-c", "--channels",
            type=str,
            help="Listen on specific channels; -c <channel1;channel2;...>")
    """
    parser.add_argument("-n", "--no-hop",
            action='store_true',
            default=False,
            help="No channel hopping")
    parser.add_argument("-l", "--list",
            action='store_true',
            help="List interfaces")
    parser.add_argument("-d", "--debug",
            action='store_true',
            default=False,
            help="Print some debug infos")
    parser.add_argument("-t", "--test",
            action='store_true',
            help="Print packets for your monitoring then quits")
    return parser.parse_args()

def application_runtime_error(err):
    import traceback
    traceback.print_exc()
    print("RuntimeError : %s" % err)
    WifiMapperApp.stop_app()
    os.kill(os.getpid(), signal.SIGKILL)

def say(s, **kwargs):
    print("WifiMapper: %s" % s, **kwargs)

def list_interfaces():
    wireless, ifaces = interface_utilities.list_interfaces()
    print("Interfaces:")
    for iface in ifaces:
        s = "\t-%s" % iface
        if iface in wireless:
            s += " (wireless)"
        if interface_utilities.is_interface_monitoring(iface):
            s += " (monitoring)"
        print(s)

if __name__ == '__main__':

    args = parse_args()

    if args.list:
        list_interfaces()
        sys.exit(0)

    wireless_lst, iface_lst = interface_utilities.list_interfaces()
    args.interface = args.interface or None

    if not args.pcap and args.interface and (args.interface not in iface_lst):
        say("Interface%s not found"\
                % (" " + args.interface if args.interface else ""))
        list_interfaces()
        sys.exit(1)

    if args.test:
        import pkts_test
        pkts_test.test(args.interface)

    if not args.pcap and args.interface\
            and not interface_utilities.\
                is_interface_monitoring(args.interface):
        say("Interface %s not monitoring" % args.interface)
        say("to monitor: make monitor")
        say("to rollback: make managed")
        list_interfaces()
        sys.exit(1)

    if not args.pcap and args.interface\
            and (args.interface not in wireless_lst):
        say("Interface %s not wireless" % args.interface)
        list_interfaces()
        sys.exit(1)

    if ((not args.pcap and args.interface) or args.test) and os.geteuid():
        say("Please run as root")
        sys.exit(1)

    """ App """
    import  WifiMapperApp
    app = WifiMapperApp.WifiMapper(args)
    try:
        app.run()
    except Exception as err:
        from backend_wifi_mapper.wifi_mapper_utilities import WM_CHANGES
        pkt = app.pcap_thread.pkt_dic
        print("Last changes before going dark: ")
        print(pkt[WM_CHANGES])
        print("---- Error ----")
        application_runtime_error(err)
    WifiMapperApp.stop_app()
