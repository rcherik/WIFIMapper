#! /usr/bin/python
# -*- coding: utf-8 -*-

from wifi_mapper_utilities import is_multicast, is_retransmitted
from wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_HANDSHAKES, WM_VENDOR
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

	def __init__(self, dic, station):
		self.station = station
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

	def add_rssi(self, signal):
		if not isinstance(signal, int):
			return
		if self.first or signal > self.max_sig:
			self.max_sig = signal
		if self.first or signal < self.min_sig:
			self.min_sig = signal
		self.first = False
		self.avg_sig = self.avg_sig\
				+ ((signal - self.avg_sig) / (self.n + 1))
		self.sigs += signal
		self.n += 1

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
		if not isinstance(addr, str):
			return
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
		if not isinstance(addr, str):
			return
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
	handshakes = {}

	def __init__(self, dic, bssid, ap_bssid, vendor=None):
		self.bssid = bssid
		self.dic = dic
		self.probe = set()
		self.ap_bssid = ap_bssid
		if ap_bssid:
			self.dic[WM_AP][ap_bssid].client_connected(bssid)
		self.connected = True if ap_bssid else False
		Station.id += 1
		self.id = Station.id
		self.eapol = {}
		self.steps_done = 0
		self.success_hs = 0
		self.new_data = True
		self.vendor = vendor.get(bssid[:8].upper(), "") if vendor else None

	def update(self, ap_bssid):
		self.ap_bssid = ap_bssid
		self.connected = True if ap_bssid else False
		self.new_data = True

	def __getitem__(self, key):
		return self.__dict__[key]

	def get_eapol_key(self, ap_bssid, key):
		if ap_bssid in self.eapol and key in self.eapol[ap_bssid]:
			return self.eapol[ap_bssid][key]
		return ""

	def has_success_hdshake(self, ap_bssid):
		if ap_bssid in self.eapol and "success" in self.eapol[ap_bssid] and\
			self.eapol[ap_bssid]["success"] > 0:
			return True
		return False

	def prepare_eapol_dict(self, ap_bssid):
		self.eapol[ap_bssid] = {
			"steps_done": 0,
			"success": 0,
			"fail": 0,
			"exited": 0,
			"kicked": 0,
			"auth": 0,
			"auth_resp": 0,
			"deauth": 0,
			"assos": 0,
			"reassos": 0,
			"assos_resp": 0,
			"reassos_resp": 0,
			"disasos": 0,
			"hdshake_pkt": [],
			"last_success": 0,
			"current_step": None,
		}

	def add_ap_exit(self, ap_bssid, type, exited):
		"""
			:param ap_bssid: access point mac addr
			:param type: "deauth" or disasos"
			:param exited: bool
		"""
		if ap_bssid not in self.eapol:
			self.prepare_eapol_dict(ap_bssid)
		ea = self.eapol[ap_bssid]
		if ea['current_step'] in\
			("step1", "step2", "step3"):
			ea["fail"] += 1
			ea["current_step"] = None
			ea['hdshake_pkt'] = ea['hdshake_pkt'][:ea['last_success']]
		ea["current_step"] = type
		ea[type] += 1
		if exited:
			ea["exited"] += 1
		else:
			ea["kicked"] += 1
		if ap_bssid == self.ap_bssid:
			self.ap_bssid = None
			self.dic[WM_AP][ap_bssid].client_disconnected(self.bssid)
			self.connected = False
			self.new_data = True

	def add_pre_eapol(self, ap_bssid, type):
		"""
			:param ap_bssid: str access point mac addr
			:param type: "auth", "assos", "reassos", "reassos_resp"
				"auth_resp", "assos_resp"
		"""
		if ap_bssid not in self.eapol:
			self.prepare_eapol_dict(ap_bssid)
		ea = self.eapol[ap_bssid]
		ea[type] += 1
		ea["current_step"] = type

	def add_global_handshake(self, ap_bssid):
		#Usefull to get all handshakes download
		if self.bssid not in Station.handshakes:
			Station.handshakes[self.bssid] = set()
		Station.handshakes[self.bssid].add(ap_bssid)

	def add_eapol(self, packet, ap_bssid, step):
		"""
			:param packet: scapy packet with EAPOL layer
			:param ap_bssid: access point mac addr
			:param step: str in ("step1", "step2", "step3", "step4")
		"""
		if ap_bssid not in self.eapol:
			self.prepare_eapol_dict(ap_bssid)
		ea = self.eapol[ap_bssid]
		ea["current_step"] = step
		ea['hdshake_pkt'].append(packet)
		if not is_retransmitted(packet):
			self.steps_done += 1
			ea['steps_done'] += 1
		if step == "step4":
			if not is_retransmitted(packet):
				ea["success"] += 1
				self.success_hs += 1
				self.ap_bssid = ap_bssid
				self.dic[WM_AP][ap_bssid].client_connected(self.bssid)
				self.new_data = True
				self.add_global_handshake(ap_bssid)
			ea['last_success'] = len(ea['hdshake_pkt'])

	def add_probe(self, name):
		if len(name) == 0:
			return
		if not isinstance(name, unicode):
			try:
				uni = unicode(name, 'utf-8')
				self.probe.add(uni)
			except UnicodeDecodeError:
				return
		else:
			self.probe.add(name)

	def get_probes(self):
		return ', '.join(self.probe)

