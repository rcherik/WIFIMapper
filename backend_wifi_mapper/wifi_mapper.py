#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
#Import logging to silence scapy IPV6 error
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import rdpcap, DNSRR, RadioTap, Dot11, Dot11Elt, Dot11Beacon,\
		Dot11ProbeResp, Dot11ProbeReq, Raw, EAPOL, Dot11AssoReq,\
		Dot11ReassoReq, Dot11AssoResp, Dot11ReassoResp, Dot11Disas,\
		Dot11Deauth, Dot11Auth, wrpcap
try:
	from scapy.all import Dot11FCS
except ImportError:
	Dot11FCS = None

from scapy.error import Scapy_Exception
import wpa_scapy
import rssi_scapy
import wifi_mapper_ds
from wifi_mapper_ds import WM_DS_SRC, WM_DS_TRANS, WM_DS_RCV, WM_DS_DST,\
		WM_DS_BSSID, WM_DS_STATION, WM_DS_SENT, WM_DS_FROM, WM_DS_TO
from wifi_mapper_classes import AccessPoint, Station, Traffic,\
		WM_TRA_SENT, WM_TRA_RECV,\
		WM_TRA_ALL, WM_TRA_MNG, WM_TRA_CTRL, WM_TRA_DATA
from wifi_mapper_utilities import is_multicast, is_retransmitted, is_control, is_data
import time

#Macro for fields
WM_AP = 0
WM_STA = WM_STATION = 1
WM_TRA = WM_TRAFFIC = 2
WM_HDSHK = WM_HANDSHAKES = 3
WM_VENDOR = 4

#Macro for ID field in Dot11Elt
ID_SSID = 0
ID_DS = 3  #Direct Spectrum/Channel
ID_RSN = 48  #Robust Security Network/WPA2
ID_VENDOR = 221  #potentially WPA

def get_broadcast(addr):
	"""
		Sent to web interface to visualise broadcast in client detail

		:param addr: str mac addr
		:return: addr if it is not broadcast else return broadcast + addr
		:rtype: str

	"""
	if is_multicast(addr):
		return "< %s - Broadcast >" % addr
	return addr

def get_client_probe(packet, dic, station):
	"""
		Get device specific probes

		Parse Dot11 elements from probe request to retrieve ssid probes
	"""
	if not packet.haslayer(Dot11Elt):
		return
	elem = packet[Dot11Elt]
	while isinstance(elem, Dot11Elt):
		if elem.ID == ID_SSID:
			sta = dic[WM_STATION][station].add_probe(elem.info)
		elem = elem.payload

def check_for_handshakes(dic):
	"""
		:return: all successful handshakes
		:rtype: int
	"""
	n = 0
	for key, value in Station.handshakes.iteritems():
		if key in dic[WM_STATION]:
			for bssid in value:
				n += dic[WM_STATION][key].eapol[bssid]['success']
	return n

def get_handshake_pcap(dic, station, bssid, name):
	"""
		Write pcap of handshakes between station and ap
		:return: True if wrote a file
		:rtype: bool
	"""
	if station not in dic[WM_STATION] or\
		bssid not in dic[WM_STATION][station].eapol or\
		dic[WM_STATION][station].eapol[bssid]['success'] == 0:
		return False
	packets = dic[WM_STATION][station].get_eapol_key(bssid, "hdshake_pkt")
	if packets is None or len(packets) == 0:
		return False
	wrpcap(name, packets)
	return True

def get_station_handshake_pcap(dic, station, name):
	"""
		Write pcap of a station's handshakes
		:return: True if wrote a file
		:rtype: bool
	"""
	if station not in dic[WM_STATION]:
		return False
	packets = []
	ret = False
	for key, value in dic[WM_STATION][station].eapol.iteritems():
		if value['success'] > 0:
			ret = True
			pkt = value['hdshake_pkt']
			packets += pkt
	if ret:
		wrpcap(name, packets)
	return ret

def get_all_handshake_pcap(dic, name):
	"""
		Write pcap of a file's handshakes
		:return: True if wrote a file
		:rtype: bool
	"""
	packets = []
	ret = False
	for key, value in Station.handshakes.iteritems():
		if key in dic[WM_STATION]:
			for bssid in value:
				if dic[WM_STATION][key].eapol[bssid]['success'] > 0:
					ret = True
					pkt = dic[WM_STATION][key].eapol[bssid]['hdshake_pkt']
					packets += pkt
	if ret:
		wrpcap(name, packets)
	return ret

