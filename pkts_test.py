import sys
from scapy.all import *
from backend_wifi_mapper.rssi_scapy import get_rssi

def callback(pkt):
    print(pkt.summary())

def test(iface):
    print("scapy (%s)" % scapy.config.conf.version)
    scapy.all.sniff(iface=iface,
            prn=callback,
            store=0,
            timeout=5)
    sys.exit(0)
