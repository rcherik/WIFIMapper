#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
#Import logging to silence scapy IPV6 error
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import rdpcap, DNSRR, RadioTap, Dot11,Dot11FCS, Dot11Elt, Dot11Beacon, Dot11ProbeResp, Dot11ProbeReq, Raw, EAPOL, Dot11AssoReq, Dot11ReassoReq, Dot11AssoResp, Dot11ReassoResp, Dot11Disas, Dot11Deauth, Dot11Auth, wrpcap
from scapy.error import Scapy_Exception
import wpa_scapy
import rssi_scapy
import wifi_mapper_ds
from wifi_mapper_classes import AccessPoint, Station, Traffic
from wifi_mapper_utilities import is_multicast, is_retransmitted, is_control, is_data
import time

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
			sta = dic['Station'][station].add_probe(elem.info)
		elem = elem.payload

def check_for_handshakes(dic):
	"""
		:return: all successful handshakes
		:rtype: int
	"""
	n = 0
	for key, value in Station.handshakes.iteritems():
		if key in dic['Station']:
			for bssid in value:
				n += dic['Station'][key].eapol[bssid]['success']
	return n

def get_handshake_pcap(dic, station, bssid, name):
	"""
		Write pcap of handshakes between station and ap
		:return: True if wrote a file
		:rtype: bool
	"""
	if station not in dic['Station'] or\
		bssid not in dic['Station'][station].eapol or\
		dic['Station'][station].eapol[bssid]['success'] == 0:
		return False
	packets = dic['Station'][station].get_eapol_key(bssid, "hdshake_pkt")
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
	if station not in dic['Station']:
		return False
	packets = []
	ret = False
	for key, value in dic['Station'][station].eapol.iteritems():
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
		if key in dic['Station']:
			for bssid in value:
				if dic['Station'][key].eapol[bssid]['success'] > 0:
					ret = True
					pkt = dic['Station'][key].eapol[bssid]['hdshake_pkt']
					packets += pkt
	if ret:
		wrpcap(name, packets)
	return ret

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
		if addr not in dic['Traffic']:
			dic['Traffic'][addr] = Traffic(addr)
		dic['Traffic'][addr].add_sent(to_addr, which)

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
		if addr not in dic['Traffic']:
			dic['Traffic'][addr] = Traffic(addr)
		dic['Traffic'][addr].add_recv(from_addr, which)

def add_station(dic, station, bssid):
	"""
		Adds station in Station key from parse() dictionnary

		:param dic: dict from parse()
		:param station: str mac addr
		:param bssid: str mac addr
		::seealso:: parse()
	"""
	if not is_multicast(station) and isinstance(station, str):
		if is_multicast(bssid):
			bssid = None
		if station not in dic['Station']:
			dic['Station'][station] = Station(station, bssid)
		elif bssid is not None and dic['Station'][station].bssid is None:
			dic['Station'][station].bssid = bssid

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
		if addr not in dic['Traffic']:
			dic['Traffic'][addr] = Traffic(addr)
		traffic = dic['Traffic'][addr]
		traffic.add_rssi(rssi)

def get_ap_infos(packet, dic):
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
	if bssid in dic['AP'] and dic['AP'][bssid].is_full():
		if packet.haslayer(Dot11Beacon):
			dic['AP'][bssid].beacons += 1
		else:
			dic['AP'][bssid].proberesp += 1
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
	if bssid not in dic['AP']:
		ap = AccessPoint(bssid, ssid, channel, '/'.join(crypto))
		if packet.haslayer(Dot11Beacon):
			ap.beacons += 1
		else:
			ap.proberesp += 1
		dic['AP'][bssid] = ap 
	else:
		ap = dic['AP'][bssid].check_infos(ssid, channel, '/'.join(crypto))

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
	if wpa_step1(key):
		step = "step1"
		add_traffic_sent(dic, station, to_addr=bssid)
		add_rssi(rssi_scapy.get_rssi(packet), dic, station)
	if wpa_step2(key):
		step = "step2"
		add_traffic_recv(dic, bssid, from_addr=station)
	if wpa_step3(key):
		step = "step3"
		add_traffic_sent(dic, station, to_addr=bssid)
		add_rssi(rssi_scapy.get_rssi(packet), dic, station)
	if wpa_step4(key):
		step = "step4"
		add_traffic_recv(dic, bssid, from_addr=station)
	dic['Station'][station].add_eapol(packet, bssid, step)

def add_ap(dic, bssid, seen):
	"""
		Adds an access point out of beacon/probeRes layers

		:param seen: str, seen from which layer, used in web interface
	"""
	if not is_multicast(bssid):
		if bssid not in dic['AP']:
			dic['AP'][bssid] = AccessPoint(bssid, seen=seen)
		else:
			dic['AP'][bssid].add_seen(seen)

