#! /usr/bin/python
# -*- coding: utf-8 -*-

from wifi_mapper_utilities import is_broadcast, is_retransmitted
from wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_HANDSHAKES, WM_VENDOR
from scapy.all import Dot11Elt
import struct

"""
	Classes used in dictionnary from pcap_paser.parse method
"""

"""
	Present in main dictionnary in dic['Traffic'][some_station_key]
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

	def add_sent(self, addr, which=None):
		self.sent += 1
		if addr not in self.traffic:
			self.prepare_traffic_dict(addr)
			self.traffic[addr]['sent']['all'] = 1
		else:
			self.traffic[addr]['sent']['all'] += 1
		if which is None:
			self.traffic[addr]['sent']['management'] += 1
			return
		if which not in self.traffic[addr]['sent']:
			self.traffic[addr]['sent'][which] = 1
		else:
			self.traffic[addr]['sent'][which] += 1
		if which not in ('control', 'data'):
			self.traffic[addr]['sent']['management'] += 1

	def add_recv(self, addr, which=None):
		self.recv += 1
		if addr not in self.traffic:
			self.prepare_traffic_dict(addr)
			self.traffic[addr]['recv']['all'] = 1
		else:
			self.traffic[addr]['recv']['all'] += 1
		if which is None:
			self.traffic[addr]['recv']['management'] += 1
			return
		if which not in self.traffic[addr]['recv']:
			self.traffic[addr]['recv'][which] = 1
		else:
			self.traffic[addr]['recv'][which] += 1
		if which not in ('control', 'data'):
			self.traffic[addr]['recv']['management'] += 1

	def get_rssi_avg(self):
		if self.n == 0:
			return self.sigs
		return float(self.sigs / self.n)

"""
	Present in main dictionnary in dic['Station'][some_macaddr_key]
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

	def __init__(self, dic, bssid, oui_dict=None):
		self.dic = dic
		self.bssid = bssid
		self.oui = oui_dict.get(bssid[:8].upper(), "") if oui_dict else None

		self.probe_req = None
		self.assoc_req = None
		self.rssi = 0
		self.ap_probed = []
		self.model = None
		self.connected = False
		self.ap_bssid = None
		self.new_data = True

		Station.id += 1
		self.id = Station.id
		if bssid not in dic[WM_TRAFFIC]:
			dic[WM_TRAFFIC][bssid] = Traffic(dic, bssid)

	def set_connected(self, ap_bssid):
		if ap_bssid and ap_bssid != self.ap_bssid:
			self.new_data = True
			self.connected = True
			self.ap_bssid = ap_bssid
			#TODO meh
			if not self.ap_bssid in self.dic[WM_AP]:
				self.dic[WM_AP][self.ap_bssid] = AccessPoint(self.dic, self.ap_bssid)
			self.dic[WM_AP][ap_bssid].client_connected(self.bssid)
		elif not ap_bssid and self.connected:
			self.new_data = True
			self.connected = False
			#TODO meh
			if self.ap_bssid:
				if not self.ap_bssid in self.dic[WM_AP]:
					self.dic[WM_AP][self.ap_bssid] = AccessPoint(self.dic, self.ap_bssid)
				self.dic[WM_AP][self.ap_bssid].client_disconnected(self.bssid)

			self.ap_bssid = None

	def set_rssi(self, rssi):
		if self.rssi != rssi:
			self.new_data = True
			self.rssi = rssi
	
	def add_ap_probed(self, ssid):
		if ssid not in self.ap_probed:
			self.new_data = True
			self.ap_probed.append(ssid)

	def set_probeReq(self, probe_req):
		self.probe_req = probe_req
		#We have both the probe_req and the assoc_req and we never
		#tried to guess the model: try it.
#		if self.assoc_req is not None and self.model == None:
#			self.model = taxonomy(self.probe_req, self.assoc_req)
		#	self.new_data = True

	def set_assocReq(self, assoc_req):
		self.assoc_req = assoc_req
		#We have both the probe_req and the assoc_req and we never
		#tried to guess the model: try it.
#		if self.probe_req is not None and self.model == None:
#			self.model = taxonomy(self.probe_req, self.assoc_req)
			#self.new_data = True

	def __getitem__(self, key):
		return self.__dict__[key]

	def get_ap_probed(self):
		return ', '.join(self.ap_probed)

"""
	Present in main dictionnary in dic['AP'][some_bssid_key]
"""
class AccessPoint():

	def __init__(self, dic, bssid, ssid=None, oui_dict=None):
		self.dic = dic
		self.bssid = bssid
		self.oui = oui_dict.get(bssid[:8].upper(), "") if oui_dict else None

		self.ssid = None
		self.channel = None
		self.security = None
		self.known = False
		self.wps = None
		self.beacons = 0
		self.proberesp = 0
		self.new_data = True
		self.rssi = 0
		self.client_co = set()
		self.client_hist_co = []

		if bssid not in dic[WM_TRAFFIC]:
			dic[WM_TRAFFIC][bssid] = Traffic(dic, bssid)

	def set_rssi(self, rssi):
		if rssi != self.rssi:
			self.rssi = rssi
			self.new_data = True
	
	def set_ssid(self, ssid):
		if ssid != self.ssid:
			self.ssid = ssid
			self.new_data = True
	
	def set_channel(self, channel):
		if self.channel != channel:
			self.channel = str(ord(channel))
			self.new_data = True
	
	def set_known(self, known):
		if self.known != known:
			self.known = known
			self.new_data = True

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
			self.new_data = True
			self.security = security
	
	def set_wps(self, elem):
		self.new_data = True
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
		data = ">BHHBHHB"
		try:
			decoded = struct.unpack(data, elem.info[:11])
		except Exception as e:
			print(e.message)
			return None
		if len(decoded) < 6:
			return None
		self.wps = int(decoded[6]) == 0x2

	def add_beacon(self):
		self.new_data = True
		self.beacons += 1
		self.known = True

	def client_connected(self, bssid):
		if bssid not in self.client_co:
			self.new_data = True
			self.client_co.add(bssid)
			self.client_hist_co.append(bssid)

	def client_disconnected(self, bssid):
		self.new_data = True
		if bssid in self.client_co:
			self.client_co.remove(bssid)
		self.client_deco.append(bssid)

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
