#! /usr/bin/python
# -*- coding: utf-8 -*-

from wifi_mapper_utilities import is_multicast, is_retransmitted

"""
	Classes used in dictionnary from pcap_paser.parse method
"""

"""
	Present in main dictionnary in dic['Traffic'][some_station_key]
	Used only to get station traffic
"""
class Traffic():

	def __init__(self, station):
		self.station = station
		self.sent = 0
		self.recv = 0
		self.max_sig = 0
		self.avg_sig = 0
		self.min_sig = 0
		self.first = True
		self.sigs = 0
		self.n = 0
		self.traffic = {}

	def add_rssi(self, signal):
		if not isinstance(signal, int):
			return
		if self.first or signal > self.max_sig:
			self.max_sig = signal
		if self.first or signal < self.min_sig:
			self.min_sig = signal
		self.first = False
		self.n += 1
		self.sigs += signal

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
			return 0
		return self.sigs / self.n

"""
	Present in main dictionnary in dic['Station'][some_macaddr_key]
"""
class Station():

	id = 0
	handshakes = {}

	def __init__(self, station, bssid):
		self.station = station
		self.probe = set()
		self.bssid = bssid if not is_multicast(bssid) else None
		Station.id += 1
		self.id = Station.id
		self.eapol = {}
		self.steps_done = 0
		self.success_hs = 0

	def get_eapol_key(self, bssid, key):
		if bssid in self.eapol and key in self.eapol[bssid]:
			return self.eapol[bssid][key]
		return ""

	def has_success_hdshake(self, bssid):
		if bssid in self.eapol and "success" in self.eapol[bssid] and\
			self.eapol[bssid]["success"] > 0:
			return True
		return False

	def prepare_eapol_dict(self, bssid):
		self.eapol[bssid] = {
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

	def add_ap_exit(self, bssid, type, exited):
		"""
			:param bssid: access point mac addr
			:param type: "deauth" or disasos"
			:param exited: bool
		"""
		if bssid not in self.eapol:
			self.prepare_eapol_dict(bssid)
		ea = self.eapol[bssid]
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
		if bssid == self.bssid:
			self.bssid = None

	def add_pre_eapol(self, bssid, type):
		"""
			:param bssid: str access point mac addr
			:param type: "auth", "assos", "reassos", "reassos_resp"
				"auth_resp", "assos_resp"
		"""
		if bssid not in self.eapol:
			self.prepare_eapol_dict(bssid)
		ea = self.eapol[bssid]
		ea[type] += 1
		ea["current_step"] = type

	def add_global_handshake(self, bssid):
		#Usefull to get all handshakes download
		if self.station not in Station.handshakes:
			Station.handshakes[self.station] = set()
		Station.handshakes[self.station].add(bssid)

	def add_eapol(self, packet, bssid, step):
		"""
			:param packet: scapy packet with EAPOL layer
			:param bssid: access point mac addr
			:param step: str in ("step1", "step2", "step3", "step4")
		"""
		if bssid not in self.eapol:
			self.prepare_eapol_dict(bssid)
		ea = self.eapol[bssid]
		ea["current_step"] = step
		ea['hdshake_pkt'].append(packet)
		if not is_retransmitted(packet):
			self.steps_done += 1
			ea['steps_done'] += 1
		if step == "step4":
			if not is_retransmitted(packet):
				ea["success"] += 1
				self.success_hs += 1
				self.bssid = bssid
				self.add_global_handshake(bssid)
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
	def __init__(self, bssid, ssid=None, channel=None, crypto=None, seen=None):
		self.bssid = bssid
		self.ssid = ssid
		self.channel = channel
		self.crypto = crypto
		self.beacons = 0
		self.proberesp = 0
		self.seen = set()
		if seen is not None:
			self.seen.add(seen)

	def is_known(self):
		"""
			Consider is known only if there was beacons or proberesp
			Used in web interface to get red table rows
		"""
		if self.beacons or self.proberesp:
			return True
		return False

	def add_seen(self, seen):
		#Adds a layer where AP has been seen
		self.seen.add(seen)

	def get_seen(self):
		#Used in web interface to get reasons why AP is in table
		if len(self.seen) == 0:
			return "Error"
		s = ', '.join(self.seen)
		s = "Seen: {}".format(s)
		if self.ssid is not None and len(self.ssid) > 0:
			s = "{} (probed: {})".format(s, self.ssid)
		return s

	def check_infos(self, ssid, channel, crypto):
		#Might get some more infos in beacons
		if self.ssid is None:
			self.ssid = ssid
		if self.channel is None:
			self.channel = channel
		if self.crypto is None:
			self.crypto = crypto
	
	def is_full(self):
		#Return true or false if all important infos are set
		if self.ssid is not None and\
			self.channel is not None and\
			self.crypto is not None:
			return True
		return False

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
