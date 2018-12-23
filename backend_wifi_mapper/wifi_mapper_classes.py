#! /usr/bin/python
#coding: utf-8
from __future__ import print_function
from scapy.all import Dot11Elt
import time
import struct
""" Our stuff """
from wifi_mapper_utilities import is_broadcast, is_retransmitted
from wifi_mapper_utilities import WM_AP, WM_STATION,\
		WM_TRAFFIC, WM_VENDOR
from taxonomy import identify_wifi_device

"""
	Present in main dictionnary in dic[WM_TRAFFIC][some_bssid_key]
	Used only to get station traffic
"""

WM_TRA_SENT = 0
WM_TRA_RECV = 1

WM_TRA_ALL = 0
WM_TRA_MNG = 1
WM_TRA_CTRL = 2
WM_TRA_DATA = 3

class Traffic():

	def __init__(self, dic, bssid):
		self.bssid = bssid
		self.sent = 0
		self.recv = 0
		self.max_sig = 0
		self.avg_sig = 0.0
		self.min_sig = 0
		self.first = True
		self.sigs = 0
		self.n = 0
		self.dic = dic
		self.traffic = {}
		self.timeline = []

	def plot(self):
		pass

	def prepare_traffic_dict(self, addr):
		self.traffic[addr] = {
				'sent': {
					'management': 0,
					'all': 0
				},
				'recv': {
					'management': 0,
					'all': 0
				}
		}
		#TODO
		"""
		self.traffic[addr] = [
				[0, 0, 0, 0],
				[0, 0, 0, 0],
				]
		"""

	def get_sent(self, addr, key):
		if addr in self.traffic and\
			key in self.traffic[addr]['sent']:
			return self.traffic[addr]['sent'][key]
		return 0

	def get_recv(self, addr, key):
		if addr in self.traffic and\
			key in self.traffic[addr]['recv']:
			return self.traffic[addr]['recv'][key]
		return 0

	def add_sent(self, addr):
		self.sent += 1
		self.timeline.append(int(time.time()))
		if not addr:
			return
		if addr not in self.traffic:
			self.prepare_traffic_dict(addr)
			self.traffic[addr]['sent']['all'] = 1
		else:
			self.traffic[addr]['sent']['all'] += 1

	def add_recv(self, addr):
		self.recv += 1
		self.timeline.append(int(time.time()))
		if addr not in self.traffic:
			self.prepare_traffic_dict(addr)
			self.traffic[addr]['recv']['all'] = 1
		else:
			self.traffic[addr]['recv']['all'] += 1

	def get_rssi_avg(self):
		if self.n == 0:
			return self.sigs
		return float(self.sigs / self.n)

"""
	Present in main dictionnary in dic[WM_STATION][some_bssid_key]
"""

#TODO
WM_STA_STEP_DONE = 0
WM_STA_SUCESS = 1
WM_STA_FAIL = 2
WM_STA_EXT = 3
WM_STA_KICK = 4
WM_STA_AUTH = 5
WM_STA_AUTH_RESP = 6
WM_STA_DEAUTH = 7
WM_STA_ASSOS = 8
WM_STA_REASSOS = 9
WM_STA_ASSOS_RESP = 10
WM_STA_REASSOS_RESP = 11
WM_STA_DISASSOS = 12
WM_STA_HDSK_PKT = 13
WM_STA_LAST_SUCCESS = 14
WM_STA_CURRENT_STEP = 15