def add_traffic(dic, addr):
	if not is_multicast(addr) and isinstance(addr, str):
		if addr not in dic[WM_TRA]:
			dic[WM_TRA][addr] = Traffic(addr)

def add_traffic_sent(dic, addr, to_addr=None, which=None):
	"""
		Adds sent to addr in Traffic key from parse() dictionnary

		:param dic: dict from parse()
		:param addr: str mac addr
		:param to_addr: str mac addr
		::seealso:: parse()
	"""

	if is_multicast(to_addr) and which == "control":
		return
	if not is_multicast(addr) and isinstance(addr, str):
		if addr not in dic[WM_TRA]:
			dic[WM_TRA][addr] = Traffic(addr)
		dic[WM_TRA][addr].add_sent(to_addr, which)

def add_traffic_recv(dic, addr, from_addr=None, which=None):
	"""
		Adds recv to addr in Traffic key from parse() dictionnary

		:param dic: dict from parse()
		:param addr: str mac addr
		:param from_addr: str mac addr
		::seealso:: parse()
	"""
	if is_multicast(from_addr) and which == "control":
		return
	if not is_multicast(addr) and isinstance(addr, str):
		if addr not in dic[WM_TRA]:
			dic[WM_TRA][addr] = Traffic(addr)
		dic[WM_TRA][addr].add_recv(from_addr, which)

def add_station(dic, bssid, ap_bssid):
	"""
		Adds bssid in Station key from parse() dictionnary

		:param dic: dict from parse()
		:param bssid: str mac addr
		:param ap_bssid: str mac addr
		::seealso:: parse()
	"""
	if not is_multicast(bssid) and isinstance(bssid, str):
		if is_multicast(ap_bssid):
			ap_bssid = None
		if bssid not in dic[WM_STATION]:
			dic[WM_STATION][bssid] = Station(bssid, ap_bssid, vendor=dic[WM_VENDOR])
			add_traffic(dic, bssid)
		elif ap_bssid is not None and dic[WM_STATION][bssid].ap_bssid is None:
			dic[WM_STATION][bssid].update(ap_bssid)

def add_rssi(rssi, dic, addr):
	"""
		Adds rssi value to address in Traffic key from parse() dictionnary

		:param rssi: int
		:param dic: dict from parse()
		:param addr: str mac addr
		::seealso:: parse()
	"""
	if rssi is not None and not is_multicast(addr) and\
		isinstance(addr, str):
		if addr not in dic[WM_TRA]:
			dic[WM_TRA][addr] = Traffic(addr)
		traffic = dic[WM_TRA][addr]
		traffic.add_rssi(rssi)

def get_ap_infos(packet, dic, channel=None):
	"""
		Get infos of access point in a beacon or probe response

		Parse Dot11 elements from packet and capabilities to get
			used privacy settings, ssid and channel

		:param packet: scapy packet
		:param dic: dict from parse()
		::seealso:: parse()
	"""
	layer = Dot11 if packet.haslayer(Dot11) else Dot11FCS
	bssid = packet[layer].addr3
	if is_multicast(bssid):
		return
	if bssid in dic[WM_AP]:
		if packet.haslayer(Dot11Beacon):
			dic[WM_AP][bssid].add_beacon()
		else:
			dic[WM_AP][bssid].add_proberesp()
		return
	elem = packet[Dot11Elt]
	capabilities = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
						"{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
	ssid, channel = None, None
	crypto = set()
	while isinstance(elem, Dot11Elt):
		#Some encoding errors there
		if elem.ID == ID_SSID:
			try:
				ssid = unicode(elem.info, 'utf-8')
			except UnicodeDecodeError:
				ssid = ""
		elif elem.ID == ID_DS and len(elem.info) == 1:
			#elem.info not always a char
			channel = ord(elem.info)
		elif elem.ID == ID_RSN:
			crypto.add("WPA2")
		elif elem.ID == ID_VENDOR and hasattr(elem, "info") and\
			elem.info.startswith('\x00P\xf2\x01\x01\x00'):
			crypto.add("WPA")
		elem = elem.payload
	if not crypto:
		if 'privacy' in capabilities:
			crypto.add("WEP")
		else:
			crypto.add("OPN")
	if bssid not in dic[WM_AP]:
		ap = AccessPoint(bssid, ssid, channel, '/'.join(crypto), vendor=dic[WM_VENDOR])
		add_traffic(dic, bssid)
		if packet.haslayer(Dot11Beacon):
			ap.add_beacon()
		else:
			ap.add_proberesp()
		dic[WM_AP][bssid] = ap 
	else:
		ap = dic[WM_AP][bssid].check_infos(ssid, channel, '/'.join(crypto))

