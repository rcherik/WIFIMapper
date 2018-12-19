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
from backend_wifi_mapper.find_iface import find_iface
from backend_wifi_mapper.wifi_mapper import start_parsing_pkt
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES, get_wm_list
from backend_wifi_mapper.taxonomy import TAXONOMY_C_FILE

DEFAULT_READ_TIME = 0.0005
DEFAULT_RELOAD_BY_PKT = 1
DEFAULT_UPDATE_TIME = 0.5

class PcapThread(threading.Thread):

    def __init__(self, args, **kwargs):
        threading.Thread.__init__(self)
        #Own values
        self.pid = os.getpid()
        self.args = args
        self.started = False
        self.stop = False
        self.sniff = True
        self.pcap_file = args.pcap or None
        self.pkts = None
        self.pkt_list = []
        self.pkt_dic = get_wm_list()
        self.iface = args.interface\
                or (find_iface() if not args.pcap else None)
        self._get_mac_list()

        #Options
        self.update_time = DEFAULT_UPDATE_TIME
        self.read_update = DEFAULT_READ_TIME
        if args.read_update:
            self.read_update = float(args.read_update) / 1000
        self.update_count = 0
        self.live_update = args.live_update or DEFAULT_RELOAD_BY_PKT

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
        try:
            with open('mac_list') as f:
                lines = f.readlines()
                for l in lines:
                    t = l.split('\t')
                    self.pkt_dic[WM_VENDOR][t[0]] = t[1].replace('\n', "")
        except Exception as e:
            self._say("error creating mac_list: %s " % e)

    def _update_gui(self):
        if self.app and hasattr(self.app, "manager"):
            self.app.manager.update_gui(self.pkt_dic)
            self.pkt_dic[WM_CHANGES] = [[], []]
            """
            if self.pcap_file:
                self.app.manager.update_gui(self.pkt_dic)
	        self.pkt_dic[WM_CHANGES] = [[], []]
            elif self.update_count == 0:
                self.app.manager.update_gui(self.pkt_dic)
	        self.pkt_dic[WM_CHANGES] = [[], []]
        self.update_count = 0\
                if self.update_count > self.live_update\
                else self.update_count + 1
            """

    def _start_update_timer(self):
        if not self.timer_thread or not self.timer_thread.isAlive():
            self.timer_thread = threading.Timer(self.update_time,
                                                self._update_gui)
            self.timer_thread.start()

    def _callback_stop(self, i):
        """ Callback check if sniffing over """
        return self.stop or not self.sniff

    def _callback(self, pkt):
        """ Callback when packet is sniffed """
        current = self.channel_thread.current_chan\
                if self.channel_thread else None
        self.pkt_list.append(pkt)
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
        if self.channel_thread:
            self.channel_thread.start()
        while not self.stop:
            self._say("starts sniffing on interface %s" % self.iface)
            sniff(iface=self.iface, prn=self._callback,
                    stop_filter=self._callback_stop, store=False)
            while not self.sniff:
                pass

    def _read_all_pcap(self):
        self.pkts = self._read_all_pkts()
        self._wait_for_gui()
        self._say("starts parsing")
        for pkt in self.pkts:
            if self.stop:
                return
            self._callback(pkt)
            time.sleep(self.read_update)
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
        while not self.stop:
            while not self.sniff:
                pass
            pkt = reader.read_packet()
            if pkt is None:
                break
            self._callback(pkt)
            time.sleep(self.read_update)

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
        return not self.sniff

    def stop_input(self):
        if self.sniff:
            self._say("Stopped")
        self.sniff = False
        return True

    def resume_input(self):
        if not self.sniff:
            self._say("Resumed")
        self.sniff = True
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
