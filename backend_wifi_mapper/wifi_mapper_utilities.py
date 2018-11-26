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
WM_HDSHK = WM_HANDSHAKES = 3
WM_VENDOR = 4

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

def is_multicast(addr):
	"""
		Check strongest byte's strongest bit to see if mac addr is broadcast

		:param addr: str mac addr
		:return: True if mac addr is broadcast else False
		:rtype: bool
	"""
	if not isinstance(addr, str):
		return True
	if addr == "00:00:00:00:00:00":
		return True
	split = addr.split(':')
	hexa = int(split[0], 16)
	if hexa & 0x1:
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