#Macro for EAPOL flags
EAPOL_KEY_TYPE = 1 << 3
EAPOL_INSTALL = 1 << 6
EAPOL_KEY_ACK = 1 << 7
EAPOL_KEY_MIC = 1 << 8
EAPOL_SECURE = 1 << 9
EAPOL_ERROR = 1 << 10
EAPOL_REQUEST = 1 << 11
EAPOL_ENCRYPTED = 1 << 12

def wpa_step1(key):
	if key.key_info & EAPOL_KEY_ACK and\
		not key.key_info & EAPOL_KEY_MIC:
		return True
	return False

def wpa_step2(key):
	if key.key_info & EAPOL_KEY_MIC and\
		not key.key_info & EAPOL_SECURE:
		return True
	return False

def wpa_step3(key):
	if key.key_info & EAPOL_KEY_ACK and\
		key.key_info & EAPOL_KEY_MIC and\
		key.key_info & EAPOL_SECURE and\
		key.key_info & EAPOL_INSTALL and\
		key.key_info & EAPOL_ENCRYPTED:
		return True
	return False

def wpa_step4(key):
	if key.key_info & EAPOL_KEY_MIC and\
		key.key_info & EAPOL_SECURE and\
		not key.key_info & EAPOL_ENCRYPTED:
		return True
	return False

def add_handshake(packet, dic, station, bssid):
	key = packet[EAPOL]
	step = None
	rssi = rssi_scapy.get_rssi(packet)
	if wpa_step1(key):
		step = "step1"
		add_traffic_sent(dic, station, to_addr=bssid)
		add_rssi(rssi, dic, station)
	if wpa_step2(key):
		step = "step2"
		add_traffic_recv(dic, bssid, from_addr=station)
	if wpa_step3(key):
		step = "step3"
		add_traffic_sent(dic, station, to_addr=bssid)
		add_rssi(rssi, dic, station)
	if wpa_step4(key):
		step = "step4"
		add_traffic_recv(dic, bssid, from_addr=station)
	dic[WM_STATION][station].add_eapol(packet, bssid, step)

def add_ap(dic, bssid, seen):
	"""
		Adds an access point out of beacon/probeRes layers

		:param seen: str, seen from which layer, used in web interface
	"""
	if not is_multicast(bssid):
		if bssid not in dic[WM_AP]:
			dic[WM_AP][bssid] = AccessPoint(bssid, seen=seen, vendor=dic[WM_VENDOR])
			add_traffic(dic, bssid)
		else:
			dic[WM_AP][bssid].update(seen)

