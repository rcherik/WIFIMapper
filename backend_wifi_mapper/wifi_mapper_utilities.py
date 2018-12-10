#! /usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import Dot11
try:
	from scapy.all import Dot11FCS
except ImportError:
	Dot11FCS = None

#Macro for frame types
MANAGEMENT = 0
CONTROL = 1
DATA = 2

#Macro for FCfield flags
FC_RETRANSMIT = 0x8

#Macro for fields
WM_AP = 0
WM_STA = WM_STATION = 1
WM_TRA = WM_TRAFFIC = 2
WM_VENDOR = 3
WM_CHANGES = 4

def get_wm_list():
	return [{}, {}, {}, {}, [[], []]]
			#AP, Sta, Traf, Vendor, Changes [[AP], [Station]]

def is_control(packet):
	#Check if packet type is control
	layer = Dot11 if packet.haslayer(Dot11) else Dot11FCS
	if packet[layer].type == CONTROL:
		return True
	return False

def is_data(packet):
	#Check if packet type is data
	layer = Dot11 if packet.haslayer(Dot11) else Dot11FCS
	if packet[layer].type == DATA:
		return True
	return False

def is_broadcast(addr):
	"""
		Broadcasts:
			00:00:00:00:00:00
			ff:ff:ff:ff:ff:ff
		IPV4 mcast:
			01:00
		IPV6 mcast:
			33:33

		:param addr: str mac addr
		:return: True if mac addr is broadcast else False
		:rtype: bool
	"""
	if not isinstance(addr, str):
		return True
	if addr == "00:00:00:00:00:00" or addr == "ff:ff:ff:ff:ff:ff"\
		or addr.startswith("33:33")\
		or addr.startswith("01:00"):
		return True
	return False

def is_retransmitted(packet):
	"""
		:param packet: scapy packet with Dot11 layer
		:return: True if packet retransmitted else False
		:rtype: bool
	"""
	layer = Dot11 if packet.haslayer(Dot11) else Dot11FCS
	if packet[layer].FCfield & FC_RETRANSMIT:
		return True
	return False

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
