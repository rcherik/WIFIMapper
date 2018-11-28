#! /usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import struct
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
import wifi_mapper_ds
from wifi_mapper_ds import WM_DS_SRC, WM_DS_TRANS, WM_DS_RCV, WM_DS_DST,\
		WM_DS_AP, WM_DS_STATION, WM_DS_SENDER, WM_DS_RECEIVER
from wifi_mapper_classes import AccessPoint, Station, Traffic,\
		WM_TRA_SENT, WM_TRA_RECV,\
		WM_TRA_ALL, WM_TRA_MNG, WM_TRA_CTRL, WM_TRA_DATA
from wifi_mapper_utilities import is_broadcast, is_retransmitted, is_control, is_data,\
			WM_AP, WM_STATION, WM_TRA, WM_HDSHK, WM_VENDOR, WM_STA
import time

#Macro for ID field in Dot11Elt
ID_SSID = 0
ID_CHANNEL = 3  #Direct Spectrum/Channel
ID_RSN = 48  #Robust Security Network/WPA2
ID_VENDOR = 221  #potentially WPA

def get_broadcast(addr):
	"""
		Sent to web interface to visualise broadcast in client detail

		:param addr: str mac addr
		:return: addr if it is not broadcast else return broadcast + addr
		:rtype: str

	"""
	if is_broadcast(addr):
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

def add_traffic(dic, addr):
	if not is_broadcast(addr) and isinstance(addr, str):
		if addr not in dic[WM_TRA]:
			dic[WM_TRA][addr] = Traffic(dic, addr)


def add_ap(dic, bssid):
	"""
		Adds an access point out of beacon/probeRes layers

		:param seen: str, seen from which layer, used in web interface
	"""
	if not is_broadcast(bssid):
		if bssid not in dic[WM_AP]:
			dic[WM_AP][bssid] = AccessPoint(dic, bssid, oui_dict=dic[WM_VENDOR])
			return dic[WM_AP][bssid]
		else:
			return dic[WM_AP][bssid]
	else:
		return None

def add_station(dic, bssid):
	"""
		Adds bssid in Station key from parse() dictionnary

		:param dic: dict from parse()
		:param bssid: str mac addr
		::seealso:: parse()
	"""
	if not is_broadcast(bssid) and isinstance(bssid, str):
		if bssid not in dic[WM_STATION]:
			dic[WM_STATION][bssid] = Station(dic, bssid, oui_dict=dic[WM_VENDOR])
			return dic[WM_STATION][bssid]
	else:
		return None

def parse_beacon(pkt, dic, ap):
	elem = pkt[Dot11Elt]
	while isinstance(elem, Dot11Elt):
		if elem.ID == ID_SSID:
			ap.set_ssid(elem.info)
		elif elem.ID == ID_CHANNEL:
			ap.set_channel(elem.info)
		elif elem.ID == ID_VENDOR:
			if hasattr(elem, "oui") and elem.oui == 0x50f2 \
			and hasattr(elem, "info") and elem.info.startswith('\x04'):
				ap.set_wps(elem)
		elem = elem.payload
	ap.set_security(pkt)
	ap.set_known(True)
	ap.add_beacon()

def parse_probeReq(pkt, dic, sta, ap):
	elem = pkt[Dot11Elt]
	while isinstance(elem, Dot11Elt):
		#Get the SSID
		if elem.ID == ID_SSID:
			#SSID is not specified
			if elem.len == 0:
				pass
			else:
				sta.add_ap_probed(elem.info)
			break
		elem = elem.payload
	sta.set_probeReq(str(pkt[Dot11ProbeReq]).encode('hex'))

def parse_assocReq(pkt, dic, sta):
	sta.set_assocReq(str(pkt[Dot11AssoReq])[4:].encode('hex'))

def parse_reassocReq(pkt, dic, sta):
	sta.set_assocReq(str(pkt[Dot11ReassoReq])[4:].encode('hex'))

def parse_assocResp(pkt, dic, sta, ap):
	pass