def get_station_infos(packet, dic, channel=None):
	"""
		Parse the packet from its layers type
			add station and access point thanks to from-DS to-DS

		Handles traffic, rssi, handshakes, all stations and some ap

		:param packet: scapy packet
		:param dic: dictionnary from parse()

		::seealso:: parse()
	"""

	ds = wifi_mapper_ds.get_addrs(packet)

	# Packets from AP to AP do not concern stations
	if ds[WM_DS_FROM] and ds[WM_DS_TO]:
		return

	rssi = rssi_scapy.get_rssi(packet)
	# Control packets are unreliable to get station, just add traffic and rssi
	if is_control(packet):
		if ds[WM_DS_SENT] is True:
			add_traffic_sent(dic, ds[WM_DS_STATION], to_addr=ds[WM_DS_DST],
					which="control")
		else:
			add_traffic_recv(dic, ds[WM_DS_STATION], from_addr=ds[WM_DS_SRC],
					which="control")
		add_rssi(rssi, dic, ds[WM_DS_STATION])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
		return

	if packet.haslayer(Dot11ProbeResp):
		#Station receive probe response
		add_station(dic, ds[WM_DS_DST], None)
		add_traffic_recv(dic, ds[WM_DS_DST], from_addr=ds[WM_DS_SRC],
				which="probe")
		add_rssi(rssi, dic, ds[WM_DS_DST])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
	elif packet.haslayer(Dot11ProbeReq):
		#Station request information
		add_station(dic, ds[WM_DS_SRC], None)
		add_traffic_sent(dic, ds[WM_DS_SRC], to_addr=None,
				which="probeReq")
		get_client_probe(packet, dic, ds[WM_DS_SRC])
		add_rssi(rssi, dic, ds[WM_DS_SRC])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
	elif packet.haslayer(Dot11Auth):
		#Authentication could be from or to station
		add_station(dic, ds[WM_DS_STATION], None)
		if ds[WM_DS_SENT]:
			add_traffic_sent(dic, ds[WM_DS_STATION], to_addr=ds[WM_DS_DST],
					which="Auth")
			add_ap(dic, ds[WM_DS_DST], seen="Auth")
			dic[WM_STATION][ds[WM_DS_STATION]].\
					add_pre_eapol(ds[WM_DS_DST], "auth")
		else:
			add_traffic_recv(dic, ds[WM_DS_STATION], from_addr=ds[WM_DS_SRC],\
					which="Auth")
			add_ap(dic, ds[WM_DS_SRC], seen="AuthResp")
		add_rssi(rssi, dic, ds[WM_DS_STATION])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
	elif packet.haslayer(Dot11AssoReq):
		#Station request association
		add_station(dic, ds[WM_DS_SRC], None)
		add_ap(dic, ds[WM_DS_DST], seen="AssociationReq")
		add_traffic_sent(dic, ds[WM_DS_SRC], to_addr=ds[WM_DS_DST],\
				which="Association")
		add_rssi(rssi, dic, ds[WM_DS_SRC])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
		dic[WM_STATION][ds[WM_DS_SRC]].add_pre_eapol(ds[WM_DS_DST], "assos")
	elif packet.haslayer(Dot11ReassoReq):
		#Station request Reassociation
		add_station(dic, ds[WM_DS_SRC], None)
		add_ap(dic, ds[WM_DS_DST], seen="ReassociationReq")
		add_traffic_sent(dic, ds[WM_DS_SRC], to_addr=ds[WM_DS_DST],\
				which="Reassociation")
		add_rssi(rssi, dic, ds[WM_DS_SRC])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
		dic[WM_STATION][ds[WM_DS_SRC]].add_pre_eapol(ds[WM_DS_DST], "reassos") 
	elif packet.haslayer(Dot11AssoResp):
		#Station receive association response
		add_station(dic, ds[WM_DS_DST], None)
		add_ap(dic, ds[WM_DS_SRC], seen="AssociationResp")
		add_traffic_recv(dic, ds[WM_DS_DST], from_addr=ds[WM_DS_SRC],\
				which="Association")
		add_rssi(rssi, dic, ds[WM_DS_DST])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
		dic[WM_STATION][ds[WM_DS_DST]].\
				add_pre_eapol(ds[WM_DS_SRC], "assos_resp") 
	elif packet.haslayer(Dot11ReassoResp):
		#Station receive Reassociation response
		add_station(dic, ds[WM_DS_DST], None)
		add_ap(dic, ds[WM_DS_SRC], seen="ReassociationResp")
		add_traffic_recv(dic, ds[WM_DS_DST], from_addr=ds[WM_DS_SRC],\
				which="Reassociation")
		add_rssi(rssi, dic, ds[WM_DS_DST])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
		dic[WM_STATION][ds[WM_DS_DST]].\
				add_pre_eapol(ds[WM_DS_SRC], "reassos_resp") 
	elif packet.haslayer(EAPOL):
		#Wpa handhsake between station and access point
		add_station(dic, ds[WM_DS_STATION], None)
		add_ap(dic, ds[WM_DS_BSSID], seen="Handshake")
		add_handshake(packet, dic, ds[WM_DS_STATION], ds[WM_DS_BSSID])
	elif packet.haslayer(Dot11Disas):
		#Disassociation could be from or to station
		add_station(dic, ds[WM_DS_STATION], ds[WM_DS_BSSID])
		if ds[WM_DS_SENT]:
			add_ap(dic, ds[WM_DS_DST], seen="DisassoSent")
			add_traffic_sent(dic, ds[WM_DS_STATION], to_addr=ds[WM_DS_DST],\
					which="Disasso")
		else:
			add_ap(dic, ds[WM_DS_SRC], seen="DisassoRecv")
			add_traffic_recv(dic, ds[WM_DS_STATION], from_addr=ds[WM_DS_SRC],\
					which="Disasso")
		add_rssi(rssi, dic, ds[WM_DS_STATION])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
		dic[WM_STATION][ds[WM_DS_STATION]].\
				add_ap_exit(ds[WM_DS_BSSID], "disasos", exited=ds[WM_DS_SENT])
	elif packet.haslayer(Dot11Deauth):
		#Deauthentification could be from or to station
		add_station(dic, ds[WM_DS_STATION], ds[WM_DS_BSSID])
		if ds[WM_DS_SENT]:
			add_ap(dic, ds[WM_DS_DST], seen="DeauthSent")
			add_traffic_sent(dic, ds[WM_DS_STATION], to_addr=ds[WM_DS_DST],\
					which="Deauth")
		else:
			add_ap(dic, ds[WM_DS_SRC], seen="DeauthRecv")
			add_traffic_recv(dic, ds[WM_DS_STATION], from_addr=ds[WM_DS_SRC],\
					which="Deauth")
		add_rssi(rssi, dic, ds[WM_DS_STATION])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])
		dic[WM_STATION][ds[WM_DS_STATION]].\
				add_ap_exit(ds[WM_DS_BSSID], "deauth", exited=ds[WM_DS_SENT])
	elif is_data(packet) and not is_multicast(ds[WM_DS_DST]):
		#Data could be from or to station
		add_station(dic, ds[WM_DS_STATION], ds[WM_DS_BSSID])
		if ds[WM_DS_SENT]:
			add_ap(dic, ds[WM_DS_DST], seen="DataSent")
			add_traffic_sent(dic, ds[WM_DS_STATION], to_addr=ds[WM_DS_DST],\
					which="data")
		else:
			add_ap(dic, ds[WM_DS_SRC], seen="DataRecv")
			add_traffic_recv(dic, ds[WM_DS_STATION], from_addr=ds[WM_DS_SRC],\
					which="data")
		add_rssi(rssi, dic, ds[WM_DS_STATION])
		add_rssi(rssi, dic, ds[WM_DS_BSSID])