"""
	Present in main dictionnary in dic['AP'][some_bssid_key]
"""
class AccessPoint():

	def __init__(self, dic, bssid, ssid=None, channel=None,
			crypto=None, seen=None, vendor=None, wps=None):
		self.bssid = bssid
		self.ssid = ssid
		self.channel = set([channel]) if channel else set()
		self.crypto = crypto
		self.beacons = 0
		self.proberesp = 0
		self.known = False
		self.seen = set([seen]) if seen else set()
		self.new_data = True
		self.vendor = vendor.get(bssid[:8].upper(), "") if vendor else None
		self.dic = dic
		self.client_co = set()
		self.client_hist_co = []
		self.client_deco = []
		self.wps = wps

	def add_beacon(self):
		self.new_data = True
		self.beacons += 1
		self.known = True

	def add_proberesp(self):
		self.new_data = True
		self.proberesp += 1
		self.known = True

	def client_connected(self, bssid):
		self.client_co.add(bssid)
		self.client_hist_co.append(bssid)
		self.new_data = True

	def client_disconnected(self, bssid):
		if bssid in self.client_co:
			self.client_co.remove(bssid)
		self.client_deco.append(bssid)
		self.new_data = True

	def is_known(self):
		if self.beacons or self.proberesp:
			return True
		return self.known

	def __getitem__(self, key):
		return self.__dict__[key]

	def update(self, frame=None, ssid=None, channel=None,
			crypto=None, wps=None):
		#Adds a layer where AP has been seen
		if frame and frame not in self.seen:
			self.seen.add(frame)
			self.new_data = True
		if ssid and self.ssid is None:
			self.new_data = True
			self.ssid = ssid
		if channel and channel not in self.channel:
			self.new_data = True
			self.channel.add(channel)
		if crypto and (self.crypto is None\
				or len(self.crypto) < len(crypto)):
			self.new_data = True
			self.crypto = crypto
		if wps and self.wps is None:
			self.new_data = True
			self.wps = wps

	def get_seen(self):
		#Used in web interface to get reasons why AP is in table
		if len(self.seen) == 0:
			return ""
		s = ', '.join(self.seen)
		s = "seen: {}".format(s)
		if self.ssid is not None and len(self.ssid) > 0:
			s = "{} (probed: {})".format(s, self.ssid)
		return s

	def is_full(self):
		#Return true or false if all important infos are set
		if self.ssid is not None and\
			self.channel is not None and\
			self.crypto is not None:
			return True
		return False

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
