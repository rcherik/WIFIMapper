#! /usr/bin/python
# -*- coding: utf-8 -*-

import struct
import scapy
from scapy.all import RadioTap

radiotap_formats = {
	"TSFT":"Q", #8
	"Flags":"B", #1
	"Rate":"B", #1
	"Channel":"HH", #2 ??
	"FHSS":"BB",
	"dBm_AntSignal":"b",
	"dBm_AntNoise":"b",
	"Lock_Quality":"H",
	"TX_Attenuation":"H",
	"dB_TX_Attenuation":"H",
	"dBm_TX_Power":"b",
	"Antenna":"B",
	"dB_AntSignal":"B",
	"dB_AntNoise":"B",
	"b14":"H", "b15":"B", "b16":"B", "b17":"B", "b18":"B",
	"b19":"BBB", "b20":"LHBB", "b21":"HBBBBBH", "b22":"B", "b23":"B",
	"b24":"B", "b25":"B", "b26":"B", "b27":"B", "b28":"B", "b29":"B",
	"b30":"B", "Ext":"B"
}

def get_rssi(packet):
	"""		
		(src: https://github.com/azz2k/scapy-rssi/blob/master/scapy-rssi.py)

		:param packet: scapy packet
		:return: None or rssi
		:rtype: None or int
	"""
	if scapy.config.conf.version != "2.2.0":
		import scapy_ex
	if hasattr(packet[RadioTap], 'dBm_AntSignal'):
		return packet[RadioTap].dBm_AntSignal
	if scapy.config.conf.version == "2.2.0":
		sig = 0
		field, val = packet.getfield_and_val("present")
		names = [field.names[i][0] for i in range(len(field.names))\
				if (1 << i) & val != 0]
		if "dBm_AntSignal" in names:
			fmt = "<"
			rssipos = 0
			for name in names:
				if name == "dBm_AntSignal":
					rssipos = len(fmt) - 1
				fmt = fmt + radiotap_formats[name]
			decoded = struct.unpack(fmt,
					packet.notdecoded[:struct.calcsize(fmt)])
			return decoded[rssipos]
	return None

# vim:noexpandtab:autoindent:tabstop=4:shiftwidth=4:
