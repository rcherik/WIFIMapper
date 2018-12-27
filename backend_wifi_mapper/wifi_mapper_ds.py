#! /usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import Dot11
try:
	from scapy.all import Dot11FCS
except ImportError:
	Dot11FCS = None

WM_DS_SRC = 0
WM_DS_TRANS = 1
WM_DS_RCV = 2
WM_DS_DST = 3
WM_DS_AP = 4
WM_DS_STATION = 5
WM_DS_SENT = 6
WM_DS_FROM = 7
WM_DS_TO = 8

WM_DS_SENDER = 9
WM_DS_RECEIVER = 10

def get_addrs(packet):
	"""
		From the DS flag, return parsed 802.11 addresses field

		:param packet: scapy packet
		:return: src (source), trans (transmitter), rcv (receiver),
			dst (destination), bssid, station (guess from DS flag),
			sent (True if station has sent, False if it has received),
			from_ds, to_ds
		:rtype: list
	"""
	layer = Dot11 if packet.haslayer(Dot11) else Dot11FCS
	ds = packet.FCfield & 0x3
	to_ds = ds & 0x1 != 0
	from_ds = ds & 0x2 != 0
	if from_ds and not to_ds:
		"""
			The frame is being forwarded by an AP typically.
			In this case, the AP is the transmitter but not the original source
		"""
		rcv = packet[layer].addr1
		dst = packet[layer].addr1
		trans = packet[layer].addr2
		bssid = packet[layer].addr2
		src = packet[layer].addr3
		station = rcv
		sent = False
		sender = bssid
		receiver = rcv
	elif not from_ds and not to_ds:
		"""
			From station to station
		"""
		rcv = packet[layer].addr1
		dst = packet[layer].addr1
		src = packet[layer].addr2
		trans = packet[layer].addr2
		bssid = packet[layer].addr3
		station = src if bssid == rcv else rcv
		sent = True if bssid == rcv else False
		sender = station if bssid == rcv else src #TODO station to station, do we want the ap getting involved ?
		receiver = bssid if bssid == rcv else rcv #TODO ^^^^

		"""
		if packet.type == 0 and packet.subtype == 13:
			print()
			print("================= STA TO STA ======================")
			packet.show()
			print(packet.summary())
			print("================= STA TO STA ======================")
			print()
		"""
	elif not from_ds and to_ds:
		"""
			The frame is being sent from a station to the DS.
			Here the receiver will be typically the AP which is 
				maybe not the final destination
		"""
		rcv = packet[layer].addr1
		bssid = packet[layer].addr1
		src = packet[layer].addr2
		trans = packet[layer].addr2
		dst = packet[layer].addr3
		station = src
		sent = True
		sender = station
		receiver = bssid
	elif from_ds and to_ds:
		"""
			From AP to AP - Do nothing
		"""
		rcv = packet[layer].addr1
		trans = packet[layer].addr2
		dst = packet[layer].addr3
		src = packet[layer].addr4
		bssid = None
		station = None
		sent = False
		sender = packet[layer].addr2
		receiver = packet[layer].addr1
		"""
		print()
		print("================= AP TO AP ======================")
		packet.show()
		print(packet.summary())
		print("================= AP TO AP ======================")
		print()
		"""
		return None


	return [
		src,
		trans,
		rcv,
		dst,
		bssid,
		station,
		sent,
		from_ds,
		to_ds,
		sender,
		receiver,
	]

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
