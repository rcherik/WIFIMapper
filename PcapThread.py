""" System """
from __future__ import print_function
import sys
import time
import threading
from subprocess import Popen, PIPE
""" Scapy """
from scapy.all import sniff, rdpcap
from scapy.error import Scapy_Exception
""" Our Stuff """
from backend_wifi_mapper.wifi_mapper import parse_pkt

READ_TIME = 0.0005

class PcapThread(threading.Thread):
    def __init__(self, args, pkts=None):
	threading.Thread.__init__(self)  
	self.counter = 0
        self.started = False
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
            with open('mac_list') as f:
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
        if self.app and hasattr(self.app, "manager"):
            self.app.manager.update_gui(self.old_dic, self.vendor_dict)

    def wait_for_gui(self):
        """ Check if all screen are loaded """
        if not self.app or not hasattr(self.app, "manager"):
            print("Thread: app not well initialized")
            sys.exit(1)
        while not self.stop and not self.app.manager.is_ready():
            pass
        return True

    def run(self):
        """ Thread either sniff or waits """
        self.started = True
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
        """ Stops thread and app """
        self.wait_for_gui()
        self.app.stop()
        sys.exit(1)