def handle_traffic(pkt, dic, src, dst):
	#check if dst is not Broadcast
	if is_broadcast(dst) is False:
		if src not in dic[WM_TRA]:
			dic[WM_TRA][src] = Traffic(dic, src)
		dic[WM_TRA][src].add_sent(dst)
		if dst not in dic[WM_TRA]:
			dic[WM_TRA][dst] = Traffic(dic, dst)
		dic[WM_TRA][dst].add_recv(src)

def ap_sender(pkt, dic, src, dst):
	#sender is an AP, do we know it ?
	if src in dic[WM_AP]:
		#yes we do
		ap = dic[WM_AP][src]
	else:
		#no we don't, create it
		ap = add_ap(dic, src)
	#sender is an AP, receiver must be an STA. Do we know it ?
	if dst in dic[WM_STA]:
		#yes we do
		sta = dic[WM_STA][dst]
	else:
		#no we don't, create it
		sta = add_station(dic, dst)
	return ap, sta

def sta_sender(pkt, dic, src, dst):
	#sender is an STA, do we know it ?
	if src in dic[WM_STA]:
		#yes we do
		sta = dic[WM_STA][src]
	else:
		#no we don't, create it
		sta = add_station(dic, src)
	#sender is an STA, receiver must be an AP. Do we know it ?
	if dst in dic[WM_AP]:
		#yes we do
		ap = dic[WM_AP][dst]
	else:
		#no we don't, create it
		ap = add_ap(dic, dst)
	return ap, sta

def parse_pkt(pkt, dic, channel=None):
	"""
		:param packet: scapy packet
		:param dic: dictionnary from parse function

		::seealso:: parse()
	"""
	#ignore control frames
	if is_control(pkt):
		return

	#check if we know both devices, create them if we don't

	#get the sender and the destination
	#Note: ap or sta will be None if broadcast
	ds = wifi_mapper_ds.get_addrs(pkt)
	src = ds[WM_DS_SENDER]
	dst = ds[WM_DS_RECEIVER]
	if src == ds[WM_DS_AP]:
		ap, sta = ap_sender(pkt, dic, src, dst)
	elif src == ds[WM_DS_STATION]:
		ap, sta = sta_sender(pkt, dic, src, dst)
	else:
		#TODO FIX WEIRD MULTICAST 
		return

	"""
	if not ap:
		print("NO AP: %s" % pkt.summary())
		print("SRC: %s" % src)
		print("DST: %s" % dst)
	if not sta:
		print("NO STATION: %s" % pkt.summary())
		print("SRC: %s" % src)
		print("DST: %s" % dst)
	"""

	#start by parsing what is in every packets: RSSI and traffic
	if ap and src == ds[WM_DS_AP]:
		ap.set_rssi(pkt.dBm_AntSignal)
	elif sta:
		sta.set_rssi(pkt.dBm_AntSignal)
	handle_traffic(pkt, dic, src, dst)

	#keep on with parsing specified packets
	if pkt.haslayer(Dot11Beacon):
		parse_beacon(pkt, dic, ap)
	elif pkt.haslayer(Dot11ProbeResp):
		parse_beacon(pkt, dic, ap)
	elif pkt.haslayer(Dot11ProbeReq):
		parse_probeReq(pkt, dic, sta, ap)
	elif pkt.haslayer(Dot11AssoReq):
		parse_assocReq(pkt, dic, sta)
	elif pkt.haslayer(Dot11ReassoReq):
		parse_reassocReq(pkt, dic, sta)
	elif pkt.haslayer(Dot11AssoResp):
		parse_assocResp(pkt, dic, sta, ap)
	elif pkt.haslayer(Dot11ReassoResp):
		parse_assocResp(pkt, dic, sta, ap)
	elif pkt.haslayer(Dot11Disas):
		sta.set_connected(None) #TODO
	elif pkt.haslayer(Dot11Deauth):
		sta.set_connected(None) #TODO
	elif is_data(pkt) and not is_broadcast(ds[WM_DS_SENDER]):
		if sta: #if rcv not broadcast (see from ds)
			sta.set_connected(ap.bssid) #TODO
		else:
			dic[WM_TRA][ap.bssid].add_sent(None) #TODO

def start_parsing_pkt(dic, pkt, channel=None):
	if pkt.haslayer(RadioTap):
		parse_pkt(pkt, dic, channel=channel)
	else:
		return False
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