def get_station_infos(packet, dic):
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
	if ds["from"] and ds["to"]:
		return

	# Control packets are unreliable to get station, just add traffic and rssi
	if is_control(packet):
		if ds["sent"] is True:
			add_traffic_sent(dic, ds["station"], to_addr=ds["dst"], which="control")
		else:
			add_traffic_recv(dic, ds["station"], from_addr=ds["src"], which="control")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["station"])
		return

	if packet.haslayer(Dot11ProbeResp):
		#Station receive probe response
		add_station(dic, ds["dst"], None)
		add_traffic_recv(dic, ds["dst"], from_addr=ds["src"], which="probe")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["dst"])
	elif packet.haslayer(Dot11ProbeReq):
		#Station request information
		add_station(dic, ds["src"], None)
		add_traffic_sent(dic, ds["src"], to_addr=None, which="probeReq")
		get_client_probe(packet, dic, ds["src"])
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["src"])
	elif packet.haslayer(Dot11Auth):
		#Authentication could be from or to station
		add_station(dic, ds["station"], None)
		if ds["sent"]:
			add_traffic_sent(dic, ds["station"], to_addr=ds["dst"], which="Auth")
			add_ap(dic, ds["dst"], seen="Auth")
			dic['Station'][ds["station"]].add_pre_eapol(ds["dst"], "auth")
		else:
			add_traffic_recv(dic, ds["station"], from_addr=ds["src"], which="Auth")
			add_ap(dic, ds["src"], seen="AuthResp")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["station"])
	elif packet.haslayer(Dot11AssoReq):
		#Station request association
		add_station(dic, ds["src"], None)
		add_ap(dic, ds["dst"], seen="AssociationReq")
		add_traffic_sent(dic, ds["src"], to_addr=ds["dst"], which="Association")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["src"])
		dic['Station'][ds["src"]].add_pre_eapol(ds["dst"], "assos") 
	elif packet.haslayer(Dot11ReassoReq):
		#Station request Reassociation
		add_station(dic, ds["src"], None)
		add_ap(dic, ds["dst"], seen="ReassociationReq")
		add_traffic_sent(dic, ds["src"], to_addr=ds["dst"], which="Reassociation")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["src"])
		dic['Station'][ds["src"]].add_pre_eapol(ds["dst"], "reassos") 
	elif packet.haslayer(Dot11AssoResp):
		#Station receive association response
		add_station(dic, ds["dst"], None)
		add_ap(dic, ds["src"], seen="AssociationResp")
		add_traffic_recv(dic, ds["dst"], from_addr=ds["src"], which="Association")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["dst"])
		dic['Station'][ds["dst"]].add_pre_eapol(ds["src"], "assos_resp") 
	elif packet.haslayer(Dot11ReassoResp):
		#Station receive Reassociation response
		add_station(dic, ds["dst"], None)
		add_ap(dic, ds["src"], seen="ReassociationResp")
		add_traffic_recv(dic, ds["dst"], from_addr=ds["src"], which="Reassociation")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["dst"])
		dic['Station'][ds["dst"]].add_pre_eapol(ds["src"], "reassos_resp") 
	elif packet.haslayer(EAPOL):
		#Wpa handhsake between station and access point
		add_station(dic, ds["station"], None)
		add_ap(dic, ds["bssid"], seen="Handshake")
		add_handshake(packet, dic, ds["station"], ds["bssid"])
	elif packet.haslayer(Dot11Disas):
		#Disassociation could be from or to station
		add_station(dic, ds["station"], ds["bssid"])
		if ds["sent"]:
			add_ap(dic, ds["dst"], seen="DisassoSent")
			add_traffic_sent(dic, ds["station"], to_addr=ds["dst"], which="Disasso")
		else:
			add_ap(dic, ds["src"], seen="DisassoRecv")
			add_traffic_recv(dic, ds["station"], from_addr=ds["src"], which="Disasso")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["station"])
		dic['Station'][ds["station"]].add_ap_exit(ds["bssid"], "disasos", exited=ds["sent"])
	elif packet.haslayer(Dot11Deauth):
		#Deauthentification could be from or to station
		add_station(dic, ds["station"], ds["bssid"])
		if ds["sent"]:
			add_ap(dic, ds["dst"], seen="DeauthSent")
			add_traffic_sent(dic, ds["station"], to_addr=ds["dst"], which="Deauth")
		else:
			add_ap(dic, ds["src"], seen="DeauthRecv")
			add_traffic_recv(dic, ds["station"], from_addr=ds["src"], which="Deauth")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["station"])
		dic['Station'][ds["station"]].add_ap_exit(ds["bssid"], "deauth", exited=ds["sent"])
	elif is_data(packet) and not is_multicast(ds["dst"]):
		#Data could be from or to station
		add_station(dic, ds["station"], ds["bssid"])
		if ds["sent"]:
			add_ap(dic, ds["dst"], seen="DataSent")
			add_traffic_sent(dic, ds["station"], to_addr=ds["dst"], which="data")
		else:
			add_ap(dic, ds["src"], seen="DataRecv")
			add_traffic_recv(dic, ds["station"], from_addr=ds["src"], which="data")
		add_rssi(rssi_scapy.get_rssi(packet), dic, ds["station"])

def get_packet_infos(packet, dic):
	"""
		Get access point info from beacon or probe response
			and get station infos from anything but beacon

		:param packet: scapy packet
		:param dic: dictionnary from parse function

		::seealso:: parse()
	"""
	if packet.haslayer(Dot11Beacon) or\
		packet.haslayer(Dot11ProbeResp):
		get_ap_infos(packet, dic)
	if not packet.haslayer(Dot11Beacon):
		get_station_infos(packet, dic)

def parse_pkt(dic, pkt):
	if pkt.haslayer(RadioTap):
		get_packet_infos(pkt, dic)
	else:
		return False
	dic['Handshakes'] = check_for_handshakes(dic)
	#Sometimes things like printer are both station and AP
	for key, value in dic['AP'].iteritems():
		if key in dic['Station']:
			dic['Station'].pop(key, None)
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
	dic = {'AP': {}, 'Station': {}, 'Traffic': {}}
	for packet in packets:
		if packet.haslayer(RadioTap):
			get_packet_infos(packet, dic)
	dic['Handshakes'] = check_for_handshakes(dic)
	#Sometimes things like printer are both station and AP
	for key, value in dic['AP'].iteritems():
		if key in dic['Station']:
			dic['Station'].pop(key, None)
	print("Parsed in {0:.3f} seconds".format(time.time() - read_time))
	return dic

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