class Station():

	id = 0

	def __init__(self, dic, bssid, oui_dict=None, hop_channel=None):
		self.dic = dic
		self.bssid = bssid
		self.oui = oui_dict.get(bssid[:8].upper(), "") if oui_dict else None

		self.ap_bssid = None
		self.probe_req = None
		self.assoc_req = None
		self.rssi = 0
		self.ap_probed = []
		self.ap_probed_str = None
		self.model = None
		self.connected = False
		self.connected_history = []
		self.channel = hop_channel

		Station.id += 1
		self.id = Station.id
		if bssid not in dic[WM_TRAFFIC]:
			dic[WM_TRAFFIC][bssid] = Traffic(dic, bssid)

	def get_ap_name(self, bssid):
		obj = self.dic[WM_AP].get(bssid, None)
		if obj:
			return obj.get_name()
		return bssid

	def get_name(self):
		if self.oui:
			return "%s%s" % (self.oui[:8], self.bssid[8:])
		return self.bssid

	def set_channel(self, channel):
		self.channel = channel

	def set_connected(self, ap_bssid):
		if not ap_bssid:
			return
		new_ap_obj = self.dic[WM_AP].get(ap_bssid, None)
		if ap_bssid != self.ap_bssid:
			time_str = time.strftime("%H:%M:%S", time.gmtime())
			current_ap_obj = self.dic[WM_AP].get(self.ap_bssid, None)
			current_ap_name = current_ap_obj.get_name()\
					if current_ap_obj else self.ap_bssid
			new_ap_name = new_ap_obj.get_name()\
					if new_ap_obj else ap_bssid

			if current_ap_obj:
				current_ap_obj.client_disconnected(self.bssid)
			if self.ap_bssid:
				self.connected_history.insert(0,
						(time_str, current_ap_name, "disconnected", self.ap_bssid))
			self.connected_history.insert(0,
					(time_str, new_ap_name, "connected", ap_bssid))

		self.connected = True
		self.ap_bssid = ap_bssid
		if new_ap_obj:
			new_ap_obj.client_connected(self.bssid)

	def set_disconnected(self):
		if self.ap_bssid and self.connected:
			self.connected = False
			current_ap_obj = self.dic[WM_AP].get(self.ap_bssid, None)
			current_ap_name = current_ap_obj.get_name()\
					if current_ap_obj else self.ap_bssid
			if current_ap_obj:
				current_ap_obj.client_disconnected(self.bssid)
			time_str = time.strftime("%H:%M:%S", time.gmtime())
			self.connected_history.insert(0,
					(time_str, current_ap_name, "disconnected", self.ap_bssid))
			self.ap_bssid = None

	def set_rssi(self, rssi):
		if self.rssi != rssi:
			self.rssi = rssi
	
	def add_ap_probed(self, ssid):
		if ssid not in self.ap_probed:
			self.ap_probed.append(ssid)
			self.ap_probed_str = self.get_ap_probed()

	def set_model(self, bssid, probe_req, assoc_req, oui):
		self.model = identify_wifi_device(bssid, probe_req, assoc_req, \
			oui)
		if self.model is None:
			self.model = False

	def set_probeReq(self, probe_req):
		self.probe_req = probe_req
		#We have the probe_req, the assoc_req and the oui and we never
		#tried to guess the model: try it.
		if self.assoc_req is not None\
				and self.model == None\
				and self.oui is not None:
			self.set_model(self.bssid, self.probe_req, \
				self.assoc_req, self.oui.lower())

	def set_assocReq(self, assoc_req):
		self.assoc_req = assoc_req
		#We have the probe_req, the assoc_req and the oui and we never
		#tried to guess the model: try it.
		if self.probe_req is not None\
				and self.model == None\
				and self.oui is not None:
			self.set_model(self.bssid, self.probe_req, \
				self.assoc_req, self.oui.lower())

	def __getitem__(self, key):
		return self.__dict__[key]

	def get_ap_probed(self):
		return ', '.join(self.ap_probed)

