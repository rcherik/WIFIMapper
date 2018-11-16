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
	ds = packet.FCfield & 0x3
	to_ds = ds & 0x1 != 0
	from_ds = ds & 0x2 != 0
	if from_ds and not to_ds:
		"""
			The frame is being forwarded by an AP typically.
			In this case, the AP is the transmitter but not the original source
		"""
		rcv = packet[Dot11FCS].addr1
		dst = packet[Dot11FCS].addr1
		trans = packet[Dot11FCS].addr2
		bssid = packet[Dot11FCS].addr2
		src = packet[Dot11FCS].addr3
		station = rcv
		sent = False
	elif not from_ds and not to_ds:
		"""
			From station to station
		"""
		rcv = packet[Dot11FCS].addr1
		dst = packet[Dot11FCS].addr1
		src = packet[Dot11FCS].addr2
		trans = packet[Dot11FCS].addr2
		bssid = packet[Dot11FCS].addr3
		station = src if bssid == rcv else rcv
		sent = True if bssid == rcv else False
	elif not from_ds and to_ds:
		"""
			The frame is being sent from a station to the DS.
			Here the receiver will be typically the AP which is 
				maybe not the final destination
		"""
		rcv = packet[Dot11FCS].addr1
		bssid = packet[Dot11FCS].addr1
		src = packet[Dot11FCS].addr2
		trans = packet[Dot11FCS].addr2
		dst = packet[Dot11FCS].addr3
		station = src
		sent = True
	elif from_ds and to_ds:
		"""
			From AP to AP - Do nothing
		"""
		rcv = packet[Dot11FCS].addr1
		trans = packet[Dot11FCS].addr2
		dst = packet[Dot11FCS].addr3
		src = packet[Dot11FCS].addr4
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
