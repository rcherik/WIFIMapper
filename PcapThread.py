""" System """
from __future__ import print_function
import sys
import os
import time
import threading
""" Scapy """
import scapy
import scapy.config
from scapy.all import sniff, rdpcap
from scapy.error import Scapy_Exception
""" Our Stuff """
from backend_wifi_mapper.find_iface import find_iface
from backend_wifi_mapper.wifi_mapper import parse_pkt, WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_HANDSHAKES

READ_TIME = 0.0005

WM_VENDOR = max([WM_AP, WM_STATION, WM_TRAFFIC, WM_HANDSHAKES]) + 1

class PcapThread(threading.Thread):
    def __init__(self, args, **kwargs):
	threading.Thread.__init__(self)  
        self.pid = os.getpid()
        self.args = args
        self.started = False
	self.stop = False
        self.app = None
        self.channelthread = None
        self.pkts = kwargs.get('pkts', None)
        self.pcap_file = args.pcap or None
        self.iface = args.interface or (find_iface() if not args.pcap else None)
        self.channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
	#self.pkt_dic = {'AP': {}, 'Station': {}, 'Traffic': {}}
	self.pkt_dic = [{}, {}, {}, {}, {}]
        self._get_mac_list()

    def _get_mac_list(self):
        try:
            with open('mac_list') as f:
                lines = f.readlines()
	        for l in lines:
		    t = l.split('\t')
		    self.pkt_dic[WM_VENDOR][t[0]] = t[1].replace('\n', "")
    	except Exception as e:
            self._say("error creating mac_list: %s " % e)

    def _callback_stop(self, i):
        """ Callback check if sniffing over """
	return self.stop

    def _callback(self, pkt):
        """ Callback when packet is sniffed """
        current = self.channelthread.current_chan\
                if self.channelthread else None
        parse_pkt(self.pkt_dic, pkt, channel=current)
        if self.app and hasattr(self.app, "manager"):
            self.app.manager.update_gui(self.pkt_dic)

    def _wait_for_gui(self):
        """ Check if all screen are loaded """
        if not self.app or not hasattr(self.app, "manager"):
            self._say("app not well initialized")
            sys.exit(1)
        while not self.stop and not self.app.manager.is_ready():
            pass
        return True

    def _say(self, s, **kwargs):
        if self.args and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)

    def run(self):
        """ Thread either sniff or waits """
        self.started = True
        self._say("using scapy (%s)" % scapy.config.conf.version)
        if not self.pcap_file:
            self._wait_for_gui()
            self.channelthread.start()
            self._say("starts sniffing on interface %s" % self.iface)
	    sniff(self.iface, prn=self._callback,
                    stop_filter=self._callback_stop, store=0)
        else:
            self.pkts = self.read_pkts(self.pcap_file)
            self._wait_for_gui()
            self._say("starts parsing")
            for pkt in self.pkts:
                if self.stop:
                    return
                self._callback(pkt)
                time.sleep(READ_TIME)
            self._say("has finished reading")

    def read_pkts(self, name):
        """ Load pkts from file """
        self._say("reading file {name}".format(name=name))
        start_time = time.time()
        try:
                packets = rdpcap(name)
        except (IOError, Scapy_Exception) as err:
                self._say("rdpcap: error: {}".format(err),
                        file=sys.stderr)
                self._app_shutdown()
        except NameError as err:
                self._say("rdpcap error: not a pcap file ({})".format(err),
                        file=sys.stderr)
                self._app_shutdown()
        except KeyboardInterrupt:
                self._app_shutdown()
        read_time = time.time()
        self._say("took {0:.3f} seconds".format(read_time - start_time))
        return packets

    def set_application(self, app):
        """ To be able to call Kivy from thread """
        self.app = app

    def set_channel_hop_thread(self, thread):
        """ To be able to start thread from thread """
        self.channelthread = thread

    def _app_shutdown(self):
        """ Stops thread and app """
        self._wait_for_gui()
        self.app.stop()
        sys.exit(1)
