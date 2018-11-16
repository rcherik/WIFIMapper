#! /usr/bin/python
# -*- coding: utf-8 -*-

from scapy.all import Dot11, Dot11FCS

def get_addrs(packet):
	"""
		From the DS flag, return parsed 802.11 addresses field

		:param packet: scapy packet
		:return: src (source), trans (transmitter), rcv (receiver),
			dst (destination), bssid, station (guess from DS flag),
			sent (True if station has sent, False if it has received),
			from_ds, to_ds
		:rtype: dict
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
	return {
		"src":src,
		"trans": trans,
		"rcv": rcv,
		"dst": dst,
		"bssid": bssid,
		"station": station,
		"sent": sent,
		"from": from_ds,
		"to": to_ds
	}

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
