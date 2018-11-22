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
