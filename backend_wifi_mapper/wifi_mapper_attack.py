import scapy

def send_pkt(packets, iface, count=1, loop=0, inter=0):
    for packet in packets:
        scapy.sendrecv.send(packet,
                iface=iface,
                count=count,
                loop=loop,
                inter=inter)
