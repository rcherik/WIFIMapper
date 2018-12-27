""" System """
from __future__ import print_function
import sys
import os
import time
import threading
import subprocess
try:
    import cPickle as pickle
except:
    import pickle
""" Scapy """
import scapy
import scapy.config
from scapy.sendrecv import sniff
from scapy.utils import rdpcap, PcapReader, wrpcap
from scapy.error import Scapy_Exception
""" Our Stuff """
import interface_utilities
from backend_wifi_mapper.wifi_mapper_attack import send_pkt
from backend_wifi_mapper.wifi_mapper import start_parsing_pkt
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES, get_wm_list
from backend_wifi_mapper.taxonomy import TAXONOMY_C_FILE
import WMConfig
from frontend_wifi_mapper.toast import toast
from ChannelHopThread import ChannelHopThread

class PcapThread(threading.Thread):

    #Global WM dict
    wm_pkt_dict = get_wm_list()
    #List of files read with [file_name] = (packets_read, has_stopped)
    files_read = {}
    #A set of compiled files so we don't have to compile them again
    compiled_files = set()
    #Pkts sniffed
    sniffed_pkt_list = []
    #Channel pkt stat
    channel_pkt_stats = [0 for i in range(1, 15)]

    def __init__(self, interface=None, pcap_file=None, no_hop=False,
                                                debug=None, app=None):
        threading.Thread.__init__(self)
        #Own values
        self.app = app
        self.debug = debug
        self.no_hop = no_hop
        #Check if file to read or set sniffing mode
        self.snifs = True if interface else False
        if not self.snifs:
            self._set_reading_file(pcap_file)
        #Try to get a valid interface
        self.ifaces = None
        if self.snifs:
            self.ifaces = interface
            if not self.ifaces:
                self.ifaces = interface_utilities.find_iface()
        self.started = False
        self.stop = False
        self.get_input = True
        #Scapy pkts var
        self.pkt_dic = PcapThread.wm_pkt_dict
        self.pkt_list = PcapThread.sniffed_pkt_list
        self.save_pkts = False
        self.n_saved_pkts = 0
        self.n_pkts = 0
        self.pkt_stats = PcapThread.channel_pkt_stats
        self.reading = False
        self.sniffing = False

        #Utilities
        self._get_mac_list()
        self._compile_c_file(TAXONOMY_C_FILE)

        #Options
        self.update_time = float(self.app.config.get('GUI', 'UpdateTime'))

        #Other classes
        self.channel_thread = None
        self.timer_thread = None

    def run(self):
        """ Thread either sniff or waits """

        self.started = True
        self._say("using scapy (%s)" % scapy.config.conf.version)
        self._wait_for_gui()
        if self.snifs:
            self.start_sniffing(self.ifaces)
        elif self.pcap_file:
            self.parse_pcap_file(self.pcap_file)

    """ Attack Methods """ #TODO own thread ?

    def send_packet(self, packet, iface=None, **kwargs):
        if not iface and not self.channel_thread:
            return False
        if not iface:
            iface = self.channel_thread.iface
        #Wifi Mapper backend
        send_pkt(packet, iface, **kwargs)


    """
        ****
            PcapThread GUI methods
        ****
    """

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
        if self.snifs and self.save_pkts:
            self.pkt_list.append(pkt)
            self.n_saved_pkts += 1
        if current:
            self.pkt_stats[current] += 1
        #Wifi Mapper backend
        start_parsing_pkt(self.pkt_dic, pkt, channel=current)
        self.n_pkts += 1
        self._start_update_timer()

    def _wait_for_gui(self):
        """ Check if all screen are loaded """
        if not self.app or not hasattr(self.app, "manager"):
            self._say("app not well initialized")
            self._app_shutdown()
        while not self.stop and not self.app.manager.is_ready():
            pass
        return True

    """
        ****
            PcapThread SNIFFING methods
        ****
    """

    def reset_saved_pkts(self):
        self.save_pkts = False
        self.n_saved_pkts = 0
        PcapThread.sniffed_pkt_list = []
        self.pkt_list = PcapThread.sniffed_pkt_list

    def start_saving_pkts(self):
        self.save_pkts = not self.save_pkts
        return self.save_pkts

    def start_sniffing(self, ifaces):
        if isinstance(ifaces, basestring):
            self.ifaces = [iface for iface in ifaces.split(';')]
        else:
            self.ifaces = ifaces
        self.snifs = True
        self._sniff()

    def _sniff(self):
        """ Sniff on interfaces while channel hopping """
        if not self.no_hop and not self.channel_thread:
            self.channel_thread = ChannelHopThread(debug=self.debug,
                    iface=self.ifaces[0],
                    app=self.app)
            self.channel_thread.start()
        while not self.stop:
            self._say("starts sniffing on %s %s"\
                    % ("interface" if len(self.ifaces) == 1 else "interfaces",
                        self.ifaces))
            self.sniffing = True
            sniff(iface=self.ifaces, prn=self._callback,
                    stop_filter=self._callback_stop, store=False)
            self.sniffing = False
            while not self.get_input and not self.stop:
                pass
        self._say("Stopped sniffing")
        self._stop_channel_thread()

    """
        ****
            PcapThread READING methods
        ****
    """

    def _set_reading_file(self, path):
        self.pcap_file = os.path.abspath(path) if path else None

    def parse_pcap_file(self, path):
        if path in PcapThread.files_read\
                and PcapThread.files_read[path][1] == False:
            toast("File %s already read" % path, True)
            return
        if self.reading:
            self.stop = True
            time.sleep(WMConfig.conf.pcap_read_pause)
            self.stop = False
        self._read_pcap(path)

    def _recover_file_status(self, reader, skip_pkts):
        n = 0
        while not self.stop:
            pkt = reader.read_packet()
            if pkt is None:
                break
            #Skip pkts until the end
            n += 1
            if n < skip_pkts:
                continue
            break
        if not self.stop:
            toast("Recovered !", False)

    def _recover_previously_read(self, path):
        if path in PcapThread.files_read\
                and PcapThread.files_read[path][1] == True:
            return PcapThread.files_read[path][0]
        return 0

    def _read_pkts(self, reader):
        """ Read a single pkt and callback GUI """
        #n_pkts = 0
        n_pkts_pause = 0
        self.reading = True
        #If file already read but stopped, recover n packets read
        skip_pkts = self._recover_previously_read(self.pcap_file)
        if skip_pkts:
            toast("Recovering file - previously read %d packets"\
                    % skip_pkts, False)
            self._recover_file_status(reader, skip_pkts)
        pause_time = WMConfig.conf.pcap_read_pause
        read_pkts_pause = WMConfig.conf.pcap_read_pkts_pause
        while not self.stop:
            while not self.get_input and not self.stop:
                pass
            pkt = reader.read_packet()
            if pkt is None:
                break
            #Skip pkts until the end
            #if n_pkts < skip_pkts:
            #    continue
            self._callback(pkt)
            if n_pkts_pause == read_pkts_pause:
                n_pkts_pause = -1
                time.sleep(pause_time)
            n_pkts_pause += 1
            #n_pkts += 1
        self.reading = False
        return self.stop

    def _read_pcap(self, path):
        """ Prepare read for updating GUI pkt per pkt """
        self._say("reading file {name}".format(name=path))
        start_time = time.time()
        try:
            fdesc = PcapReader(path)
            self._set_reading_file(path)
        except (IOError, Scapy_Exception) as err:
            toast("{}".format(err), True)
            self._say("rdpcap: error: {}".format(err),
                    file=sys.stderr)
            return
            #self._app_shutdown()
        except NameError as err:
            toast("{}".format(err), True)
            self._say("rdpcap error: not a pcap file ({})".format(err),
                    file=sys.stderr)
            return
            #self._app_shutdown()
        except KeyboardInterrupt:
            self._app_shutdown()
        has_stopped = self._read_pkts(fdesc)
        l = self.n_pkts + self._recover_previously_read(path)
        PcapThread.files_read[path] = (l, has_stopped)
        if has_stopped:
            return
        read_time = time.time()
        toast("File {0:s} read - {1:d} packets".format(path, l), True)
        self._say("took {0:.3f} seconds to read and parse {1:d} packets"\
                .format(read_time - start_time, l))

    """
        ****
            PcapThread OTHER - FILE - UTILITY methods
        ****
    """

    def dump_data(self, filename):
        if not self.pkt_dic:
            return
        data = [
            dict(self.pkt_dic[WM_AP]),
            dict(self.pkt_dic[WM_STATION]),
            dict(self.pkt_dic[WM_TRAFFIC])
            ]
        try:
            with open(filename, 'wb') as f:
                f.write(WMConfig.conf.magic_file)
                pickle.dump(3, f)
                for elem in data:
                    pickle.dump(elem, f)
            s = "Saved data to file %s" % (filename)
            toast(s, False)
            self._say(s)
            return True
        except IOError as err:
            toast("Failed to save data to %s" % (filename), True)
            self._say("{}".format(err))
        return False

    def _check_magic(self, f):
        magic = f.read(len(WMConfig.conf.magic_file))
        if magic.startswith(WMConfig.conf.magic_file):
            return True
        else:
            raise NameError("Bad magic for loading "
                    "Wifi Mapper file: '%s'" % magic)
        return False

    def _parse_data(self, f):
        data = []
        size = int(pickle.load(f))
        self._say(str(size))
        for i in range(size):
            data.append(pickle.load(f))
        return data

    def load_data(self, filename):
        self.app.stop_input()
        try:
            with open(filename, 'rb') as f:
                if self._check_magic(f):
                    data = self._parse_data(f)
            self._say("Loaded data from %s" % (filename))
            self.pkt_dic[WM_AP].update(data[WM_AP])
            self.pkt_dic[WM_STATION].update(data[WM_STATION])
            self.pkt_dic[WM_TRAFFIC].update(data[WM_TRAFFIC])
            for bssid, obj in data[WM_AP].iteritems():
                self.pkt_dic[WM_CHANGES][WM_AP].append(bssid)
                obj.dic = self.pkt_dic
            for bssid, obj in data[WM_STATION].iteritems():
                self.pkt_dic[WM_CHANGES][WM_STATION].append(bssid)
                obj.dic = self.pkt_dic
            for bssid, obj in data[WM_TRAFFIC].iteritems():
                obj.dic = self.pkt_dic
            self.app.resume_input()
            self._start_update_timer()
            self._say("Start loading with new packets GUI")
            toast("Loaded data from {}".format(filename), True)
            return True
        except IOError as err:
            toast("{}".format(err), True)
            self._say("{}".format(err))
        except NameError as err:
            toast("{}".format(err), True)
            self._say("{}".format(err))
        except ValueError as err:
            toast("ValueError: old or corrupted Wfi Mapper dump file", True)
            self._say("{}".format(err))
        return False

    def write_pcap(self, filename, append=False):
        if not isinstance(filename, basestring)\
                or not self.pkt_list:
            return
        self._say("Writing pcap to file %s" % filename)
        wrpcap(filename, self.pkt_list, append=append)

    def _compile_c_file(self, name):
        """ Compile a c file for later use """
        if name in PcapThread.compiled_files:
            return
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
            PcapThread.compiled_files.add(name)
        except Exception as e:
            if dn and not dn.closed:
                dn.close()
            self._say("Could not compile file %s: %s" % (name, e.message))

    def _get_mac_list(self):
        """ Get list to match bssid with vendor """
        if self.pkt_dic[WM_VENDOR]:
            return
        try:
            with open(WMConfig.conf.mac_list_file) as f:
                lines = f.readlines()
                for l in lines:
                    t = l.split('\t')
                    self.pkt_dic[WM_VENDOR][t[0]] = t[1].replace('\n', "")
        except Exception as e:
            self._say("error creating mac_list: %s " % e)

    """ Stop input flow from pcap thread """

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

    """ Utility """

    def get_ap(self, key):
        return self.pkt_dic[WM_AP].get(key, None)

    def get_station(self, key):
        return self.pkt_dic[WM_STATION].get(key, None)

    def doing_nothing(self):
        return not self.reading and not self.sniffing

    def no_purpose(self):
        return not self.ifaces and not self.pcap_file

    def _say(self, s, **kwargs):
        if self.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)

    """ Stop thread """

    def stop_thread(self):
        #self._stop_channel_thread()
        self.stop = True

    def _stop_channel_thread(self):
        if self.channel_thread and self.channel_thread.started:
            self.channel_thread.stop = True
            self.channel_thread.join(timeout=1)
            self.channel_thread = None
            self._say("Channel thread stopped")

    def _app_shutdown(self):
        """ Stops thread and app """
        self._stop_channel_thread()
        if self.app:
            self.app.stop()
        sys.exit(1)
