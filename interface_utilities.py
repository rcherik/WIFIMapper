""" System """
from __future__ import print_function
import os
import sys
import subprocess

def find_iface():
    """ Find internet interface and returns it """
    try:
        dn = open(os.devnull, 'w')
    except IOError:
        dn = None
    try:
        ipr = subprocess.Popen(['/sbin/iwconfig'],
                stdout=subprocess.PIPE, stderr=dn)
        if dn:
            dn.close()
        for line in ipr.communicate()[0].splitlines():
            if 'IEEE 802.11' in line:
                l = line.split()
                iface = l[0]
                return iface
    except Exception as e:
        if dn and not dn.closed:
            dn.close()
        sys.exit('Could not find interface: ' + e.message)

def list_interfaces():
    lst = []
    wireless_lst = []
    if os.name == 'posix':
        for dir in os.listdir('/sys/class/net'):
            lst.append(dir)
        for iface in lst:
            if os.path.isdir('/sys/class/net/%s/wireless' % iface):
                wireless_lst.append(iface)
    return wireless_lst, lst

def is_interface_up(iface):
    """
        http://lxr.free-electrons.com/source/include/uapi/linux/if_arp.h

        Managed Mode: Type = 1 (ARPHRD_ETHER)
        Monitor Mode: Type = 803 (ARPHRD_IEEE80211_RADIOTAP)
    """
    if os.name == 'posix':
        with open('/sys/class/net/%s/type' % iface, 'r') as f:
            t = int(f.read())
            if t == 1:
                return False
            elif t == 803:
                return True
        return False
    return False
