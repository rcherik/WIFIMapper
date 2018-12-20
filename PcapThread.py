""" System """
from __future__ import print_function
import sys
import os
import time
import threading
import subprocess
""" Scapy """
import scapy
import scapy.config
from scapy.sendrecv import sniff
from scapy.utils import rdpcap, PcapReader
from scapy.error import Scapy_Exception
""" Our Stuff """
import interface_utilities
from backend_wifi_mapper.wifi_mapper import start_parsing_pkt
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES, get_wm_list
from backend_wifi_mapper.taxonomy import TAXONOMY_C_FILE
import WMConfig

class PcapThread(threading.Thread):

    def __init__(self, args, **kwargs):
        threading.Thread.__init__(self)
        #Own values
        self.pid = os.getpid()
        self.args = args
        self.pcap_file = args.pcap or None
        self.ifaces = None
        if not args.pcap:
            if args.interface:
                self.ifaces = [iface for iface in args.interface.split(';')]
            else:
                self.ifaces = interface_utilities.find_iface()
        self.started = False
        self.stop = False
        self.get_input = True
        self.pkts = None
        self.pkt_list = []
        self.pkt_dic = get_wm_list()
        self._get_mac_list()
        self.pkt_stats = {}

        #Options
        self.update_time = WMConfig.conf.gui_update_time

        #Other classes
        self.app = None
        self.channel_thread = None
        self.timer_thread = None

    def run(self):
        """ Thread either sniff or waits """
        self.started = True
        self._compile_c_file(TAXONOMY_C_FILE)
        self._say("using scapy (%s)" % scapy.config.conf.version)
        self._wait_for_gui()
        if not self.pcap_file:
            self._sniff()
        else:
            self._read_pcap()

    def _compile_c_file(self, name):
        """ Compile a c file for later use """
        self._say("Compiling %s file to %s" % (name, name[:-2]))
        try:
            dn = open(os.devnull, 'w')
        except IOError:
            dn = None
        try:
            ipr = subprocess.Popen(['/usr/bin/gcc', name, '-o', name[:-2]],
                    stdout=dn, stderr=dn)
            if dn:
                dn.close()
        except Exception as e:
            if dn and not dn.closed:
                dn.close()
            self._say("Could not compile file %s: %s" % (name, e.message))

    def _get_mac_list(self):
        """ Get list to match bssid with vendor """
        try:
            with open(WMConfig.conf.mac_list_file) as f:
                lines = f.readlines()
                for l in lines:
                    t = l.split('\t')
                    self.pkt_dic[WM_VENDOR][t[0]] = t[1].replace('\n', "")
        except Exception as e:
            self._say("error creating mac_list: %s " % e)

    def _update_gui(self):
        """ Update gui with pkts """
        if self.app and hasattr(self.app, "manager"):
            self.app.manager.update_gui(self.pkt_dic)
            self.pkt_dic[WM_CHANGES] = [[], []]

    def _start_update_timer(self):
        """ Update gui on timer """
        if not self.timer_thread or not self.timer_thread.isAlive():
            self.timer_thread = threading.Timer(self.update_time,
                                                self._update_gui)
            self.timer_thread.start()

    def _callback_stop(self, i):
        """ Callback check if sniffing over """
        return self.stop or not self.get_input

    def _callback(self, pkt):
        """ Callback when packet is sniffed """
        current = None
        if self.channel_thread:
            current = self.channel_thread.current_chan
        self.pkt_list.append(pkt)
        if current:
            self.pkt_stats[current] = self.pkt_stats.get(current, 0) + 1
        start_parsing_pkt(self.pkt_dic, pkt, channel=current)
        self._start_update_timer()

    def _wait_for_gui(self):
        """ Check if all screen are loaded """
        if not self.app or not hasattr(self.app, "manager"):
            self._say("app not well initialized")
            sys.exit(1)
        while not self.stop and not self.app.manager.is_ready():
            pass
        return True

    def _sniff(self):
        """ Sniff on interfaces while channel hopping """
        if self.channel_thread:
            self.channel_thread.start()
        while not self.stop:
            self._say("starts sniffing on %s %s"\
                    % ("interface" if len(self.ifaces) == 1 else "interfaces",
                        self.ifaces))
            sniff(iface=self.ifaces, prn=self._callback,
                    stop_filter=self._callback_stop, store=False)
            while not self.get_input:
                pass

    def _read_all_pcap(self):
        """ Read all pcap at once """
        self.pkts = self._read_all_pkts()
        self._wait_for_gui()
        self._say("starts parsing")
        i = 0
        for pkt in self.pkts:
            if self.stop:
                return
            self._callback(pkt)
            if i == WMConfig.conf.pcap_read_pkts_pause:
                i = -1
                time.sleep(WMConfig.conf.pcap_read_pause)
            i += 1
        self._say("has finished reading")

    def _read_all_pkts(self):
        """ Load pkts from file """
        self._say("loading full file {name}".format(name=self.pcap_file))
        start_time = time.time()
        try:
                packets = rdpcap(self.pcap_file)
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
        self._say("took {0:.3f} seconds to read {} packets"
                .format(read_time - start_time, len(packets)))
        return packets

    def _read_pkts(self, reader):
        """ Read a single pkt and callback GUI """
        i = 0
        while not self.stop:
            while not self.get_input:
                pass
            pkt = reader.read_packet()
            if pkt is None:
                break
            self._callback(pkt)
            if i == WMConfig.conf.pcap_read_pkts_pause:
                i = -1
                time.sleep(WMConfig.conf.pcap_read_pause)
            i += 1

    def _read_pcap(self):
        """ Prepare read for updating GUI pkt per pkt """
        self._say("reading file {name}".format(name=self.pcap_file))
        start_time = time.time()
        try:
            fdesc = PcapReader(self.pcap_file)
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
        self._read_pkts(fdesc)
        read_time = time.time()
        self._say("took {0:.3f} seconds to read and parse {1:d} packets"\
                .format(read_time - start_time, len(self.pkt_list)))
        
    def is_input(self):
        return not self.get_input

    def stop_input(self):
        if self.get_input:
            self._say("Stopped")
        self.get_input = False
        return True

    def resume_input(self):
        if not self.get_input:
            self._say("Resumed")
        self.get_input = True
        return False

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)

    def set_application(self, app):
        """ To be able to call Kivy from thread """
        self.app = app

    def set_channel_hop_thread(self, thread):
        """ To be able to start thread from thread """
        self.channel_thread = thread

    def _app_shutdown(self):
        """ Stops thread and app """
        self._wait_for_gui()
        self.app.stop()
        sys.exit(1)