"""
	Present in main dictionnary in dic[WM_AP][some_bssid_key]
"""
class AccessPoint():

	def __init__(self, dic, bssid, ssid=None, oui_dict=None, hop_channel=None):
		self.dic = dic
		self.bssid = bssid
		self.oui = oui_dict.get(bssid[:8].upper(), "") if oui_dict else None

		self.ssid = None
		self.channel = None
		self.hop_channel = hop_channel
		self.security = None
		self.known = False
		self.wps = None
		self.beacons = 0
		self.proberesp = 0
		self.rssi = 0
		self.client_co = set()
		self.client_hist_co = []
		self.n_clients = 0

		if bssid not in dic[WM_TRAFFIC]:
			dic[WM_TRAFFIC][bssid] = Traffic(dic, bssid)

	def get_station_name(self, bssid):
		obj = self.dic[WM_STATION].get(bssid, None)
		if obj:
			return obj.get_name()
		return bssid

	def get_name(self):
		if self.oui:
			return "%s%s" % (self.oui[:8], self.bssid[8:])
		return self.bssid

	def set_rssi(self, rssi):
		if rssi != self.rssi:
			self.rssi = rssi
	
	def set_ssid(self, ssid):
		try:
			utf8_ssid = ssid.decode('utf-8')
		except UnicodeDecodeError:
			return
		if utf8_ssid != self.ssid:
			self.ssid = utf8_ssid
	
	def set_channel(self, channel):
		if self.channel != channel:
			try:
				self.channel = int(channel.encode('hex'), 16)
			except Exception, e:
				print('set_channel failed: ', e)
	
	def set_known(self, known):
		if self.known != known:
			self.known = known

	def set_security(self, pkt):
		elem = pkt[Dot11Elt]
		security = None
		while isinstance(elem, Dot11Elt):
			if elem.ID == 48:
				security = "WPA2"
			elif elem.ID == 221 and hasattr(elem, "info") and\
				elem.info.startswith('\x00P\xf2\x01\x01\x00'):
				security = "WPA"
			elem = elem.payload
		if not security:
			capabilities = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"\
				"{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
			if 'privacy' in capabilities:
				security = "WEP"
			else:
				security = "OPN"
		if security != self.security:
			self.security = security
	
	def get_security(self):
		wps_str = "has wps" if self.wps is True else "no wps"
		if not self.security and not self.wps:
			return ""
		if self.security is None and isinstance(self.wps, bool):
			return wps_str
		if self.wps is None and self.security:
			return self.security
		return "%s | %s" % (self.security, wps_str)

	def set_wps(self, elem):
		"""
		wps_format = {
			"Type":"B", #1
			"DataElemVersion":"H", #2
			"DataElemVersionLen":"H", #2
			"Version":"B", #1
			"DataElemWPS":"H", #2
			"DataElemWPSLen":"H", #2
			"WPSSetup":"B", #1
		}
		"""
		if len(elem.info) < 11:
			return None
		data = ">BHHBHHB"
		try:
			decoded = struct.unpack(data, elem.info[:11])
		except Exception as e:
			print(e.message)
			print([x for x in elem.info[:11]])
			return None
		if len(decoded) < 6:
			return None
		self.wps = int(decoded[6]) == 0x2

	def add_beacon(self):
		self.beacons += 1
		self.known = True

	def client_connected(self, bssid):
		if bssid not in self.client_co:
			time_str = time.strftime("%H:%M:%S", time.gmtime())
			self.client_co.add(bssid)
			obj = self.dic[WM_STATION].get(bssid, None)
			name = obj.get_name() if obj else bssid
			self.client_hist_co.insert(0, (time_str, name, "connected", bssid))
			self.n_clients += 1

	def client_disconnected(self, bssid):
		if bssid in self.client_co:
			self.n_clients -= 1
			self.client_co.remove(bssid)
		time_str = time.strftime("%H:%M:%S", time.gmtime())
		obj = self.dic[WM_STATION].get(bssid, None)
		name = obj.get_name() if obj else bssid
		self.client_hist_co.insert(0, (time_str, name, "disconnected", bssid))

	def __getitem__(self, key):
		return self.__dict__[key]

	def get_seen(self):
		#Used in web interface to get reasons why AP is in table
		return ""
		if len(self.seen) == 0:
			return ""
		s = ', '.join(self.seen)
		s = "seen: {}".format(s)
		if self.ssid is not None and len(self.ssid) > 0:
			s = "{} (probed: {})".format(s, self.ssid)
		return s

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