def get_packet_infos(packet, dic, channel=None):
	"""
		Get access point info from beacon or probe response
			and get station infos from anything but beacon

		:param packet: scapy packet
		:param dic: dictionnary from parse function

		::seealso:: parse()
	"""
	if packet.haslayer(Dot11Beacon) or\
		packet.haslayer(Dot11ProbeResp):
		get_ap_infos(packet, dic, channel=channel)
	if not packet.haslayer(Dot11Beacon):
		get_station_infos(packet, dic, channel=channel)

def parse_pkt(dic, pkt, channel=None):
	if pkt.haslayer(RadioTap):
		get_packet_infos(pkt, dic, channel=channel)
	else:
		return False
	dic[WM_HDSHK] = check_for_handshakes(dic)
	#Sometimes things like printer are both station and AP
	for key, value in dic[WM_AP].iteritems():
		if key in dic[WM_STATION]:
			dic[WM_STATION].pop(key, None)
	return True

def parse_file(name):
	"""
		Read a pcap file and parse its packet containing a RadioTap header

		:param name: a pcap file path
		:return: a dictionnary with keys: AP, Station, Traffic
			containing mac addresses keys giving access to AccessPoint, Station
			and Traffic class
		:rtype: dict

	"""
	print("Reading file {}".format(name))
	start_time = time.time()
	try:
		packets = rdpcap(name)
	except (IOError, Scapy_Exception) as err:
		print("Pcap parser error: {}".format(err),
			file=sys.stderr)
		return None
	#Scapy exception in a file of scapy is not included
	#when reading wrong pcap magic number in file
	except NameError as err:
		print("Pcap parser error: not a pcap file ({})".format(err),
			file=sys.stderr)
		return None
	#Prevents massive output when quitting while rdpcap reads
	except KeyboardInterrupt:
		sys.exit(1)
	read_time = time.time()
	print("Took {0:.3f} seconds".format(read_time - start_time))
	dic =[{}, {}, {}]
	for packet in packets:
		if packet.haslayer(RadioTap):
			get_packet_infos(packet, dic)
	dic[WM_HDSHK] = check_for_handshakes(dic)
	#Sometimes things like printer are both station and AP
	for key, value in dic[WM_AP].iteritems():
		if key in dic[WM_STATION]:
			dic[WM_STATION].pop(key, None)
	print("Parsed in {0:.3f} seconds".format(time.time() - read_time))
	return dic

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
