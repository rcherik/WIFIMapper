"""Database of signatures for known Wifi devices."""

import hashlib
import subprocess
#import dhcp

TAXONOMY_C_FILE = "backend_wifi_mapper/C_Utilities/create_signature.c"

# Associated with each signature is a tuple:
# Field #1 = Genus = a human-recognizeable name for the device. If the device
#   has branding silkscreened on it (ex: "Samsung Galaxy S4" on the back), that
#   should probably be the Genus though this isn't rigidly adhered to.
#   We want someone reading the Genus to recognize it without thinking to
#   themselves "Wow, that is comically detailed."
# Field #2 = Species = the most specific designation we know of, such as the
#   version or model number or vintage. Not all entries will have a Species,
#   if the Genus is very specific we may not have any additional information
#   to put in the species.
#   We want someone reading the Species to think to themselves "Wow, that is
#   comically detailed."
# Field #3 = Frequency = band of this signature, '2.4GHz' or '5GHz'.

database = {
    'wifi4|probe:0,1,50,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),extcap:00000080,wps:5042T|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Alcatel One Touch', 'Pop Astro', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:ALCATEL_ONE_TOUCH_Fierce|assoc:0,1,50,45,127,221(0050f2,2),48,htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Alcatel One Touch', 'Fierce 2', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff|oui:amazon':
        ('Amazon Dash Button', '', '2.4GHz'),

    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0200000040|oui:amazon':
        ('Amazon Fire Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0200000040|oui:amazon':
        ('Amazon Fire Phone', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0200000000|oui:amazon':
        ('Amazon Fire Phone', '', '2.4GHz'),

    'wifi4|probe:0,1,221(0050f2,4),221(506f9a,9),wps:AFTS|assoc:0,1,45,191,127,221(000c43,6),221(0050f2,2),htcap:008e,htagg:1f,htmcs:0000ffff,vhtcap:31c139b0,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:0000000000000040':
        ('Amazon Fire TV', '2015 (2nd gen)', '5GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),221(506f9a,9),htcap:01ed,htagg:1f,htmcs:0000ffff,extcap:00,wps:AFTS|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:008c,htagg:1f,htmcs:0000ffff,extcap:00000a02':
        ('Amazon Fire TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),221(506f9a,9),htcap:01ef,htagg:1f,htmcs:0000ffff,extcap:00,wps:AFTS|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:008c,htagg:1f,htmcs:0000ffff,extcap:00000a02':
        ('Amazon Fire TV', '2015 (2nd gen)', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:AFTS|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:008c,htagg:1f,htmcs:0000ffff,extcap:00000a02':
        ('Amazon Fire TV', '2015 (2nd gen)', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:007e,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,48,45,221(001018,2),221(0050f2,2),htcap:007e,htagg:1b,htmcs:0000ffff,txpow:e50d|oui:amazon':
        ('Amazon Fire TV Stick', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:003c,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:003c,htagg:1b,htmcs:0000ffff,txpow:170c|oui:amazon':
        ('Amazon Fire TV Stick', '', '2.4GHz'),

    'wifi4|probe:0,1,45,htcap:11ee,htagg:02,htmcs:0000ffff|assoc:0,1,33,36,48,221(0050f2,2),45,127,htcap:11ee,htagg:02,htmcs:0000ffff,txpow:0e00,extcap:01|oui:amazon':
        ('Amazon Echo', '', '5GHz'),
    'wifi4|probe:0,1,50,45,htcap:01ac,htagg:02,htmcs:0000ffff|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:01ac,htagg:02,htmcs:0000ffff,extcap:01|oui:amazon':
        ('Amazon Echo', '', '2.4GHz'),

    'wifi4|probe:0,1,221(0050f2,4),221(506f9a,9),wps:AEOBC|assoc:0,1,36,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Amazon Echo', 'Dot', '5GHz'),
    'wifi4|probe:0,1,221(0050f2,4),221(506f9a,9),wps:AEOBC|assoc:0,1,36,45,48,127,221(0050f2,2),htcap:0130,htagg:03,htmcs:000000ff,extcap:00':
        ('Amazon Echo', 'Dot', '5GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:AEOBC|assoc:0,1,50,36,45,48,127,221(0050f2,2),htcap:0130,htagg:03,htmcs:000000ff,extcap:00':
        ('Amazon Echo', 'Dot', '2.4GHz'),

    'wifi4|probe:0,1,50|assoc:0,1,50,48,221(0050f2,2)|oui:amazon':
        ('Amazon Kindle', '', '2.4GHz'),
    'wifi4|probe:0,1,50|assoc:0,1,50,221(0050f2,2)|oui:amazon':
        ('Amazon Kindle', 'Keyboard 3', '2.4GHz'),
    'wifi4|probe:0,1,50,45,htcap:002c,htagg:01,htmcs:000000ff|assoc:0,1,50,45,48,221(0050f2,2),htcap:002c,htagg:01,htmcs:000000ff|oui:amazon':
        ('Amazon Kindle', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:1130,htagg:18,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:1130,htagg:18,htmcs:000000ff|oui:amazon':
        ('Amazon Kindle', 'Fire 7" (2011 edition)', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:KFFOWI|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Amazon Kindle', 'Fire 7" (2015 edition)', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:KFFOWI|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:0130,htagg:03,htmcs:000000ff,extcap:00':
        ('Amazon Kindle', 'Fire 7" (2015 edition)', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:081e,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:081e,htagg:1b,htmcs:0000ffff,txpow:0008|os:appletv1':
        ('Apple TV', '1st gen', '5GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:181c,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:181c,htagg:1b,htmcs:0000ffff,txpow:1308|os:appletv1':
        ('Apple TV', '1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:581c,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:581c,htagg:1b,htmcs:0000ffff,txpow:1308|os:appletv1':
        ('Apple TV', '1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:181c,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:581c,htagg:1b,htmcs:0000ffff,txpow:1308|os:appletv1':
        ('Apple TV', '1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:581c,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:181c,htagg:1b,htmcs:0000ffff,txpow:1308|os:appletv1':
        ('Apple TV', '1st gen', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:080c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:080c,htagg:1b,htmcs:000000ff,txpow:1208|oui:apple':
        ('Apple TV', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:180c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:180c,htagg:1b,htmcs:000000ff,txpow:1308|oui:apple':
        ('Apple TV', '2nd gen', '2.4GHz'),

    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff,txpow:180f|name:appletv':
        ('Apple TV', '3rd gen', '2.4GHz'),
    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff,txpow:180f|name:appletv':
        ('Apple TV', '3rd gen', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1907|oui:apple':
        ('Apple TV', '3rd gen rev A', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1907|oui:apple':
        ('Apple TV', '3rd gen rev A', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1a07|oui:apple':
        ('Apple TV', '3rd gen rev A', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1a07|oui:apple':
        ('Apple TV', '3rd gen rev A', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:appletv':
        ('Apple TV', '4th gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1502,extcap:0000000000000040|name:appletv':
        ('Apple TV', '4th gen', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff|oui:apple':
        ('Apple Watch', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff|oui:apple':
        ('Apple Watch', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0017f2,10),221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff|oui:apple':
        ('Apple Watch', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:040000000000004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1e08,extcap:0400000000000040|oui:asus':
        ('ASUS ZenFone', 'AR', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:asus':
        ('ASUS ZenFone', 'AR', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:asus':
        ('ASUS ZenFone', 'AR', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1e08,extcap:0400000000000040|oui:asus':
        ('ASUS ZenFone', 'AR', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:asus':
        ('ASUS ZenFone', 'AR', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:asus':
        ('ASUS ZenFone', 'AR', '5GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),3,127,htcap:012f,htagg:df,htmcs:000000ff,extcap:04000a020100004080|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012d,htagg:1f,htmcs:000000ff,txpow:1e08|oui:asus':
        ('ASUS ZenFone', 'AR', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:040000000000000080|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012d,htagg:1f,htmcs:000000ff,txpow:1e08|oui:asus':
        ('ASUS ZenFone', 'AR', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),191,127,htcap:012d,htagg:1f,htmcs:000000ff,vhtcap:33907112,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:040000000000004080|assoc:0,1,50,48,45,221(0050f2,2),127,221(00904c,4),htcap:012d,htagg:1f,htmcs:000000ff,extcap:0400080200000040|oui:asus':
        ('ASUS ZenFone', 'AR', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),3,127,htcap:012f,htagg:df,htmcs:000000ff,extcap:04000a020100004080|assoc:0,1,50,48,45,221(0050f2,2),127,221(00904c,4),htcap:012d,htagg:1f,htmcs:000000ff,extcap:0400080200000040|oui:asus':
        ('ASUS ZenFone', 'AR', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),191,127,htcap:012d,htagg:1f,htmcs:000000ff,vhtcap:33903112,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,50,48,45,221(0050f2,2),127,221(00904c,4),htcap:012d,htagg:1f,htmcs:000000ff,extcap:0400080200000040|oui:asus':
        ('ASUS ZenFone', 'AR', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(001018,2),htcap:0020,htagg:17,htmcs:000000ff,wps:ASUS_Z007|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:17,htmcs:000000ff,txpow:140d':
        ('ASUS ZenFone', 'C', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0200000000|oui:asus':
        ('ASUS ZenFone', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:160d,extcap:00000a0200000000|oui:asus':
        ('ASUS ZenFone', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,45,3,221(0050f2,4),221(506f9a,9),221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff,wps:ASUS_T00F|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff':
        ('ASUS ZenFone', '5', '2.4GHz'),

    'wifi4|probe:0,1,50,45,htcap:1030,htagg:18,htmcs:000000ff|assoc:0,1,50,46,48,45,221(0050f2,2),htcap:1030,htagg:18,htmcs:000000ff|oui:barnes&noble':
        ('Barnes & Noble Nook', 'Color', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4)|assoc:0,1,50,45,221(0050f2,2),48,htcap:000c,htagg:1b,htmcs:000000ff|os:wemo':
        ('Belkin WeMo', 'Switch', '2.4GHz'),

    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(001018,2),htcap:016f,htagg:17,htmcs:0000ffff,vhtcap:0f815932,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140,wps:STV100_1|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:016f,htagg:17,htmcs:0000ffff,vhtcap:0f815932,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:000008800140':
        ('Blackberry Priv', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(001018,2),htcap:016f,htagg:17,htmcs:0000ffff,vhtcap:0f815932,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040,wps:STV100_1|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:016f,htagg:17,htmcs:0000ffff,vhtcap:0f815932,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000088001400040':
        ('Blackberry Priv', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(001018,2),htcap:012d,htagg:17,htmcs:0000ffff,extcap:000008800140,wps:STV100_1|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:012d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140':
        ('Blackberry Priv', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(001018,2),htcap:012d,htagg:17,htmcs:0000ffff,extcap:0000088001400040,wps:STV100_1|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:012d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140':
        ('Blackberry Priv', '', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:BLU_DASH_M|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('BLU Dash', 'M', '2.4GHz'),

    'wifi4|probe:0,1,50,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),extcap:00000080,wps:BLU_STUDIO_5_0_C_HD|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:0100008000c6':
        ('BLU Studio', '5.0.C HD', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:BLU_STUDIO_C_SUPER_CAMERA|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('BLU Studio', 'C Super Camera', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:112c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:112c,htagg:19,htmcs:000000ff|os:brotherprinter':
        ('Brother Printer', '', '2.4GHz'),

    # MX410, probably others
    'wifi4|probe:0,1,3,45,50,htcap:007e,htagg:00,htmcs:000000ff|assoc:0,1,45,48,50,221(0050f2,2),htcap:000c,htagg:1b,htmcs:000000ff|os:canonprinter':
        ('Canon Printer', '', '2.4GHz'),
    # MX492, probably others
    'wifi4|probe:0,1,3,45,50,htcap:007e,htagg:00,htmcs:000000ff|assoc:0,1,48,50,221(0050f2,2),45,htcap:000c,htagg:1b,htmcs:000000ff|os:canonprinter':
        ('Canon Printer', '', '2.4GHz'),
    # MX492 has been seen to send these massive Probe packets. Likely other models, too.
    'wifi4|probe:64,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,127,11,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,extcap:|assoc:0,1,48,50,221(0050f2,2),45,htcap:000c,htagg:1b,htmcs:000000ff|os:canonprinter':
        ('Canon Printer', '', '2.4GHz'),
    'wifi4|probe:0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0|assoc:0,1,48,50,221(0050f2,2),45,htcap:000c,htagg:1b,htmcs:000000ff|os:canonprinter':
        ('Canon Printer', '', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:W6210__4560MMX_b_fingerprint_|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01|oui:cherry':
        ('Cherry Mobile One', '', '2.4GHz'),

    'wifi4|probe:0,1,45,191,htcap:11e2,htagg:17,htmcs:0000ffff,vhtcap:038071a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,48,45,127,191,221(0050f2,2),htcap:11e6,htagg:17,htmcs:0000ffff,vhtcap:038001a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000000000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '5GHz'),
    'wifi4|probe:0,1,45,191,htcap:11e2,htagg:17,htmcs:0000ffff,vhtcap:038071a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,48,45,127,191,221(0050f2,2),htcap:11ee,htagg:17,htmcs:0000ffff,vhtcap:038001a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000000000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '5GHz'),
    'wifi4|probe:0,1,45,191,htcap:11e2,htagg:17,htmcs:0000ffff,vhtcap:038071a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,33,36,48,45,127,191,221(0050f2,2),htcap:11e6,htagg:17,htmcs:0000ffff,vhtcap:038001a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1600,extcap:0000000000000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '5GHz'),
    'wifi4|probe:0,1,45,127,191,htcap:11e2,htagg:17,htmcs:0000ffff,vhtcap:038071a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000001000040|assoc:0,1,48,45,127,191,221(0050f2,2),htcap:11e6,htagg:17,htmcs:0000ffff,vhtcap:038001a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000001000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '5GHz'),
    'wifi4|probe:0,1,45,127,191,htcap:11e2,htagg:17,htmcs:0000ffff,vhtcap:038071a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000001000040|assoc:0,1,33,36,48,45,127,191,221(0050f2,2),htcap:11e6,htagg:17,htmcs:0000ffff,vhtcap:038001a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1600,extcap:0000000001000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '5GHz'),
    'wifi4|probe:0,1,45,191,htcap:11e2,htagg:17,htmcs:0000ffff,vhtcap:038071a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,48,45,127,191,221(0050f2,2),htcap:11e6,htagg:17,htmcs:0000ffff,vhtcap:038031a0,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000001000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '5GHz'),
    'wifi4|probe:0,1,50,45,htcap:11e2,htagg:17,htmcs:0000ffff|assoc:0,1,50,48,45,127,221(0050f2,2),htcap:11a4,htagg:17,htmcs:0000ffff,extcap:0000000000000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '2.4GHz'),
    'wifi4|probe:0,1,50,45,htcap:11e2,htagg:17,htmcs:0000ffff|assoc:0,1,50,48,45,127,221(0050f2,2),htcap:11ac,htagg:17,htmcs:0000ffff,extcap:0000000000000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,htcap:11e2,htagg:17,htmcs:0000ffff,extcap:0000000001000040|assoc:0,1,50,48,45,127,221(0050f2,2),htcap:11a4,htagg:17,htmcs:0000ffff,extcap:0000000001000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '2.4GHz'),
    'wifi4|probe:0,1,50,45,htcap:11e2,htagg:17,htmcs:0000ffff|assoc:0,1,50,48,45,127,221(0050f2,2),htcap:11a4,htagg:17,htmcs:0000ffff,extcap:0000000001000040|os:chromeos':
        ('Chromebook', 'Pixel 2', '2.4GHz'),

    'wifi4|probe:0,1,45,htcap:11ef,htagg:1b,htmcs:0000ffff|assoc:0,1,48,45,221(0050f2,2),htcap:11ef,htagg:1b,htmcs:0000ffff|os:chromeos':
        ('Chromebook', 'HP 14', '5GHz'),
    'wifi4|probe:0,1,50,3,45,htcap:11ef,htagg:1b,htmcs:0000ffff|assoc:0,1,50,48,45,221(0050f2,2),htcap:11ef,htagg:1b,htmcs:0000ffff|os:chromeos':
        ('Chromebook', 'HP 14', '2.4GHz'),

    'wifi4|probe:0,1,45,50,htcap:016e,htagg:03,htmcs:0000ffff|assoc:0,1,48,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:0000ffff,extcap:00|os:chromeos':
        ('Chromebook', 'Samsung 2012 model', '5GHz'),
    'wifi4|probe:0,1,45,50,htcap:016e,htagg:03,htmcs:0000ffff|assoc:0,1,48,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:0000ffff,extcap:04|os:chromeos':
        ('Chromebook', 'Samsung 2012 model', '5GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:016e,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:0000ffff,extcap:00|os:chromeos':
        ('Chromebook', 'Samsung 2012 model', '2.4GHz'),
    'wifi4|probe:0,1,3,45,htcap:016e,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:0000ffff,extcap:00|os:chromeos':
        ('Chromebook', 'Samsung 2012 model', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:016e,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:0000ffff,extcap:04|os:chromeos':
        ('Chromebook', 'Samsung 2012 model', '2.4GHz'),
    'wifi4|probe:0,1,3,45,htcap:016e,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:0000ffff,extcap:04|os:chromeos':
        ('Chromebook', 'Samsung 2012 model', '2.4GHz'),

    'wifi4|probe:0,1,3,45,50,htcap:0120,htagg:03,htmcs:00000000|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:012c,htagg:03,htmcs:000000ff,extcap:0000000000000140|oui:google':
        ('Chromecast', 'v1', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:0120,htagg:03,htmcs:00000000|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:112c,htagg:03,htmcs:000000ff,extcap:0400080200000040|oui:google':
        ('Chromecast', 'v1', '2.4GHz'),

    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000000000040|assoc:0,1,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400000000000140|name:chromecast':
        ('Chromecast', 'v2', '5GHz'),
    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000020000040|assoc:0,1,33,36,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1308,extcap:0000000020000040|name:chromecast':
        ('Chromecast', 'v2', '5GHz'),
    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000000000040|assoc:0,1,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0100000000000040|name:chromecast':
        ('Chromecast', 'v2', '5GHz'),
    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000000000040|assoc:0,1,33,36,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400000000000140|name:chromecast':
        ('Chromecast', 'v2', '5GHz'),
    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000000000040|assoc:0,1,33,36,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1308,extcap:0400000000000140|name:chromecast':
        ('Chromecast', 'v2', '5GHz'),
    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000020000040|assoc:0,1,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0000000020000040|name:chromecast':
        ('Chromecast', 'v2', '5GHz'),
    'wifi4|probe:0,1,3,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000000000040|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:002c,htagg:03,htmcs:000000ff,extcap:0000000000000140|name:chromecast':
        ('Chromecast', 'v2', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000020000040|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:002c,htagg:03,htmcs:000000ff,extcap:0000000020000040|name:chromecast':
        ('Chromecast', 'v2', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000020000040|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:102c,htagg:03,htmcs:000000ff,extcap:0000000020000040|name:chromecast':
        ('Chromecast', 'v2', '2.4GHz'),

    'wifi4|probe:0,1,45,50,59,127,191,htcap:0163,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0168fffa,vhttxmcs:0168fffa,extcap:040000000100004000|assoc:0,1,48,59,127,221(0050f2,2),45,191,199,htcap:016f,htagg:03,htmcs:0000ffff,vhtcap:33d071b0,vhtrxmcs:009cfffa,vhttxmcs:009cfffa,extcap:050000000000004000|oui:google':
        ('Chromecast', 'Ultra', '5GHz'),
    'wifi4|probe:0,1,45,50,59,127,191,htcap:016f,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0168fffa,vhttxmcs:0168fffa,extcap:040000000100004000|assoc:0,1,48,59,127,221(0050f2,2),45,191,199,htcap:016f,htagg:03,htmcs:0000ffff,vhtcap:33d071b0,vhtrxmcs:009cfffa,vhttxmcs:009cfffa,extcap:040008020000004000|oui:google':
        ('Chromecast', 'Ultra', '5GHz'),
    'wifi4|probe:0,1,45,50,59,127,191,htcap:016f,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0168fffa,vhttxmcs:0168fffa,extcap:040000000100004000|assoc:0,1,33,36,48,59,70,127,221(0050f2,2),45,191,199,htcap:016f,htagg:03,htmcs:0000ffff,vhtcap:33d071b0,vhtrxmcs:009cfffa,vhttxmcs:009cfffa,txpow:1400,extcap:040000000000014000|oui:google':
        ('Chromecast', 'Ultra', '5GHz'),
    'wifi4|probe:0,1,45,50,59,127,191,221(0050f2,8),htcap:016f,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0168fffa,vhttxmcs:0168fffa,extcap:040000000100004000|assoc:0,1,33,36,48,59,70,127,221(0050f2,2),45,191,199,htcap:016f,htagg:03,htmcs:0000ffff,vhtcap:33d071b0,vhtrxmcs:009cfffa,vhttxmcs:009cfffa,txpow:1400,extcap:040000000000014000|oui:google':
        ('Chromecast', 'Ultra', '5GHz'),
    'wifi4|probe:0,1,3,45,50,59,127,191,htcap:0163,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0168fffa,vhttxmcs:0168fffa,extcap:040000000100004000|assoc:0,1,33,48,50,59,70,127,221(0050f2,2),45,199,htcap:012d,htagg:03,htmcs:0000ffff,txpow:1400,extcap:040000000000014000|oui:google':
        ('Chromecast', 'Ultra', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,59,127,191,htcap:016f,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0168fffa,vhttxmcs:0168fffa,extcap:040000000100004000|assoc:0,1,33,48,50,59,70,127,221(0050f2,2),45,199,htcap:012d,htagg:03,htmcs:0000ffff,txpow:1400,extcap:040000000000014000|oui:google':
        ('Chromecast', 'Ultra', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,59,127,191,htcap:016f,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0168fffa,vhttxmcs:0168fffa,extcap:040000000100004000|assoc:0,1,48,50,59,127,221(0050f2,2),45,199,htcap:112d,htagg:03,htmcs:0000ffff,extcap:040008020000004000|oui:google':
        ('Chromecast', 'Ultra', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,59,127,191,htcap:0163,htagg:03,htmcs:00000000,vhtcap:33d071b0,vhtrxmcs:0249fff0,vhttxmcs:0249fff0,extcap:040000000100004000|assoc:0,1,48,50,59,127,221(0050f2,2),45,htcap:112d,htagg:03,htmcs:0000ffff,extcap:040008020000004000|oui:google':
        ('Chromecast', 'Ultra', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:007c,htagg:1a,htmcs:0000ffff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:007c,htagg:1a,htmcs:0000ffff,txpow:1408|os:directv':
        ('DirecTV', 'HR44 or HD54', '5GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:107c,htagg:1a,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:107c,htagg:1a,htmcs:0000ffff,txpow:1608|os:directv':
        ('DirecTV', 'HR44 or HF54', '2.4GHz'),

    # Noted from a ViP722k, likely matches other models
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:186c,htagg:1a,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:186c,htagg:1a,htmcs:0000ffff,txpow:1408|oui:dish':
        ('Dish Network Receiver', '', '2.4GHz'),

    'wifi4|probe:0,1,45,htcap:106e,htagg:01,htmcs:000000ff|assoc:0,1,45,33,36,48,221(0050f2,2),htcap:106e,htagg:01,htmcs:000000ff,txpow:0e00|oui:dropcam':
        ('Dropcam', 'Pro', '5GHz'),
    'wifi4|probe:0,1,50,45,htcap:002c,htagg:01,htmcs:000000ff|assoc:0,1,50,45,48,221(0050f2,2),htcap:002c,htagg:01,htmcs:000000ff|oui:dropcam':
        ('Dropcam', 'HD or Pro', '2.4GHz'),

    'wifi4|probe:0,1,50,45,htcap:002c,htagg:01,htmcs:000000ff|assoc:0,1,50,45,48,221(0050f2,2),htcap:002c,htagg:01,htmcs:000000ff|oui:ecobee':
        ('ecobee thermostat', 'ecobee3', '2.4GHz'),

    'wifi4|probe:0,1,3,45,50,htcap:0162,htagg:00,htmcs:000000ff|assoc:0,1,45,48,127,50,221(0050f2,2),htcap:016e,htagg:1b,htmcs:000000ff,extcap:00|os:epsonprinter':
        ('Epson Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:182c,htagg:1b,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:182c,htagg:1b,htmcs:000000ff|os:epsonprinter':
        ('Epson Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,50,221(001018,2)|assoc:0,1,48,50,221(001018,2)|os:epsonprinter':
        ('Epson Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff|os:epsonprinter':
        ('Epson Printer', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff|oui:firstalert':
        ('First Alert thermostat', '', '2.4GHz'),

    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000020000040|assoc:0,1,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0000000020000040|oui:google':
        ('Google Home', '', '5GHz'),
    'wifi4|probe:0,1,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000000000040|assoc:0,1,33,36,48,127,221(0050f2,2),45,191,htcap:006e,htagg:03,htmcs:000000ff,vhtcap:33c07030,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1308,extcap:0400000000000140|oui:google':
        ('Google Home', '', '5GHz'),
    'wifi4|probe:0,1,3,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000020000040|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:002c,htagg:03,htmcs:000000ff,extcap:0000000020000040|oui:google':
        ('Google Home', '', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,127,191,htcap:0062,htagg:03,htmcs:00000000,vhtcap:33c07030,vhtrxmcs:0124fffc,vhttxmcs:0124fffc,extcap:0000000020000040|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:102c,htagg:03,htmcs:000000ff,extcap:0000000020000040|oui:google':
        ('Google Home', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff|oui:ademco':
        ('Honeywell thermostat', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:102c,htagg:1b,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:102c,htagg:1b,htmcs:000000ff|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:0160,htagg:03,htmcs:000000ff|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:016c,htagg:03,htmcs:000000ff,extcap:00|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:0160,htagg:03,htmcs:000000ff|assoc:0,1,45,48,127,50,221(0050f2,2),htcap:016c,htagg:03,htmcs:000000ff,extcap:00000000|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(0050f2,2),221(506f9a,9),htcap:0020,htagg:1a,htmcs:000000ff|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:0060,htagg:03,htmcs:000000ff|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:006c,htagg:03,htmcs:000000ff,extcap:00|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,127,htcap:010c,htagg:1b,htmcs:0000ffff,extcap:00|assoc:0,1,45,48,127,50,221(0050f2,2),htcap:016c,htagg:1b,htmcs:000000ff,extcap:00|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,50,221(001018,2)|assoc:0,1,48,50,221(001018,2)|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,127,htcap:010c,htagg:1b,htmcs:0000ffff,extcap:00|assoc:0,1,48,50,221(0050f2,2)|os:hpprinter':
        ('HP Printer', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:03800032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:03800032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e008,extcap:0000000000000040|oui:htc':
        ('HTC One', '', '5GHz'),
    'wifi4|probe:0,1,3,45,127,191,221(001018,2),221(00904c,51),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:03800032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:03800032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e008,extcap:0000000000000040|oui:htc':
        ('HTC One', '', '5GHz'),
    'wifi4|probe:0,1,50,45,127,221(001018,2),221(00904c,51),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1408|oui:htc':
        ('HTC One', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1408|oui:htc':
        ('HTC One', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1408,extcap:0000000000000040|oui:htc':
        ('HTC One', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:HTC_VLE_U|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('HTC One', 'S', '2.4GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:HTC_VLE_U|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('HTC One', 'S', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a820040,wps:HTC_One_M8|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a820040,wps:HTC_One_M8|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040,wps:HTC_One_M8|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:0000008001400040':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040|oui:htc':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a820040,wps:HTC_One_M8|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a8201400040':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a8201400040|oui:htc':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a820040,wps:HTC_One_M8|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a8201400000':
        ('HTC One', 'M8', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a8201400000|oui:htc':
        ('HTC One', 'M8', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:140d,extcap:00000a8201400000|oui:htc':
        ('HTC One', 'M8', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a820040,wps:HTC_One_M8|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:140d,extcap:00000a8201400000':
        ('HTC One', 'M8', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:160d,extcap:00000a8201400000|oui:htc':
        ('HTC One', 'M8', '2.4GHz'),

    # HTC One M8, Sprint edition
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a820040,wps:831C|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a8201400000':
        ('HTC One', 'M8', '2.4GHz'),

    # HTC One M8, Verizon edition
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040,wps:HTC6525LVW|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040,wps:HTC6525LVW|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a8201400040':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040,wps:HTC6525LVW|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a8201400040':
        ('HTC One', 'M8', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a820040,wps:HTC6525LVW|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:160d,extcap:00000a8201400000':
        ('HTC One', 'M8', '2.4GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040,wps:HTC6525LVW|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040':
        ('HTC One', 'M8', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:000000800040,wps:HTC6525LVW|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a8201400000':
        ('HTC One', 'M8', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:000000800040,wps:HTC6525LVW|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:160d,extcap:00000a8201400000':
        ('HTC One', 'M8', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,107,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e009,extcap:0000088001400040|oui:htc':
        ('HTC One', 'M9', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040,wps:HTC_One_M9|assoc:0,1,33,36,48,45,127,107,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e009,extcap:0000088001400040':
        ('HTC One', 'M9', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000008800140,wps:HTC_One_M9|assoc:0,1,33,36,48,45,127,107,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e009,extcap:000008800140':
        ('HTC One', 'M9', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(0050f2,8),221(001018,2),htcap:1063,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,50,33,36,45,127,107,221(001018,2),221(0050f2,2),htcap:1063,htagg:17,htmcs:000000ff,txpow:1309,extcap:000008800140|oui:htc':
        ('HTC One', 'M9', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(506f9a,16),221(0050f2,8),221(001018,2),htcap:1063,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,50,33,36,45,127,107,221(001018,2),221(0050f2,2),htcap:1063,htagg:17,htmcs:000000ff,txpow:1309,extcap:000008800140|oui:htc':
        ('HTC One', 'M9', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:1063,htagg:17,htmcs:000000ff,extcap:0000088001400040,wps:HTC_One_M9|assoc:0,1,50,33,36,48,45,127,107,221(001018,2),221(0050f2,2),htcap:1063,htagg:17,htmcs:000000ff,txpow:1309,extcap:000008800140':
        ('HTC One', 'M9', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:1063,htagg:17,htmcs:000000ff,extcap:000008800140,wps:HTC_One_M9|assoc:0,1,50,33,36,48,45,127,107,221(001018,2),221(0050f2,2),htcap:1063,htagg:17,htmcs:000000ff,txpow:1309,extcap:000008800140':
        ('HTC One', 'M9', '2.4GHz'),

    # HTC One M9, Sprint edition
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,10),221(506f9a,9),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000008800140,wps:0PJA2|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e009,extcap:000008800140':
        ('HTC One', 'M9', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:1063,htagg:17,htmcs:000000ff,extcap:000008800140,wps:0PJA2|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:1063,htagg:17,htmcs:000000ff,txpow:1309,extcap:000008800140':
        ('HTC One', 'M9', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(0050f2,4),221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff,wps:_|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff|oui:htc':
        ('HTC One', 'V', '2.4GHz'),

    'wifi4|probe:0,1,45,htcap:0130,htagg:18,htmcs:000000ff|assoc:0,1,48,45,221(0050f2,2),htcap:013c,htagg:18,htmcs:000000ff|oui:htc':
        ('HTC One', 'X', '5GHz'),
    'wifi4|probe:0,1,50,45,htcap:0130,htagg:18,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:013c,htagg:18,htmcs:000000ff|oui:htc':
        ('HTC One', 'X', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:000008':
        ('HTC 10', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,33,36,48,70,45,191,221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102':
        ('HTC 10', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,33,36,48,70,45,191,221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102':
        ('HTC 10', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9138b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:000008':
        ('HTC 10', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:0163,htagg:17,htmcs:0000ffff,vhtcap:0f901032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9138b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:000008':
        ('HTC 10', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:000008':
        ('HTC 10', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:11ef,htagg:17,htmcs:0000ffff,extcap:00080f8401400040,wps:HTC_M10h|assoc:0,1,50,33,36,48,70,45,221(001018,2),221(0050f2,2),htcap:11ef,htagg:17,htmcs:0000ffff,txpow:1302':
        ('HTC 10', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:11ef,htagg:17,htmcs:0000ffff,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:11ef,htagg:17,htmcs:0000ffff,txpow:1302,extcap:000008':
        ('HTC 10', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,4),221(506f9a,9),221(506f9a,16),221(0050f2,8),221(001018,2),htcap:11ef,htagg:17,htmcs:0000ffff,extcap:00080f840140,wps:HTC_M10h|assoc:0,1,50,33,36,48,70,45,221(001018,2),221(0050f2,2),htcap:11ef,htagg:17,htmcs:0000ffff,txpow:1302':
        ('HTC 10', '', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:Infinix_X510|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Infinix HOT', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:080c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:080c,htagg:1b,htmcs:000000ff,txpow:1008|oui:apple':
        ('iPad', '1st or 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,221(001018,2),htcap:080c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),htcap:080c,htagg:1b,htmcs:000000ff,txpow:1008|oui:apple':
        ('iPad', '1st or 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:0800,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0800,htagg:1b,htmcs:000000ff,txpow:1008|oui:apple':
        ('iPad', '1st or 2nd gen', '5GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:180c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:180c,htagg:1b,htmcs:000000ff,txpow:1008|oui:apple':
        ('iPad', '1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:1800,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1800,htagg:1b,htmcs:000000ff,txpow:1008|oui:apple':
        ('iPad', '1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:180c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:180c,htagg:1b,htmcs:000000ff,txpow:1108|oui:apple':
        ('iPad', '2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:1800,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1800,htagg:1b,htmcs:000000ff,txpow:1108|oui:apple':
        ('iPad', '2nd gen', '2.4GHz'),

    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff,txpow:180f|oui:apple':
        ('iPad', '3rd gen', '5GHz'),
    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff,txpow:180f|oui:apple':
        ('iPad', '3rd gen', '5GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff,txpow:150c|oui:apple':
        ('iPad', '3rd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff,txpow:150c|oui:apple':
        ('iPad', '3rd gen', '2.4GHz'),

    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1906':
        ('iPad', '4th gen', '5GHz'),
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1906':
        ('iPad', '4th gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1503':
        ('iPad', '4th gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1503':
        ('iPad', '4th gen', '2.4GHz'),

    # iPad Air 1st gen with iOS 9
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e708|oui:apple':
        ('iPad', 'Air 1st gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e708|oui:apple':
        ('iPad', 'Air 1st gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e708|oui:apple':
        ('iPad', 'Air 1st gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1805|oui:apple':
        ('iPad', 'Air 1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1805|oui:apple':
        ('iPad', 'Air 1st gen', '2.4GHz'),

    # iPad Air 1st gen with iOS 10
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e708':
        ('iPad', 'Air 1st gen', '5GHz'),
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e708':
        ('iPad', 'Air 1st gen', '5GHz'),
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,127,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e708,extcap:000008':
        ('iPad', 'Air 1st gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1805':
        ('iPad', 'Air 1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1805':
        ('iPad', 'Air 1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1805,extcap:000008':
        ('iPad', 'Air 1st gen', '2.4GHz'),

    # iPad Air 2nd gen with iOS 9. 5GHz signatures identical to iPhone 6s, use name to distinguish them.
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1502,extcap:0000000000000040|oui:apple':
        ('iPad', 'Air 2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1502,extcap:0000000000000040|oui:apple':
        ('iPad', 'Air 2nd gen', '2.4GHz'),

    # iPad Air 2nd gen with iOS 10. 5GHz signatures identical to iPhone 6s, use name to distinguish them.
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400000000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400080000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400080000000040|name:ipad':
        ('iPad', 'Air 2nd gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1502,extcap:0000000000000040':
        ('iPad', 'Air 2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1502,extcap:0000000000000040':
        ('iPad', 'Air 2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1502,extcap:0400080000000040':
        ('iPad', 'Air 2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1502,extcap:0400080000000040':
        ('iPad', 'Air 2nd gen', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1807|oui:apple':
        ('iPad Mini', '1st gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1807|oui:apple':
        ('iPad Mini', '1st gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1605|oui:apple':
        ('iPad Mini', '1st gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1605|oui:apple':
        ('iPad Mini', '1st gen', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e606|oui:apple':
        ('iPad Mini', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e606|oui:apple':
        ('iPad Mini', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,127,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e606,extcap:000008|oui:apple':
        ('iPad Mini', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1603|oui:apple':
        ('iPad Mini', '2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1603|oui:apple':
        ('iPad Mini', '2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1403|oui:apple':
        ('iPad Mini', '2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1403,extcap:000008|oui:apple':
        ('iPad Mini', '2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1403|oui:apple':
        ('iPad Mini', '2nd gen', '2.4GHz'),

    # iPad Mini 3rd gen with iOS 8.4
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,127,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e001,extcap:000008|oui:apple':
        ('iPad Mini', '3rd gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1401|oui:apple':
        ('iPad Mini', '3rd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1401,extcap:000008|oui:apple':
        ('iPad Mini', '3rd gen', '2.4GHz'),

    # iPad Mini 3rd gen with iOS 9, 10.0, and 10.1
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e001|oui:apple':
        ('iPad Mini', '3rd gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01fe,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff,txpow:e001|oui:apple':
        ('iPad Mini', '3rd gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1201|oui:apple':
        ('iPad Mini', '3rd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:01bc,htagg:1b,htmcs:0000ffff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff,txpow:1201|oui:apple':
        ('iPad Mini', '3rd gen', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad Mini', '4th gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|name:ipad':
        ('iPad Mini', '4th gen', '5GHz'),

    'wifi4|probe:0,1,3,50|assoc:0,1,48,50|oui:apple':
        ('iPhone 1', '', '2.4GHz'),

    'wifi4|probe:0,1,3,50|assoc:0,1,48,50,221(0050f2,2)|oui:apple':
        ('iPhone 3G', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,221(001018,2)|assoc:0,1,48,50,221(001018,2),221(0050f2,2)|oui:apple':
        ('iPod Touch 2nd gen or iPhone 3GS', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:1800,htagg:1b,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1800,htagg:1b,htmcs:000000ff|oui:apple':
        ('iPhone 4', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff|oui:apple':
        ('iPhone 4s', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0100,htagg:19,htmcs:000000ff|oui:apple':
        ('iPhone 4s', '', '2.4GHz'),

    # iPhone 5 with iOS 9 and prior.
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1504|oui:apple':
        ('iPhone 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1504|oui:apple':
        ('iPhone 5', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1403|oui:apple':
        ('iPhone 5', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1403|oui:apple':
        ('iPhone 5', '', '2.4GHz'),

    # iPhone 5 with iOS 10.
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1504':
        ('iPhone 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1504':
        ('iPhone 5', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1403':
        ('iPhone 5', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1403':
        ('iPhone 5', '', '2.4GHz'),

    # iPhone 5c with iOS 9.
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1805|oui:apple':
        ('iPhone 5c', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1805|oui:apple':
        ('iPhone 5c', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1805|oui:apple':
        ('iPhone 5c', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,127,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1805,extcap:000008|oui:apple':
        ('iPhone 5c', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1704|oui:apple':
        ('iPhone 5c', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1704|oui:apple':
        ('iPhone 5c', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1704|oui:apple':
        ('iPhone 5c', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1704,extcap:000008|oui:apple':
        ('iPhone 5c', '', '2.4GHz'),

    # iPhone 5c with iOS 10.
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1805':
        ('iPhone 5c', '', '5GHz'),
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,127,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1805,extcap:000008':
        ('iPhone 5c', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1704,extcap:000008':
        ('iPhone 5c', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1704':
        ('iPhone 5c', '', '2.4GHz'),

    # iPhone 5s with iOS 9 and prior.
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1603|oui:apple':
        ('iPhone 5s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1603|oui:apple':
        ('iPhone 5s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1603|oui:apple':
        ('iPhone 5s', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1805|oui:apple':
        ('iPhone 5s', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1805|oui:apple':
        ('iPhone 5s', '', '2.4GHz'),

    # iPhone 5s with iOS 10.
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1603':
        ('iPhone 5s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1603':
        ('iPhone 5s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,45,127,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1603,extcap:000008':
        ('iPhone 5s', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1805':
        ('iPhone 5s', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1805':
        ('iPhone 5s', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:0100,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1805':
        ('iPhone 5s', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000804|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,51),221(0050f2,2),221(0017f2,10),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1805,extcap:000008':
        ('iPhone 5s', '', '2.4GHz'),

    # iPhone 6/6+ with iOS 9 and prior.
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6/6+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6/6+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(00904c,51),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6/6+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(00904c,51),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6/6+', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1302,extcap:0000000000000040|oui:apple':
        ('iPhone 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1302,extcap:0000000000000040|oui:apple':
        ('iPhone 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(00904c,51),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1302,extcap:0000000000000040|oui:apple':
        ('iPhone 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0400000000000040|oui:apple':
        ('iPhone 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0000000000000040|oui:apple':
        ('iPhone 6+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0000000000000040|oui:apple':
        ('iPhone 6+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(00904c,51),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0000000000000040|oui:apple':
        ('iPhone 6+', '', '2.4GHz'),

    # iPhone 6 with iOS 10 changed txpow, now distinguishable from iPhone 6+.
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1202,extcap:0400000000000040':
        ('iPhone 6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1202,extcap:0400000000000040':
        ('iPhone 6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1202,extcap:0400080000000040':
        ('iPhone 6', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1302,extcap:0000000000000040':
        ('iPhone 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1302,extcap:0000000000000040':
        ('iPhone 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1302,extcap:0400080000000040':
        ('iPhone 6', '', '2.4GHz'),

    # iPhone 6+ with iOS 10 changed txpow, now distinguishable from iPhone 6.
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1302,extcap:0400000000000040':
        ('iPhone 6+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1302,extcap:0400000000000040':
        ('iPhone 6+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1302,extcap:0400080000000040':
        ('iPhone 6+', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0000000000000040':
        ('iPhone 6+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0000000000000040':
        ('iPhone 6+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0400080000000040':
        ('iPhone 6+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0400080000000040':
        ('iPhone 6+', '', '2.4GHz'),

    # iPhone 6s/6s+ with iOS 10 changed txpow, now distinguishable on 5GHz. 2.4GHz signatures are identical.
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400000000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400000000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400080000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400080000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400080000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400080000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400000000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1302,extcap:0400000000000040':
        ('iPhone 6s', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0400000000000040':
        ('iPhone 6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0400000000000040':
        ('iPhone 6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0400080000000040':
        ('iPhone 6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0400080000000040':
        ('iPhone 6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0400080000000040':
        ('iPhone 6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0400080000000040':
        ('iPhone 6s+', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0400080000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0400080000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0400080000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0400080000000040':
        ('iPhone 6s/6s+', '', '2.4GHz'),

    # iOS 9 and earlier signature is identical between iPhone 6s and 6s+
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400088400000040|assoc:0,1,33,36,48,70,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f815832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e002,extcap:0400000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:000000ff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(00904c,51),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(00904c,51),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0400088400000040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:000000ff,txpow:1202,extcap:0000000000000040|oui:apple':
        ('iPhone 6s/6s+', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000884|assoc:0,1,33,36,48,70,54,45,127,191,199,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9,extcap:000008':
        ('iPhone 7', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00000884|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9,extcap:000008':
        ('iPhone 7', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f817032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00000884|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9,extcap:000008':
        ('iPhone 7', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f801032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000884|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f813032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9,extcap:000008':
        ('iPhone 7', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000884|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f813032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9,extcap:000008':
        ('iPhone 7', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f803032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000884|assoc:0,1,33,36,48,70,45,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9':
        ('iPhone 7', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000884|assoc:0,1,33,36,48,70,45,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9':
        ('iPhone 7', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f817032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00000884|assoc:0,1,33,36,48,45,191,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f817032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:13f9':
        ('iPhone 7+', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:00000884|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:13f9,extcap:000008':
        ('iPhone 7/7+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:00000884|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:13f9,extcap:000008':
        ('iPhone 7/7+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0000088400000040|assoc:0,1,50,33,36,48,70,45,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:13f9':
        ('iPhone 7/7+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:00000884|assoc:0,1,50,33,36,48,70,45,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:13f9':
        ('iPhone 7/7+', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1405,extcap:0000000000000040':
        ('iPhone 8', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,vhtcap:0f817032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000080400000040|assoc:0,1,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,txpow:1405,extcap:0000000000000040':
        ('iPhone 8', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000080400000040|assoc:0,1,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,txpow:1405,extcap:0000000000000040':
        ('iPhone 8', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1405,extcap:0000080000000040':
        ('iPhone 8', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1405,extcap:0000000000000040':
        ('iPhone 8', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f813032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1405,extcap:0000080000000040':
        ('iPhone 8', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f813032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1405,extcap:0000080000000040':
        ('iPhone 8', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1405,extcap:0000080000000040':
        ('iPhone 8', '', '5GHz'),
    # iPhone 8 2.4GHz has the same signature as iPhone X, below.

    'wifi4|probe:0,1,45,127,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,vhtcap:0f817032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000080400000040|assoc:0,1,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,txpow:1505,extcap:0000000000000040':
        ('iPhone X', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f817032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000080400000040|assoc:0,1,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,txpow:1505,extcap:0000000000000040':
        ('iPhone X', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000080400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1505,extcap:0000000000000040':
        ('iPhone X', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,vhtcap:0f817032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000080400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1505,extcap:0000000000000040':
        ('iPhone X', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f813032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1505,extcap:0000080000000040':
        ('iPhone X', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f801032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1505,extcap:0000080000000040':
        ('iPhone X', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f813032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1505,extcap:0000080000000040':
        ('iPhone X', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(0017f2,10),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f807032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088400000040|assoc:0,1,33,36,48,45,127,191,221(0017f2,10),221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f811032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1505,extcap:0000080000000040':
        ('iPhone X', '', '5GHz'),

    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000080400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000080000000040':
        ('iPhone 8/X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0000080400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000000000000040':
        ('iPhone 8/X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000080400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000000000000040':
        ('iPhone 8/X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:506f,htagg:17,htmcs:000000ff,extcap:0000088400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000080000000040':
        ('iPhone 8/X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0017f2,10),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:000000ff,extcap:0000080400000040|assoc:0,1,50,33,36,48,45,127,221(0017f2,10),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000080000000040':
        ('iPhone 8/X', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0400088400000040|assoc:0,1,33,36,45,127,221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,txpow:e002,extcap:000008|oui:apple':
        ('iPhone SE', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0400088400000040|assoc:0,1,50,33,36,45,127,221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:1402,extcap:0000000000000040|oui:apple':
        ('iPhone SE', '', '2.4GHz'),

    'wifi4|probe:0,1,3,50|assoc:0,1,48,50|os:ipodtouch1':
        ('iPod Touch', '1st gen', '2.4GHz'),

    'wifi4|probe:0,1,50,221(001018,2)|assoc:0,1,48,50,221(001018,2),221(0050f2,2)|name:ipod':
        ('iPod Touch', '3rd gen', '2.4GHz'),

    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:180c,htagg:1b,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:180c,htagg:1b,htmcs:000000ff|oui:apple':
        ('iPod Touch', '4th gen', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1504|oui:apple':
        ('iPod Touch', '5th gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0020,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,50,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1504|oui:apple':
        ('iPod Touch', '5th gen', '5GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,70,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1706|oui:apple':
        ('iPod Touch', '5th gen', '2.4GHz'),
    'wifi4|probe:0,1,45,127,107,221(001018,2),221(00904c,51),221(0050f2,8),htcap:0062,htagg:1a,htmcs:000000ff,extcap:00000004|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1706|oui:apple':
        ('iPod Touch', '5th gen', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:0020,htagg:17,htmcs:000000ff|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01|oui:lava':
        ('Lava Pixel', '', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:PixelV1|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Lava Pixel', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a0201000040|oui:motorola':
        ('Lenovo Phab 2', 'Pro', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201000040|oui:motorola':
        ('Lenovo Phab 2', 'Pro', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201000040|oui:motorola':
        ('Lenovo Phab 2', 'Pro', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:140d,extcap:00000a0201000000|oui:motorola':
        ('Lenovo Phab 2', 'Pro', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0201000000|oui:motorola':
        ('Lenovo Phab 2', 'Pro', '2.4GHz'),

    'wifi4|probe:0,1,3,45,127,191,221(001018,2),221(00904c,51),221(0050f2,8),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000080000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e001,extcap:0000000000000040|oui:lg':
        ('LG G2', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000080000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:11ff|oui:lg':
        ('LG G2', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000080000000040|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:11ff|oui:lg':
        ('LG G2', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040|assoc:0,1,33,36,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:170d,extcap:00000a8201400040|oui:lg':
        ('LG G3', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040|assoc:0,1,33,36,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:170d,extcap:00000a8201400040|oui:lg':
        ('LG G3', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,33,36,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:170d,extcap:00000a8201400040|oui:lg':
        ('LG G3', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040|oui:lg':
        ('LG G3', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040|oui:lg':
        ('LG G3', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:000000800040|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a8201400040|oui:lg':
        ('LG G3', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:000000800040|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a8201400000|oui:lg':
        ('LG G3 or K7', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:000000800040|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a8201400000|oui:lg':
        ('LG G3 or K7', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,extcap:000000800040|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a8201400000|oui:lg':
        ('LG G3 or K7', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a8201400000|oui:lg':
        ('LG G3 or K7', '', '2.4GHz'),

    # new 5GHz txpow:e003 signatures go in the 'LG G4 or Nexus 5' section below
    'wifi4|probe:0,1,3,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1d01,extcap:0000008001400040|oui:lg':
        ('LG G4', '', '5GHz'),
    'wifi4|probe:0,1,3,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,70,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1d01,extcap:0000008001400040|oui:lg':
        ('LG G4', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1d01,extcap:0000088001400040|oui:lg':
        ('LG G4', '', '5GHz'),
    'wifi4|probe:0,1,3,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1d01,extcap:0000088001400040|oui:lg':
        ('LG G4', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1203,extcap:000000800140|oui:lg':
        ('LG G4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,4),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1203,extcap:0000088001400040|oui:lg':
        ('LG G4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,70,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1203,extcap:000000800140|oui:lg':
        ('LG G4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1001,extcap:000000800140|oui:lg':
        ('LG G4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,4),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1001,extcap:0000088001400040|oui:lg':
        ('LG G4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,4),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1001,extcap:0000088001400040|oui:lg':
        ('LG G4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,70,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1001,extcap:000000800140|oui:lg':
        ('LG G4', '', '2.4GHz'),

    # some LG G4s use the same txpow as Nexus 5, indistinguishable in 5GHz band
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e003,extcap:0000088001400040|oui:lg':
        ('LG G4 or Nexus 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,70,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e003,extcap:0000008001400040|oui:lg':
        ('LG G4 or Nexus 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e003,extcap:0000000000000040|oui:lg':
        ('LG G4 or Nexus 5', '', '5GHz'),
    'wifi4|probe:0,1,3,45,127,191,221(001018,2),221(00904c,51),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e003,extcap:0000000000000040|oui:lg':
        ('LG G4 or Nexus 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|assoc:0,1,33,36,45,127,191,221(001018,2),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e003,extcap:0000000000000040|oui:lg':
        ('LG G4 or Nexus 5', '', '5GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001632,64),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e003,extcap:0000080000000040|oui:lg':
        ('LG G5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,191,221(00904c,4),221(001632,64),221(001018,2),221(0050f2,2),htcap:0063,htagg:17,htmcs:000000ff,vhtcap:0f805032,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e003,extcap:0000000000000040|oui:lg':
        ('LG G5', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,221(00904c,4),221(001632,64),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:0f03,extcap:0000080000000040|oui:lg':
        ('LG G5', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:0021,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,50,33,36,48,70,45,127,221(001632,64),221(001018,2),221(0050f2,2),htcap:0021,htagg:17,htmcs:000000ff,txpow:0f03,extcap:0000000000000040|oui:lg':
        ('LG G5', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:LGL16C|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('LG Lucky', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:LGMS395|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:lg':
        ('LG Optimus F60', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:lg':
        ('LG Optimus', 'L7', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:_|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:lg':
        ('LG Optimus', 'L7', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:lg':
        ('LG Optimus', 'L7', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:LGMS323|assoc:0,1,50,48,45,221(0050f2,2),221(004096,3),htcap:012c,htagg:03,htmcs:000000ff':
        ('LG Optimus', 'L70', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:LG_D415|assoc:0,1,50,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0200000000':
        ('LG Optimus', 'L90', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:LG_D415|assoc:0,1,50,48,45,221(0050f2,2),221(004096,3),htcap:012c,htagg:03,htmcs:000000ff':
        ('LG Optimus', 'L90', '2.4GHz'),

    'wifi4|probe:0,1,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,wps:LG_V400|assoc:0,1,33,36,48,70,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a0200000000':
        ('LG Pad', 'v400', '5GHz'),

    'wifi4|probe:0,1,45,191,221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,33,36,48,45,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009|os:lgtv':
        ('LG Smart TV', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,wps:_|assoc:0,1,33,36,48,45,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009|os:lgtv':
        ('LG Smart TV', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000000000000040,wps:_|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209|os:lgtv':
        ('LG Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:11ac,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:11ac,htagg:16,htmcs:0000ffff,txpow:140a,extcap:0000000000000040|os:lgtv':
        ('LG Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,wps:_|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209|os:lgtv':
        ('LG Smart TV', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:LGLS660|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('LG Tribute', '', '2.4GHz'),

    # LHA19
    'wifi4|probe:0,1,50,45,htcap:0120,htagg:01,htmcs:000000ff|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:0120,htagg:01,htmcs:000000ff,extcap:01|oui:lifx':
        ('LIFX smart bulb', '', '2.4GHz'),
    'wifi4|probe:0,1,50|assoc:0,1,50,48,221(0050f2,2)|oui:lifx':
        ('LIFX smart bulb', '', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:Micromax_D303|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Micromax Bolt', '', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:Micromax_AQ4501|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Micromax Canvas', 'A1', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:Micromax_A106|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Micromax Canvas Unite', '2', '2.4GHz'),

    'wifi4|probe:0,1,50,45,htcap:102c,htagg:1f,htmcs:000000ff|assoc:0,1,50,48,221(0050f2,2),45,htcap:102c,htagg:1f,htmcs:000000ff|oui:micromax':
        ('Micromax Q335', '', '2.4GHz'),

    'wifi4|probe:0,1,45,50,htcap:0102,htagg:03,htmcs:0000ffff|assoc:0,1,48,221(0050f2,2),45,htcap:010e,htagg:03,htmcs:0000ffff|oui:microsoft':
        ('Microsoft Surface', 'RT', '5GHz'),
    'wifi4|probe:0,1,45,50,htcap:0102,htagg:03,htmcs:0000ffff|assoc:0,1,33,36,48,221(0050f2,2),45,htcap:010e,htagg:03,htmcs:0000ffff|oui:microsoft':
        ('Microsoft Surface', 'RT', '5GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:0102,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,221(0050f2,2),45,htcap:012c,htagg:03,htmcs:0000ffff|oui:microsoft':
        ('Microsoft Surface', 'RT', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0200000000|oui:motorola':
        ('Moto E', '2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a0200000000|oui:motorola':
        ('Moto E', '2nd gen', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:160d|oui:motorola':
        ('Moto G', '3rd gen', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:motorola':
        ('Moto G or Moto X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:motorola':
        ('Moto G or Moto X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:motorola':
        ('Moto G or Moto X', '', '2.4GHz'),
    # Proprietary VHT rates on 2.4GHz
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),191,htcap:012c,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:motorola':
        ('Moto G or Moto X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),191,htcap:012c,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:motorola':
        ('Moto G or Moto X', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a02|oui:motorola':
        ('Moto X', '1st gen', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31805120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a02|oui:motorola':
        ('Moto X', '1st gen', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,33,36,48,45,221(0050f2,2),191,127,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a02|oui:motorola':
        ('Moto X', '1st gen', '5GHz'),

    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|oui:motorola':
        ('Moto X', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|oui:motorola':
        ('Moto X', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:120d,extcap:0000000000000040|oui:motorola':
        ('Moto X', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|oui:motorola':
        ('Moto X', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:120d,extcap:0000000000000040|oui:motorola':
        ('Moto X', '2nd gen', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:0d0d|oui:motorola':
        ('Moto X', '2nd gen', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:0d0d|oui:motorola':
        ('Moto X', '2nd gen', '2.4GHz'),

    'wifi4|probe:0,1,127,45,htcap:01ef,htagg:03,htmcs:0000ffff,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004040|oui:motorola':
        ('Moto X', 'Style', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004040|oui:motorola':
        ('Moto X', 'Style', '5GHz'),
    'wifi4|probe:0,1,50,127,45,htcap:01ef,htagg:03,htmcs:0000ffff,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:00000a020100000040|oui:motorola':
        ('Moto X', 'Style', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:00000a020100000040|oui:motorola':
        ('Moto X', 'Style', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:082c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:082c,htagg:1b,htmcs:000000ff,txpow:0a08|oui:motorola':
        ('Motorola Xoom', '', '5GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:182c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:182c,htagg:1b,htmcs:000000ff,txpow:0e08|oui:motorola':
        ('Motorola Xoom', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000802|oui:motorola':
        ('Moto Z', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,33,36,48,70,45,221(0050f2,2),htcap:016e,htagg:03,htmcs:000000ff,txpow:100d|oui:motorola':
        ('Moto Z', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),htcap:016e,htagg:03,htmcs:000000ff|oui:motorola':
        ('Moto Z', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000802|oui:motorola':
        ('Moto Z', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),htcap:016e,htagg:03,htmcs:000000ff|oui:motorola':
        ('Moto Z', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000802|oui:motorola':
        ('Moto Z', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000802|oui:motorola':
        ('Moto Z', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:120d|oui:motorola':
        ('Moto Z', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000802|oui:motorola':
        ('Moto Z', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:120d|oui:motorola':
        ('Moto Z', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,191,221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:03800032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000008001000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000008001000040|oui:nest':
        ('Nest Cam', 'IQ', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000008001000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000008001000040|oui:nest':
        ('Nest Cam', 'IQ', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000008001000040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1307,extcap:0000008001000040|oui:nest':
        ('Nest Cam', 'IQ', '2.4GHz'),

    'wifi4|probe:0,1,45,htcap:106e,htagg:01,htmcs:000000ff|assoc:0,1,45,33,36,48,221(0050f2,2),htcap:106e,htagg:01,htmcs:000000ff,txpow:1000|oui:nest':
        ('Nest Cam', 'Indoor', '5GHz'),
    'wifi4|probe:0,1,50,45,htcap:002c,htagg:01,htmcs:000000ff|assoc:0,1,50,45,48,221(0050f2,2),htcap:002c,htagg:01,htmcs:000000ff|oui:nest':
        ('Nest Cam', 'Indoor', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:110c,htagg:18,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:18,htmcs:000000ff|oui:nest':
        ('Nest Protect', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,htcap:0130,htagg:18,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:013c,htagg:18,htmcs:000000ff|oui:nest':
        ('Nest Thermostat', 'v1 or v2', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:0f09|oui:nest':
        ('Nest Thermostat', 'v3', '5GHz'),
    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:0f09|oui:nest':
        ('Nest Thermostat', 'v3', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:150b|oui:nest':
        ('Nest Thermostat', 'v3', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:1209|oui:nest':
        ('Nest Thermostat', 'v4', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff,txpow:140b|oui:nest':
        ('Nest Thermostat', 'v4', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_4|assoc:0,1,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('Nexus 4', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,vhtcap:31811120,vhtrxmcs:01b2fffc,vhttxmcs:01b2fffc,wps:Nexus_4|assoc:0,1,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('Nexus 4', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,vhtcap:31811120,vhtrxmcs:01b2fffc,vhttxmcs:01b2fffc,wps:Nexus_4|assoc:0,1,33,36,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:130d':
        ('Nexus 4', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_4|assoc:0,1,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 4', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,vhtcap:31811120,vhtrxmcs:01b2fffc,vhttxmcs:01b2fffc,wps:Nexus_4|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('Nexus 4', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_4|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a02':
        ('Nexus 4', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a02|oui:lg':
        ('Nexus 4', '', '5GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),191,221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,vhtcap:31811120,vhtrxmcs:01b2fffc,vhttxmcs:01b2fffc,wps:Nexus_4|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('Nexus 4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_4|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('Nexus 4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:lg':
        ('Nexus 4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:lg':
        ('Nexus 4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_4|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_4|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:lg':
        ('Nexus 4', '', '2.4GHz'),

    # new 5GHz txpow:e003 signatures go in the 'LG G4 or Nexus 5' section above
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1303|oui:lg':
        ('Nexus 5', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(001018,2),221(00904c,51),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1303|oui:lg':
        ('Nexus 5', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1303,extcap:0000000000000040|oui:lg':
        ('Nexus 5', '', '2.4GHz'),

    'wifi4|probe:0,1,127,45,191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a0201000040|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:0000000000000040|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,127,extcap:00000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:000000000000004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,127,45,191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,127,45,191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,127,45,191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,txpow:1e08,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,127,45,191,htcap:01ad,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,txpow:1e08,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,127,extcap:00000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,txpow:1e08,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:000000000000004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,txpow:1e08,extcap:000000000000004080|oui:lg':
        ('Nexus 5X', '', '5GHz'),
    'wifi4|probe:0,1,50,127,45,191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a0201000040|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:0000000000000000|oui:lg':
        ('Nexus 5X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:000000000000000080|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:000000000000000080|oui:lg':
        ('Nexus 5X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,127,45,191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004080|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:000000000000000080|oui:lg':
        ('Nexus 5X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,127,45,191,htcap:01ef,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,txpow:1e08,extcap:000000000000000080|oui:lg':
        ('Nexus 5X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,127,45,191,htcap:01ad,htagg:03,htmcs:0000ffff,vhtcap:338061b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a020100004080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,txpow:1e08,extcap:000000000000000080|oui:lg':
        ('Nexus 5X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,127,extcap:00000a020100004080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,txpow:1e08,extcap:000000000000000080|oui:lg':
        ('Nexus 5X', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:01ad,htagg:03,htmcs:0000ffff,extcap:000000000000000080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:01ad,htagg:03,htmcs:0000ffff,txpow:1e08,extcap:000000000000000080|oui:lg':
        ('Nexus 5X', '', '2.4GHz'),

    'wifi4|probe:0,1,45,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140,wps:Nexus_6|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:000008800140':
        ('Nexus 6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140,wps:Nexus_6|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:000008800140':
        ('Nexus 6', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,wps:Nexus_6|assoc:0,1,33,36,48,45,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009':
        ('Nexus 6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040,wps:Nexus_6|assoc:0,1,33,36,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000088001400040':
        ('Nexus 6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140,wps:Nexus_6|assoc:0,1,33,36,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:000008800140':
        ('Nexus 6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040,wps:Nexus_6|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000088001400040':
        ('Nexus 6', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040,wps:Nexus_6|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140':
        ('Nexus 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140,wps:Nexus_6|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140':
        ('Nexus 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140,wps:Nexus_6|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140':
        ('Nexus 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,wps:Nexus_6|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209':
        ('Nexus 6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140,wps:Nexus_6|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:140b,extcap:000008800140':
        ('Nexus 6', '', '2.4GHz'),

    'wifi4|probe:0,1,45,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,wps:Nexus_6P|assoc:0,1,33,36,48,45,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002':
        ('Nexus 6P', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040,wps:Nexus_6P|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0000088001400040':
        ('Nexus 6P', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040,wps:Nexus_6P|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000088001400040':
        ('Nexus 6P', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040,wps:Nexus_6P|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1302,extcap:0000088001400040':
        ('Nexus 6P', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,wps:Nexus_6P|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1302':
        ('Nexus 6P', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,wps:Nexus_6P|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402':
        ('Nexus 6P', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff|oui:asus':
        ('Nexus 7', '2012 edition', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02|oui:asus':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02|oui:asus':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:1e0d,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:1e0d,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:1e0d,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:1e0d,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:1e0d,extcap:00000a02|oui:asus':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,33,36,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:1e0d,extcap:00000a02|oui:asus':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '5GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_7|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:asus':
        ('Nexus 7', '2013 edition', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:asus':
        ('Nexus 7', '2013 edition', '2.4GHz'),
    'wifi4|probe:0,1,50,45,htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:asus':
        ('Nexus 7', '2013 edition', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,wps:Nexus_7|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff':
        ('Nexus 7', '2013 edition', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,221(0050f2,4),221(506f9a,9),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02,wps:Nexus_7|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02':
        ('Nexus 7', '2013 edition', '2.4GHz'),

    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140,wps:Nexus_9|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:000008800140':
        ('Nexus 9', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,wps:Nexus_9|assoc:0,1,33,36,48,45,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009':
        ('Nexus 9', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040,wps:Nexus_9|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000088001400040':
        ('Nexus 9', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140,wps:Nexus_9|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e20b,extcap:000008800140':
        ('Nexus 9', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040,wps:Nexus_9|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1309,extcap:000008800140':
        ('Nexus 9', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140,wps:Nexus_9|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:150b,extcap:000008800140':
        ('Nexus 9', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140,wps:Nexus_9|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1309,extcap:000008800140':
        ('Nexus 9', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,wps:Nexus_9|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1309':
        ('Nexus 9', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:01fe,htagg:1b,htmcs:0000ffff|assoc:0,1,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff|oui:samsunge':
        ('Nexus 10', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,4),221(506f9a,9),221(001018,2),221(00904c,51),htcap:01fe,htagg:1b,htmcs:0000ffff,wps:Nexus_10|assoc:0,1,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff':
        ('Nexus 10', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:01bc,htagg:1b,htmcs:0000ffff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff|oui:samsunge':
        ('Nexus 10', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),221(00904c,51),htcap:01bc,htagg:1b,htmcs:0000ffff,wps:Nexus_10|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff':
        ('Nexus 10', '', '2.4ghz'),

    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040,wps:Nexus_Player|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000088001400040':
        ('Nexus Player', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140,wps:Nexus_Player|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:000008800140':
        ('Nexus Player', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140,wps:Nexus_Player|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140':
        ('Nexus Player', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040,wps:Nexus_Player|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140':
        ('Nexus Player', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,51,127,htcap:012c,htagg:1b,htmcs:000000ff,extcap:0100000000000040|assoc:0,1,48,50,221(0050f2,2),45,51,127,htcap:012c,htagg:1b,htmcs:000000ff,extcap:0100000000000040|os:windows-phone':
        ('Nokia Lumia', '635', '2.4GHz'),
    'wifi4|probe:0,1,50,45,htcap:012c,htagg:1b,htmcs:000000ff|assoc:0,1,48,50,221(0050f2,2),45,51,127,htcap:012c,htagg:1b,htmcs:000000ff,extcap:0100000000000040|os:windows-phone':
        ('Nokia Lumia', '635', '2.4GHz'),

    'wifi4|probe:0,1,45,htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,48,45,221(0050f2,2),htcap:016e,htagg:03,htmcs:000000ff|os:windows-phone':
        ('Nokia Lumia', '920', '5GHz'),
    'wifi4|probe:0,1,50,45,htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|os:windows-phone':
        ('Nokia Lumia', '920', '2.4GHz'),

    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000008001000040,wps:SHIELD_Android_TV|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000008001000040':
        ('NVidia SHIELD', 'Android TV', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(0050f2,4),221(506f9a,9),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040,wps:SHIELD_Android_TV|assoc:0,1,33,36,48,70,45,127,191,221(00904c,51),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000088001400040':
        ('NVidia SHIELD', 'Android TV', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000008001000040,wps:SHIELD_Android_TV|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1207,extcap:0000008001000040':
        ('NVidia SHIELD', 'Android TV', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(0050f2,4),221(506f9a,9),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040,wps:SHIELD_Android_TV|assoc:0,1,50,33,36,48,70,45,127,221(00904c,51),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1207,extcap:0000088001400040':
        ('NVidia SHIELD', 'Android TV', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:01fe,htagg:1b,htmcs:0000ffff|assoc:0,1,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01fe,htagg:1b,htmcs:0000ffff|oui:nvidia':
        ('NVidia SHIELD', 'Portable', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:01bc,htagg:1b,htmcs:0000ffff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:01bc,htagg:1b,htmcs:0000ffff|oui:nvidia':
        ('NVidia SHIELD', 'Portable', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a0200000000|oui:oneplus':
        ('OnePlus', 'X', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:000000000000004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1e08,extcap:000000000000004080|oui:oneplus':
        ('OnePlus', '2', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:000000000000004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:000000000000004080|oui:oneplus':
        ('OnePlus', '2', '5GHz'),
    'wifi4|probe:0,1,127,45,191,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:338001b2,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:000000000000004080|oui:oneplus':
        ('OnePlus', '2', '5GHz'),
    'wifi4|probe:0,1,127,45,191,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:338021b2,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:00000a0201|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1e08,extcap:000000000000004080|oui:oneplus':
        ('OnePlus', '2', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:000000000000004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:000000000000004080|oui:oneplus':
        ('OnePlus', '2', '5GHz'),
    'wifi4|probe:0,1,127,45,191,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:338061b2,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:000000000000004080|oui:oneplus':
        ('OnePlus', '2', '5GHz'),
    'wifi4|probe:0,1,50,127,45,191,htcap:016f,htagg:03,htmcs:000000ff,vhtcap:338001b2,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012d,htagg:03,htmcs:000000ff,extcap:000000000000000080|oui:oneplus':
        ('OnePlus', '2', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012d,htagg:03,htmcs:000000ff,extcap:000000000000000080|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012d,htagg:03,htmcs:000000ff,extcap:000000000000000080|oui:oneplus':
        ('OnePlus', '2', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,127,htcap:012d,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012d,htagg:03,htmcs:000000ff,extcap:000000000000000080|oui:oneplus':
        ('OnePlus', '2', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:A11w|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Oppo Joy', '3', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:R831K|assoc:0,1,50,45,127,221(0050f2,2),48,htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('Oppo Neo', '3', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,4),htcap:11ee,htagg:02,htmcs:0000ffff,wps:WPS_STA|assoc:0,1,33,36,48,221(0050f2,2),45,127,htcap:11ee,htagg:02,htmcs:0000ffff,txpow:0b00,extcap:01|os:panasonictv':
        ('Panasonic TV', '', '5GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,4),htcap:01ac,htagg:02,htmcs:0000ffff,wps:WPS_STA|assoc:0,1,50,221(0050f2,2),45,127,htcap:01ac,htagg:02,htmcs:0000ffff,extcap:01|os:panasonictv':
        ('Panasonic TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,48|assoc:0,1,33,36,50,221(0050f2,2),45,221(00037f,1),221(00037f,4),48,htcap:1004,htagg:1b,htmcs:0000ffff,txpow:0f0f|os:panasonictv':
        ('Panasonic TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,4),htcap:01ad,htagg:02,htmcs:0000ffff,wps:WPS_SUPPLICANT_STATION|assoc:0,1,50,45,48,221(0050f2,2),htcap:01ad,htagg:02,htmcs:0000ffff|os:panasonictv':
        ('Panasonic TV', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:040000000000004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,txpow:1e08,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,txpow:1e08,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,txpow:1e08,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:01ef,htagg:df,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:040000000000004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339031b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:040000000000004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339031b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339031b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:339071b2,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|oui:htc':
        ('Pixel Phone', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:01ad,htagg:1f,htmcs:0000ffff,extcap:040000000000000080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:01ad,htagg:1f,htmcs:0000ffff,txpow:1e08,extcap:04000a020100000080|oui:htc':
        ('Pixel Phone', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:01ad,htagg:1f,htmcs:0000ffff,extcap:040000000000000080|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:1f,htmcs:0000ffff,extcap:04000a020100000080|oui:htc':
        ('Pixel Phone', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,191,221(0050f2,8),3,127,htcap:01ef,htagg:df,htmcs:0000ffff,vhtcap:33800192,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:1f,htmcs:0000ffff,extcap:04000a020100000080|oui:htc':
        ('Pixel Phone', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,191,221(0050f2,8),3,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:33800192,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:01ad,htagg:1f,htmcs:0000ffff,extcap:04000a020100000080|oui:htc':
        ('Pixel Phone', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,191,221(0050f2,8),3,127,htcap:01ef,htagg:1f,htmcs:0000ffff,vhtcap:33800192,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:04000a020100004080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:01ad,htagg:1f,htmcs:0000ffff,txpow:1e08,extcap:04000a020100000080|oui:htc':
        ('Pixel Phone', '', '2.4GHz'),

    'wifi4|probe:0,1|assoc:0,1,221(005043,1)|os:playstation':
        ('Playstation', '3', '2.4GHz'),

    'wifi4|probe:0,1,50|assoc:0,1,50,48,221(005043,1)|os:playstation':
        ('Playstation', '3 or 4', '2.4GHz'),

    'wifi4|probe:0,1,3,50|assoc:0,1,33,48,50,221(0050f2,2),45,htcap:010c,htagg:03,htmcs:0000ffff,txpow:1209|os:playstation':
        ('Playstation', '4', '2.4GHz'),
    'wifi4|probe:0,1,3,50|assoc:0,1,48,50,221(0050f2,2),45,htcap:112c,htagg:03,htmcs:0000ffff,txpow:0f06|os:playstation':
        ('Playstation', '4', '2.4GHz'),
    'wifi4|probe:0,1,3,50|assoc:0,1,33,48,50,221(0050f2,2),45,htcap:112c,htagg:03,htmcs:0000ffff,txpow:0f06|os:playstation':
        ('Playstation', '4', '2.4GHz'),
    'wifi4|probe:0,1,3,50|assoc:0,1,33,48,50,221(0050f2,2),45,htcap:010c,htagg:03,htmcs:0000ffff,txpow:0f06|os:playstation':
        ('Playstation', '4', '2.4GHz'),
    'wifi4|probe:0,1,3,50|assoc:0,1,221(0050f2,2),45,htcap:012c,htagg:03,htmcs:0000ffff|os:playstation':
        ('Playstation', '4', '2.4GHz'),
    'wifi4|probe:0,1,3,50|assoc:0,1,48,50,221(0050f2,2),45,htcap:012c,htagg:03,htmcs:0000ffff|os:playstation':
        ('Playstation', '4', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,4),221(506f9a,9),221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff,wps:_|assoc:0,1,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff|oui:compal':
        ('Project Tango Devkit', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,4),221(506f9a,9),221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff,wps:_|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff|oui:compal':
        ('Project Tango Devkit', '', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:RCT6303W87DK|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('RCA Viking Tablet', 'RCA 10 Viking Pro', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:RCT6773W42B|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('RCA Voyager Tablet', 'v1', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:RCT6773W42B|assoc:0,1,50,45,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('RCA Voyager Tablet', 'v1', '2.4GHz'),

    # RCA Voyager-II
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:RCT6773W22B|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('RCA Voyager Tablet', 'v2', '2.4GHz'),

    # Roku model 1100, 2500 and LT model 2450
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff|os:roku':
        ('Roku', 'HD or LT', '2.4GHz'),

    # Roku model 1101
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:186e,htagg:1a,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:186e,htagg:1a,htmcs:0000ffff,txpow:1208|os:roku':
        ('Roku', 'HD-XR', '2.4GHz'),

    # Roku Streaming Stick model 3400X
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:187c,htagg:1a,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:187c,htagg:1a,htmcs:0000ffff,txpow:1208|os:roku':
        ('Roku', 'Streaming Stick 3400X', '2.4GHz'),

    # Roku Streaming Stick model 3600
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:19bc,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,50,45,127,221(001018,2),221(0050f2,2),htcap:19bc,htagg:16,htmcs:0000ffff,txpow:140a,extcap:0000000000000040|os:roku':
        ('Roku', 'Streaming Stick 3600', '2.4GHz'),

    # Roku 1 models 2000, 2050, 2100, and XD
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:186e,htagg:1a,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:186e,htagg:1a,htmcs:0000ffff,txpow:1308|os:roku':
        ('Roku', '1', '2.4GHz'),

    # Roku 1 model 2710 and Roku LT model 2700
    'wifi4|probe:0,1,50,3,45,221(001018,2),221(00904c,51),htcap:0020,htagg:1a,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0020,htagg:1a,htmcs:000000ff|os:roku':
        ('Roku', '1 or LT', '2.4GHz'),

    # Roku 2 models 3000, 3050, 3100, and Roku LT model 2400
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff|os:roku':
        ('Roku', '2 or LT', '2.4GHz'),

    # Roku 2 model 2720
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:187c,htagg:1a,htmcs:0000ffff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:187c,htagg:1a,htmcs:0000ffff|os:roku':
        ('Roku', '2', '2.4GHz'),

    # Roku 2 model 4210X
    'wifi4|probe:0,1,50,45,127,221(001018,2),221(00904c,51),htcap:193c,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:193c,htagg:16,htmcs:0000ffff,txpow:140a,extcap:0000000000000040|os:roku':
        ('Roku', '2', '2.4GHz'),

    # Roku 3 model 4230, 4200, 4200X, 4230X, Roku Streaming Stick model 3500, Roku 2 model 4210X
    'wifi4|probe:0,1,45,127,221(001018,2),221(00904c,51),htcap:09bc,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:09bc,htagg:16,htmcs:0000ffff,txpow:100a,extcap:0000000000000040|os:roku':
        ('Roku', '2, 3, TV, or Streaming Stick', '5GHz'),
    'wifi4|probe:0,1,3,45,127,221(001018,2),221(00904c,51),htcap:09bc,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:09bc,htagg:16,htmcs:0000ffff,txpow:100a,extcap:0000000000000040|os:roku':
        ('Roku', '2, 3, TV, or Streaming Stick', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:19bc,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:19bc,htagg:16,htmcs:0000ffff,txpow:140a,extcap:0000000000000040|os:roku':
        ('Roku', '2, 3, TV, or Streaming Stick', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),htcap:193c,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:193c,htagg:16,htmcs:0000ffff,txpow:140a,extcap:0000000000000040|os:roku':
        ('Roku', '2, 3, TV, or Streaming Stick', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(001018,2),221(00904c,51),htcap:19bc,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:19bc,htagg:16,htmcs:0000ffff,txpow:140a,extcap:0000000000000040|os:roku':
        ('Roku', '2, 3, TV, or Streaming Stick', '2.4GHz'),

    # Roku Streaming Stick model 3600
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:187c,htagg:1a,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:187c,htagg:1a,htmcs:0000ffff,txpow:1208|os:roku':
        ('Roku', 'Streaming Stick', '2.4GHz'),

    # Roku 3 model 4230RW
    'wifi4|probe:0,1,45,127,221(001018,2),221(00904c,51),htcap:093c,htagg:16,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:093c,htagg:16,htmcs:0000ffff,txpow:110a,extcap:0000000000000040|os:roku':
        ('Roku', '3', '5GHz'),

    # Roku 4 model 4400 or Roku TV NP-YW
    'wifi4|probe:0,1,45,127,191,221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,191,199,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1109,extcap:0000000000000040|os:roku':
        ('Roku', '4, TV, or Premiere', '5GHz'),
    'wifi4|probe:0,1,45,191,221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,33,36,48,45,191,199,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1109|os:roku':
        ('Roku', '4, TV, or Premiere', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1209|os:roku':
        ('Roku', '4, TV, or Premiere', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1209|os:roku':
        ('Roku', '4, TV, or Premiere', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:0020,htagg:17,htmcs:000000ff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:17,htmcs:000000ff,txpow:120b|oui:samsunge':
        ('Samsung Galaxy Ace 4', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff|oui:samsunge':
        ('Samsung Galaxy Core 2', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0200000000|oui:samsunge':
        ('Samsung Galaxy Core Prime', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a0200000000|oui:samsunge':
        ('Samsung Galaxy Core Prime', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:0020,htagg:1f,htmcs:000000ff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:1f,htmcs:000000ff,txpow:1203|oui:samsunge':
        ('Samsung Galaxy Grand Prime', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:0020,htagg:17,htmcs:000000ff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:17,htmcs:000000ff,txpow:130b|oui:samsunge':
        ('Samsung Galaxy J1', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:0020,htagg:1f,htmcs:000000ff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:1f,htmcs:000000ff,txpow:1202|oui:samsunge':
        ('Samsung Galaxy J2', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,127,221(001018,2),htcap:0020,htagg:1f,htmcs:000000ff,extcap:0000008001|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:1f,htmcs:000000ff,txpow:1302|oui:samsunge':
        ('Samsung Galaxy J3', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:170d|oui:samsunge':
        ('Samsung Galaxy J5', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,127,221(001018,2),htcap:0020,htagg:1f,htmcs:000000ff,extcap:0000008001|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:1f,htmcs:000000ff,txpow:1203|oui:samsunge':
        ('Samsung Galaxy J7', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,htcap:0020,htagg:01,htmcs:000000ff|assoc:0,1,50,45,61,48,221(0050f2,2),htcap:0020,htagg:01,htmcs:000000ff|oui:samsunge':
        ('Samsung Galaxy', 'Mini', '2.4GHz'),

    'wifi4|probe:0,1,45,3,221(0050f2,4),221(001018,2),221(00904c,51),htcap:010c,htagg:19,htmcs:000000ff,wps:Galaxy_Nexus|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:010c,htagg:19,htmcs:000000ff,txpow:0f09':
        ('Samsung Galaxy Nexus', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,4),221(001018,2),221(00904c,51),htcap:010c,htagg:19,htmcs:000000ff,wps:Galaxy_Nexus|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:010c,htagg:19,htmcs:000000ff,txpow:0f09':
        ('Samsung Galaxy Nexus', '', '5GHz'),
    'wifi4|probe:0,1,45,3,221(0050f2,4),221(001018,2),221(00904c,51),htcap:000c,htagg:19,htmcs:000000ff,wps:_|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:000c,htagg:19,htmcs:000000ff,txpow:0f0a|oui:samsunge':
        ('Samsung Galaxy Nexus', '', '5GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,4),221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff,wps:Galaxy_Nexus|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff,txpow:1209':
        ('Samsung Galaxy Nexus', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,3,221(0050f2,4),221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff,wps:Galaxy_Nexus|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff,txpow:1209':
        ('Samsung Galaxy Nexus', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,4),221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff,wps:_|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff,txpow:120a|oui:samsunge':
        ('Samsung Galaxy Nexus', '', '2.4GHz'),

    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:000c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:000c,htagg:19,htmcs:000000ff,txpow:0f09|oui:samsunge':
        ('Samsung Galaxy Note or S2+', '', '5GHz'),
    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:000c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:000c,htagg:19,htmcs:000000ff,txpow:0f09|oui:samsunge':
        ('Samsung Galaxy Note or S2+', '', '5GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff,txpow:1409|oui:samsunge':
        ('Samsung Galaxy Note', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff,txpow:1409|oui:samsunge':
        ('Samsung Galaxy Note', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:0e09|oui:samsunge':
        ('Samsung Galaxy Note II', '', '5GHz'),
    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:0e09|oui:samsunge':
        ('Samsung Galaxy Note II', '', '5GHz'),
    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:0e09|oui:samsunge':
        ('Samsung Galaxy Note II', '', '5GHz'),
    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:0e09|oui:samsunge':
        ('Samsung Galaxy Note II', '', '5GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:1020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1020,htagg:1a,htmcs:000000ff,txpow:1209|oui:samsunge':
        ('Samsung Galaxy Note II', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:1020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1020,htagg:1a,htmcs:000000ff,txpow:1209|oui:samsunge':
        ('Samsung Galaxy Note II', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:1020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1020,htagg:1a,htmcs:000000ff,txpow:1209|oui:samsunge':
        ('Samsung Galaxy Note II', '', '2.4GHz'),

    'wifi4|probe:0,1,3,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000080000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e008,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000080000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e008,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e008,extcap:0000008001400040|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:016f,htagg:17,htmcs:000000ff,vhtcap:0f805932,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e008,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000080000000040|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1208|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000080000000040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1208|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,4),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1208,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,4),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1208,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:112d,htagg:17,htmcs:000000ff,extcap:0000088001400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff,txpow:1208,extcap:000000800140|oui:samsunge':
        ('Samsung Galaxy Note 3', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,107,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 4', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 4', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,107,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1509,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1509,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,107,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1509,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy Note 4', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,70,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy Note 5 or S7 Edge', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,70,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy Note 5 or S7 Edge', '', '5GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,70,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1202,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140|assoc:0,1,33,36,48,70,45,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1202|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9138b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9138b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:00080f8401400040|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1202|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:00080f8401400040|assoc:0,1,50,33,36,48,45,127,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1202,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:00080f8401400040|assoc:0,1,50,33,36,48,70,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1202|oui:samsunge':
        ('Samsung Galaxy Note 5', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:000c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:000c,htagg:19,htmcs:000000ff,txpow:0f0a|oui:samsunge':
        ('Samsung Galaxy S2', '', '5GHz'),
    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:000c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:000c,htagg:19,htmcs:000000ff,txpow:0f0a|oui:samsunge':
        ('Samsung Galaxy S2', '', '5GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff,txpow:120a|oui:samsunge':
        ('Samsung Galaxy S2 or Infuse', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff,txpow:120a|oui:samsunge':
        ('Samsung Galaxy S2 or Infuse', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff,txpow:1209|oui:samsunge':
        ('Samsung Galaxy S2+', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1409|oui:samsunge':
        ('Samsung Galaxy S3', '', '5GHz'),
    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1409|oui:samsunge':
        ('Samsung Galaxy S3', '', '5GHz'),
    'wifi4|probe:0,1,45,3,221(001018,2),221(00904c,51),htcap:0062,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:0062,htagg:1a,htmcs:000000ff,txpow:1009|oui:samsunge':
        ('Samsung Galaxy S3', '', '5GHz'),
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:1020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1020,htagg:1a,htmcs:000000ff,txpow:1409|oui:samsunge':
        ('Samsung Galaxy S3', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:1020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1020,htagg:1a,htmcs:000000ff,txpow:1409|oui:samsunge':
        ('Samsung Galaxy S3', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000080000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e001,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S4', '', '5GHz'),
    'wifi4|probe:0,1,3,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000080000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e001,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S4', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088000400040|assoc:0,1,33,36,48,45,127,107,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e001,extcap:0000008000400040|oui:samsunge':
        ('Samsung Galaxy S4', '', '5GHz'),
    'wifi4|probe:0,1,3,45,127,107,191,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000088000400040|assoc:0,1,33,36,48,45,127,107,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e001,extcap:0000008000400040|oui:samsunge':
        ('Samsung Galaxy S4', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000080000400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e001,extcap:0000000000400040|oui:samsunge':
        ('Samsung Galaxy S4', '', '5GHz'),
    'wifi4|probe:0,1,3,45,127,191,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000080000400040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(00904c,4),221(0050f2,2),htcap:006f,htagg:17,htmcs:000000ff,vhtcap:0f805832,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:e001,extcap:0000000000400040|oui:samsunge':
        ('Samsung Galaxy S4', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000088000400040|assoc:0,1,33,36,48,50,45,127,107,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1201,extcap:000000800040|oui:samsunge':
        ('Samsung Galaxy S4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000080000000040|assoc:0,1,33,36,48,50,45,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1201|oui:samsunge':
        ('Samsung Galaxy S4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,107,221(506f9a,16),221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000088000400040|assoc:0,1,33,36,48,50,45,127,107,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1201,extcap:000000800040|oui:samsunge':
        ('Samsung Galaxy S4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000080000400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,4),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1201,extcap:0000000000400040|oui:samsunge':
        ('Samsung Galaxy S4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000080000400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(00904c,4),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1201,extcap:0000000000400040|oui:samsunge':
        ('Samsung Galaxy S4', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),221(00904c,51),221(00904c,4),221(0050f2,8),htcap:102d,htagg:17,htmcs:000000ff,extcap:0000080000400040|assoc:0,1,33,36,48,50,45,127,221(001018,2),221(0050f2,2),htcap:102d,htagg:17,htmcs:000000ff,txpow:1201,extcap:000000000040|oui:samsunge':
        ('Samsung Galaxy S4', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,107,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e20b,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140|assoc:0,1,33,36,48,45,127,107,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e20b,extcap:000008800140|oui:samsunge':
        ('Samsung Galaxy S5', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,33,36,48,45,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e20b|oui:samsunge':
        ('Samsung Galaxy S5', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:9b40fffa,vhttxmcs:18dafffa|assoc:0,1,33,36,48,45,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:9b40fffa,vhttxmcs:18dafffa,txpow:e20b|oui:samsunge':
        ('Samsung Galaxy S5', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e20b,extcap:000008800140|oui:samsunge':
        ('Samsung Galaxy S5', '', '5GHz'),

    # SM-G900F non-US version
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:52e9fffa,vhttxmcs:3e04fffa,extcap:000008800140|assoc:0,1,33,36,48,45,127,107,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:52e9fffa,vhttxmcs:3e04fffa,txpow:e009,extcap:000008800140|oui:samsunge':
        ('Samsung Galaxy S5', '', '5GHz'),

    # Samsung Galaxy Tab S 2.4GHz signature is identical to S5.
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140|assoc:0,1,50,33,36,48,45,127,107,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140|oui:samsunge':
        ('Samsung Galaxy S5 or Tab S', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,107,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140|oui:samsunge':
        ('Samsung Galaxy S5 or Tab S', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:000008800140|assoc:0,1,50,33,36,48,70,45,127,107,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:000008800140|oui:samsunge':
        ('Samsung Galaxy S5 or Tab S', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,107,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S5 or Tab S', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,191,221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,33,36,48,45,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002|oui:samsunge':
        ('Samsung Galaxy S6', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,107,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,107,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,107,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1402,extcap:0000088001400040|oui:samsunge':
        ('Samsung Galaxy S6', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:0163,htagg:17,htmcs:0000ffff,vhtcap:0f907032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,70,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S7', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:00080f8401400040|assoc:0,1,50,33,36,48,70,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1402|oui:samsunge':
        ('Samsung Galaxy S7', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:00080f840140|assoc:0,1,50,33,36,48,70,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1402|oui:samsunge':
        ('Samsung Galaxy S7', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f840140|assoc:0,1,33,36,48,70,45,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1102|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9138b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1002,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9138b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1002,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9118b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1002,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9178b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:00080f8401400040|assoc:0,1,33,36,48,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f9138b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1002,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:1163,htagg:17,htmcs:0000ffff,extcap:00080f8401400040|assoc:0,1,50,33,36,48,70,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1302|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:00080f8401400040|assoc:0,1,50,33,36,48,70,45,221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1302|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:00080f8401400040|assoc:0,1,50,33,36,48,45,127,199,221(00904c,4),221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1302,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S7 Edge', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1103,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9179b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1103,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,45,127,191,199,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1203,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9139b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1203,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9179b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9139b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1203,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,vhtcap:0f9179b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1203,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1203,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,vhtcap:0f9179b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1103,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,vhtcap:0f9139b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9119b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1103,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9179b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9139b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1103,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9139b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,45,127,191,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:0f9139b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:1103,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,txpow:1503,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:11ef,htagg:1b,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,33,36,48,45,221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:000000ff,txpow:1503|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:11ef,htagg:1b,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,199,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,txpow:1503,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,45,127,199,221(00904c,4),221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,txpow:1503,extcap:0000080000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),221(00904c,92),htcap:11ef,htagg:1b,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,70,45,127,221(001018,2),221(0050f2,2),221(00904c,92),htcap:01ad,htagg:1b,htmcs:0000ffff,txpow:1503,extcap:0000000000000040|oui:samsunge':
        ('Samsung Galaxy S8/S8+', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(001018,2),221(00904c,51),htcap:082c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:082c,htagg:1b,htmcs:000000ff,txpow:0f08|oui:samsunge':
        ('Samsung Galaxy Tab', '', '5GHz'),
    'wifi4|probe:0,1,50,45,221(001018,2),221(00904c,51),htcap:182c,htagg:1b,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:182c,htagg:1b,htmcs:000000ff,txpow:1208|oui:samsunge':
        ('Samsung Galaxy Tab', '', '2.4GHz'),

    'wifi4|probe:0,1,45,50,htcap:0162,htagg:03,htmcs:00000000|assoc:0,1,48,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:000000ff,extcap:0400000000000140|oui:samsunge':
        ('Samsung Galaxy Tab 3', '', '5GHz'),
    'wifi4|probe:0,1,45,50,htcap:0162,htagg:03,htmcs:00000000|assoc:0,1,33,36,48,127,221(0050f2,2),45,htcap:016e,htagg:03,htmcs:000000ff,txpow:1208,extcap:0400000000000140|oui:samsunge':
        ('Samsung Galaxy Tab 3', '', '5GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:0162,htagg:03,htmcs:00000000|assoc:0,1,48,50,127,221(0050f2,2),45,htcap:012c,htagg:03,htmcs:000000ff,extcap:0000000000000140|oui:samsunge':
        ('Samsung Galaxy Tab 3', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,33,36,48,45,221(0050f2,2),221(004096,3),htcap:016e,htagg:03,htmcs:000000ff,txpow:170d|oui:samsunge':
        ('Samsung Galaxy Tab 4', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),221(004096,3),htcap:012c,htagg:03,htmcs:000000ff|oui:samsunge':
        ('Samsung Galaxy Tab 4', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,4),221(001018,2),221(00904c,51),htcap:000c,htagg:19,htmcs:000000ff,wps:_|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:000c,htagg:19,htmcs:000000ff,txpow:0c0a|oui:samsunge':
        ('Samsung Galaxy Tab 10.1', '', '5GHz'),
    'wifi4|probe:0,1,45,3,221(0050f2,4),221(001018,2),221(00904c,51),htcap:000c,htagg:19,htmcs:000000ff,wps:_|assoc:0,1,33,36,48,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:000c,htagg:19,htmcs:000000ff,txpow:0c0a|oui:samsunge':
        ('Samsung Galaxy Tab 10.1', '', '5GHz'),
    'wifi4|probe:0,1,50,45,3,221(0050f2,4),221(001018,2),221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff,wps:_|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff,txpow:0f0a|oui:samsunge':
        ('Samsung Galaxy Tab 10.1', '', '2.4GHz'),

    'wifi4|probe:0,1,3,45,221(0050f2,8),127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a820040|assoc:0,1,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,48,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a820040|assoc:0,1,33,36,48,70,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),127,107,221(506f9a,16),htcap:016e,htagg:03,htmcs:000000ff,extcap:00000a820040|assoc:0,1,33,36,48,70,45,221(0050f2,2),127,htcap:016e,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a820040|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,107,221(506f9a,16),htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a820040|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a8201400000|oui:samsunge':
        ('Samsung Galaxy Tab A', '', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(00904c,4),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:000008800140|assoc:0,1,33,36,48,45,127,107,191,221(00904c,4),221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:000008800140|oui:samsunge':
        ('Samsung Galaxy Tab S', '', '5GHz'),
    # Galaxy Tab S 2.4GHz signature is identical to Galaxy S5. See above for "Galaxy S5 or Tab S"

    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:0020,htagg:17,htmcs:000000ff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:17,htmcs:000000ff,txpow:140b|oui:samsunge':
        ('Samsung Galaxy Young', '2', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:0020,htagg:1f,htmcs:000000ff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:0020,htagg:1f,htmcs:000000ff,txpow:1203|os:tizen':
        ('Samsung Watch', 'Gear S2', '2.4GHz'),

    'wifi4|probe:0,1,45,htcap:11ee,htagg:02,htmcs:0000ffff|assoc:0,1,45,127,33,36,48,221(0050f2,2),htcap:11ee,htagg:02,htmcs:0000ffff,txpow:1100,extcap:01|os:samsungtv':
        ('Samsung Smart TV', '', '5GHz'),
    # UN55JS9000, probably more
    'wifi4|probe:0,1,45,127,191,221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000000000040|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000000000000040|os:tizen':
        ('Samsung Smart TV', '', '5GHz'),
    # LED75
    'wifi4|probe:0,1,45,221(002d25,32),htcap:11ee,htagg:02,htmcs:0000ffff|assoc:0,1,33,36,221(0050f2,2),45,127,htcap:11ee,htagg:02,htmcs:0000ffff,txpow:0e00,extcap:01|os:samsungtv':
        ('Samsung Smart TV', '', '5GHz'),
    # UN46ES7100F
    'wifi4|probe:0,1,45,221(002d25,32),htcap:11ee,htagg:02,htmcs:0000ffff|assoc:0,1,33,36,48,221(0050f2,2),45,127,htcap:11ee,htagg:02,htmcs:0000ffff,txpow:0e00,extcap:01|os:samsungtv':
        ('Samsung Smart TV', '', '5GHz'),
    # UN40JU7100F
    'wifi4|probe:0,1,45,127,191,221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000000000000040|assoc:0,1,33,36,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000000000000040|os:tizen':
        ('Samsung Smart TV', '', '5GHz'),
    # UN40JU6500
    'wifi4|probe:0,1,45,191,221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa|assoc:0,1,33,36,48,45,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009|os:tizen':
        ('Samsung Smart TV', '', '5GHz'),
    'wifi4|probe:0,1,50,45,htcap:01ac,htagg:02,htmcs:0000ffff|assoc:0,1,50,45,127,48,221(0050f2,2),htcap:01ac,htagg:02,htmcs:0000ffff,extcap:01|os:samsungtv':
        ('Samsung Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(002d25,32),htcap:01ac,htagg:02,htmcs:0000ffff|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:01ac,htagg:02,htmcs:0000ffff,extcap:01|os:samsungtv':
        ('Samsung Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,htcap:0120,htagg:02,htmcs:000000ff|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:0120,htagg:02,htmcs:000000ff,extcap:01|os:samsungtv':
        ('Samsung Smart TV', '', '2.4GHz'),
    # UN40JU6500, UN40JU7100F, probably more
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000000000000040|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209|os:tizen':
        ('Samsung Smart TV', '', '2.4GHz'),
    # UN40JU6500, probably more
    'wifi4|probe:0,1,50,3,45,221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff|assoc:0,1,50,33,36,48,45,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1209|os:tizen':
        ('Samsung Smart TV', '', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,htcap:11ef,htagg:1b,htmcs:0000ffff|assoc:0,1,50,48,45,221(0050f2,2),htcap:11ef,htagg:1b,htmcs:0000ffff|oui:sling':
        ('Slingbox', '500', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:1b0d,extcap:00000a02|oui:haier':
        ('SmartFren AndroMax G2', '', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a02|oui:haier':
        ('SmartFren AndroMax G2', '', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,4),htcap:11ee,htagg:02,htmcs:0000ffff,wps:Sony_BRAVIA|assoc:0,1,33,36,48,221(0050f2,2),45,127,htcap:11ee,htagg:02,htmcs:0000ffff,txpow:0500,extcap:01':
        ('Sony Bravia TV', '', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:11ef,htagg:13,htmcs:0000ffff,wps:BRAVIA_2015|assoc:0,1,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:01ef,htagg:13,htmcs:0000ffff,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '5GHz'),
    'wifi4|probe:0,1,221(0050f2,4),221(506f9a,10),221(506f9a,9),wps:BRAVIA_2015|assoc:0,1,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:01ef,htagg:13,htmcs:0000ffff,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:11ef,htagg:13,htmcs:0000ffff,vhtcap:31c139b0,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,wps:BRAVIA_4K_2015|assoc:0,1,45,191,127,221(000c43,6),221(0050f2,2),48,127,htcap:006f,htagg:13,htmcs:0000ffff,vhtcap:31c001b0,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,4),htcap:11ee,htagg:02,htmcs:0000ffff,wps:Sony_BRAVIA|assoc:0,1,33,36,48,221(0050f2,2),45,127,htcap:11ee,htagg:02,htmcs:0000ffff,txpow:0c00,extcap:01':
        ('Sony Bravia TV', '', '5GHz'),
    'wifi4|probe:0,1,221(0050f2,4),221(506f9a,10),221(506f9a,9),wps:BRAVIA_4K_2015|assoc:0,1,45,191,127,221(000c43,6),221(0050f2,2),48,127,htcap:006f,htagg:13,htmcs:0000ffff,vhtcap:31c001b0,vhtrxmcs:030cfffa,vhttxmcs:030cfffa,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '5GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:01ad,htagg:02,htmcs:0000ffff,wps:Sony_BRAVIA|assoc:0,1,50,45,127,48,221(0050f2,2),htcap:01ad,htagg:02,htmcs:0000ffff,extcap:01':
        ('Sony Bravia TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,4),htcap:01ac,htagg:02,htmcs:0000ffff,wps:Sony_BRAVIA|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:01ac,htagg:02,htmcs:0000ffff,extcap:01':
        ('Sony Bravia TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,4),htcap:01ac,htagg:02,htmcs:0000ffff,wps:Sony_BRAVIA|assoc:0,1,50,221(0050f2,2),45,127,htcap:01ac,htagg:02,htmcs:0000ffff,extcap:01':
        ('Sony Bravia TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:01ed,htagg:13,htmcs:0000ffff,extcap:00,wps:BRAVIA_2015|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:008c,htagg:13,htmcs:0000ffff,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:11ef,htagg:13,htmcs:0000ffff,extcap:00,wps:BRAVIA_2015|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:01ad,htagg:13,htmcs:0000ffff,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,10),221(506f9a,9),wps:BRAVIA_4K_2015|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:008c,htagg:13,htmcs:0000ffff,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,10),221(506f9a,9),wps:BRAVIA_2015|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:01ad,htagg:13,htmcs:0000ffff,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),221(506f9a,10),221(506f9a,9),htcap:11ef,htagg:13,htmcs:0000ffff,extcap:00,wps:BRAVIA_4K_2015|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,127,htcap:008c,htagg:13,htmcs:0000ffff,extcap:00000a02':
        ('Sony Bravia TV', '2015 model', '2.4GHz'),

    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffc,vhttxmcs:0000fffc|assoc:0,1,33,36,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff|oui:sony':
        ('Sony Xperia', 'Z Ultra', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:31800120,vhtrxmcs:0000fffc,vhttxmcs:0000fffc|assoc:0,1,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:sony':
        ('Sony Xperia', 'Z Ultra', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a0200000000|oui:sony':
        ('Sony Xperia', 'Z Ultra', '2.4GHz'),
    'wifi4|probe:0,1,50,45,htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:170d,extcap:00000a0200000000|oui:sony':
        ('Sony Xperia', 'Z Ultra', '2.4GHz'),

    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,107,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815032,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000088001400040|oui:sony':
        ('Sony Xperia', 'Z4 or Z5', '5GHz'),
    'wifi4|probe:0,1,45,127,107,191,221(506f9a,16),221(0050f2,8),221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000088001400040|assoc:0,1,33,36,48,70,45,127,107,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000088001400040|oui:sony':
        ('Sony Xperia', 'Z4 or Z5', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,107,221(506f9a,16),221(0050f2,8),221(001018,2),htcap:002d,htagg:17,htmcs:0000ffff,extcap:0000088001400040|assoc:0,1,50,33,36,48,70,45,127,107,221(001018,2),221(0050f2,2),htcap:002d,htagg:17,htmcs:0000ffff,txpow:1307,extcap:0000088001400040|oui:sony':
        ('Sony Xperia', 'Z4 or Z5', '2.4GHz'),

    # TIVO-849
    'wifi4|probe:0,1,45,127,191,221(001018,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000008001|assoc:0,1,33,36,48,45,127,191,221(001018,2),221(0050f2,2),htcap:006f,htagg:17,htmcs:0000ffff,vhtcap:0f815832,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e009,extcap:0000008001|os:tivo':
        ('TiVo', 'BOLT', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(00904c,51),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000008001000040|assoc:0,1,33,36,48,45,127,191,221(00904c,51),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000008001000040|os:tivo':
        ('TiVo', 'BOLT', '5GHz'),
    'wifi4|probe:0,1,45,127,191,221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0000008001000040|assoc:0,1,33,36,48,45,127,191,221(00904c,51),221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e007,extcap:0000008001000040|os:tivo':
        ('TiVo', 'BOLT', '5GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(00904c,51),221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:0000008001000040|assoc:0,1,50,33,36,48,45,127,221(00904c,51),221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1207,extcap:0000008001000040|os:tivo':
        ('TiVo', 'BOLT', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,127,221(001018,2),htcap:01ad,htagg:17,htmcs:0000ffff,extcap:0000008001000040|assoc:0,1,50,33,36,48,45,127,221(00904c,51),221(001018,2),221(0050f2,2),htcap:01ad,htagg:17,htmcs:0000ffff,txpow:1207,extcap:0000008001000040|os:tivo':
        ('TiVo', 'BOLT', '2.4GHz'),

    # TIVO-746
    'wifi4|probe:0,1,50,221(00904c,51),45,48,htcap:13ce,htagg:1b,htmcs:0000ffff|assoc:0,1,33,36,50,221(0050f2,2),221(00904c,51),45,221(002163,1),221(002163,4),48,htcap:13ce,htagg:1b,htmcs:0000ffff,txpow:0f0f|os:tivo':
        ('TiVo', 'Premiere Series 4', '2.4GHz'),
    # TIVO-846
    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:107c,htagg:19,htmcs:0000ffff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:107c,htagg:19,htmcs:0000ffff,txpow:1208|os:tivo':
        ('TiVo', 'Roamio', '2.4GHz'),
    # TIVO-848
    'wifi4|probe:0,1,50|assoc:0,1,50,221(0050f2,2),45,51,48,htcap:01ac,htagg:1b,htmcs:0000ffff|os:tivo':
        ('TiVo', 'Roamio Plus', '2.4GHz'),
    # TiVo-652 HD and HD XL, TIVO-648, and TIVO-750 have the same signature
    'wifi4|probe:0,1,50,221(001018,2)|assoc:0,1,48,50,221(001018,2)|os:tivo':
        ('TiVo', 'Series3 or Series4', '2.4GHz'),

    'wifi4|probe:0,1,50,45,221(0050f2,4),htcap:106e,htagg:13,htmcs:0000ffff,wps:Ralink_Wireless_Linux_Client|assoc:0,1,45,127,221(000c43,6),221(0050f2,2),48,htcap:000e,htagg:13,htmcs:0000ffff,extcap:00|oui:toshiba':
        ('Toshiba Smart TV', '', '5GHz'),
    'wifi4|probe:0,1,221(0050f2,4),wps:Ralink_Wireless_Linux_Client|assoc:0,1,45,127,221(000c43,6),221(0050f2,2),48,htcap:000e,htagg:13,htmcs:0000ffff,extcap:00|oui:toshiba':
        ('Toshiba Smart TV', '', '5GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),wps:Ralink_Wireless_Linux_Client|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,htcap:000c,htagg:13,htmcs:0000ffff,extcap:01|oui:toshiba':
        ('Toshiba Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),htcap:106e,htagg:13,htmcs:0000ffff,extcap:00,wps:Ralink_Wireless_Linux_Client|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,htcap:000c,htagg:13,htmcs:0000ffff,extcap:01|oui:toshiba':
        ('Toshiba Smart TV', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,htcap:0120,htagg:01,htmcs:000000ff|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:0120,htagg:01,htmcs:000000ff,extcap:01|name:LB100':
        ('TP-Link smart bulb', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,htcap:0120,htagg:01,htmcs:000000ff|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:0120,htagg:01,htmcs:000000ff,extcap:01|name:HS105':
        ('TP-Link smart plug', '', '2.4GHz'),

    # https://www.hellotwist.com
    'wifi4|probe:0,1,50,3,45,127,htcap:0172,htagg:13,htmcs:000000ff,extcap:0000000000000040|assoc:0,1,50,48,45,127,221(0050f2,2),htcap:013c,htagg:13,htmcs:000000ff,extcap:0000000000000040|oui:astro':
        ('Twist Speaker', '', '2.4GHz'),

    # P602ui-B3
    'wifi4|probe:0,1,50,221(0050f2,4),wps:_|assoc:0,33,36,1,48,221(0050f2,2),45,127,htcap:106e,htagg:1f,htmcs:0000ffff,txpow:150d,extcap:0000000000000000|os:viziotv':
        ('Vizio Smart TV', '', '5GHz'),
    # P602ui-B3
    'wifi4|probe:0,1,50|assoc:0,33,36,1,48,221(0050f2,2),45,127,htcap:106e,htagg:1f,htmcs:0000ffff,txpow:150d,extcap:0000000000000000|os:viziotv':
        ('Vizio Smart TV', '', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,4),221(506f9a,9),221(001018,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,wps:_|assoc:0,1,33,36,48,45,191,221(001018,2),221(0050f2,2),htcap:01ef,htagg:17,htmcs:0000ffff,vhtcap:0f8159b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,txpow:e002|oui:vizio':
        ('Vizio SmartCast TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),wps:Ralink_Wireless_Linux_Client|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,htcap:000c,htagg:12,htmcs:000000ff,extcap:01000000|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),wps:Ralink_Wireless_Linux_Client|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,htcap:000c,htagg:13,htmcs:000000ff,extcap:01|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),htcap:106e,htagg:12,htmcs:000000ff,extcap:00,wps:Ralink_Wireless_Linux_Client|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,htcap:000c,htagg:12,htmcs:000000ff,extcap:01000000|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,45,127,221(0050f2,4),htcap:106e,htagg:13,htmcs:000000ff,extcap:00,wps:Ralink_Wireless_Linux_Client|assoc:0,1,50,45,127,221(000c43,6),221(0050f2,2),48,htcap:000c,htagg:13,htmcs:000000ff,extcap:01|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,221(0050f2,4),wps:Ralink_Wireless_Linux_Client|assoc:0,1,50,45,221(000c43,6),221(0050f2,2),48,htcap:000c,htagg:13,htmcs:000000ff|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),
    'wifi4|probe:0,1,50,48|assoc:0,1,50,221(0050f2,2),45,51,127,48,htcap:012c,htagg:1b,htmcs:000000ff,extcap:01|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),
    # P602ui-B3
    'wifi4|probe:0,1,50,221(0050f2,4),wps:_|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:122c,htagg:1f,htmcs:0000ffff,extcap:0000000000000000|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),
    # P602ui-B3
    'wifi4|probe:0,1,50|assoc:0,1,50,48,221(0050f2,2),45,127,htcap:122c,htagg:1f,htmcs:0000ffff,extcap:0000000000000000|os:viziotv':
        ('Vizio Smart TV', '', '2.4GHz'),

    'wifi4|probe:0,1,3,45,221(0050f2,8),htcap:016e,htagg:03,htmcs:000000ff|assoc:0,1,33,36,45,221(0050f2,2),htcap:016e,htagg:03,htmcs:000000ff,txpow:110d|oui:vizio':
        ('Vizio Tablet', 'XR6P', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:vizio':
        ('Vizio Tablet', 'XR6P', '2.4GHz'),

    'wifi4|probe:0,1,50,221(001018,2)|assoc:0,1,48,50,221(001018,2)|os:wii':
        ('Wii', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(00904c,51),htcap:100c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(00904c,51),221(0050f2,2),htcap:100c,htagg:19,htmcs:000000ff|os:wii':
        ('Wii-U', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:1020,htagg:1a,htmcs:000000ff|assoc:0,1,33,36,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:1020,htagg:1a,htmcs:000000ff,txpow:1009|oui:wink':
        ('Wink Hub', '', '2.4GHz'),

    'wifi4|probe:0,1,50,45,3,221(001018,2),221(00904c,51),htcap:110c,htagg:19,htmcs:000000ff|assoc:0,1,48,50,45,221(001018,2),221(00904c,51),221(0050f2,2),htcap:110c,htagg:19,htmcs:000000ff|oui:withings':
        ('Withings Scale', '', '2.4GHz'),

    'wifi4|probe:0,1,3,45,50,127,htcap:010c,htagg:1b,htmcs:0000ffff,extcap:00|assoc:0,1,45,48,50,221(0050f2,2),htcap:010c,htagg:1b,htmcs:000000ff|oui:microsoft':
        ('Xbox', '', '5GHz'),
    'wifi4|probe:0,1,3|assoc:0,1,48,33,36,221(0050f2,2),txpow:1405|oui:microsoft':
        ('Xbox', '', '5GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:016e,htagg:03,htmcs:0000ffff|assoc:0,1,33,48,50,127,221(0050f2,2),45,htcap:012c,htagg:03,htmcs:0000ffff,txpow:1208,extcap:0000000000000140|oui:microsoft':
        ('Xbox', '', '5GHz'),
    'wifi4|probe:0,1,50|assoc:0,1,3,33,36,50,221(0050f2,2),45,221(00037f,1),221(00037f,4),48,htcap:104c,htagg:00,htmcs:000000ff,txpow:0f0f|oui:microsoft':
        ('Xbox', '', '2.4GHz'),
    'wifi4|probe:0,1,50,48|assoc:0,1,3,33,36,50,221(0050f2,2),45,221(00037f,1),221(00037f,4),48,htcap:104c,htagg:00,htmcs:0000ffff,txpow:0f0f|oui:microsoft':
        ('Xbox', '', '2.4GHz'),
    'wifi4|probe:0,1,3,50|assoc:0,1,33,48,50,127,127,221(0050f2,2),45,htcap:012c,htagg:03,htmcs:0000ffff,txpow:1208,extcap:0000000000000140|oui:microsoft':
        ('Xbox', '', '2.4GHz'),

    'wifi4|probe:0,1,3,50|assoc:0,1,45,48,50,221(0050f2,2),htcap:11ed,htagg:1b,htmcs:000000ff|oui:microsoft':
        ('Xbox', '360', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,127,htcap:11ed,htagg:1b,htmcs:0000ffff,extcap:04|assoc:0,1,45,48,50,221(0050f2,2),htcap:11ed,htagg:1b,htmcs:000000ff|oui:microsoft':
        ('Xbox', '360', '2.4GHz'),
    'wifi4|probe:0,1,3,45,127,htcap:192d,htagg:17,htmcs:000000ff,extcap:05|assoc:0,1,45,221(0050f2,2),htcap:112d,htagg:17,htmcs:000000ff|oui:microsoft':
        ('Xbox', '360', '2.4GHz'),
    'wifi4|probe:0,1,3,50|assoc:0,1,45,48,50,221(0050f2,2),htcap:010c,htagg:1b,htmcs:000000ff|oui:microsoft':
        ('Xbox', '360', '2.4GHz'),

    'wifi4|probe:0,1,45,50,htcap:058f,htagg:03,htmcs:0000ffff|assoc:0,1,33,36,221(0050f2,2),45,htcap:058f,htagg:03,htmcs:0000ffff,txpow:1208|oui:microsoft':
        ('Xbox', 'One', '5GHz'),
    'wifi4|probe:0,1,45,50,htcap:058f,htagg:03,htmcs:0000ffff|assoc:0,1,48,221(0050f2,2),45,htcap:058f,htagg:03,htmcs:0000ffff|oui:microsoft':
        ('Xbox', 'One', '5GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:058f,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,221(0050f2,2),45,htcap:058d,htagg:03,htmcs:0000ffff|oui:microsoft':
        ('Xbox', 'One', '2.4GHz'),
    'wifi4|probe:0,1,45,50,htcap:058f,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,221(0050f2,2),45,htcap:058d,htagg:03,htmcs:0000ffff|oui:microsoft':
        ('Xbox', 'One', '2.4GHz'),
    'wifi4|probe:0,1|assoc:0,1,50,45,127,221(000c43,0),221(0050f2,2),33,48,htcap:008d,htagg:02,htmcs:0000ffff,txpow:0805,extcap:0100000000000000|oui:microsoft':
        ('Xbox', 'One', '2.4GHz'),
    'wifi4|probe:0,1,50|assoc:0,1,50,45,127,221(000c43,0),221(0050f2,2),33,48,htcap:008d,htagg:02,htmcs:0000ffff,txpow:0805,extcap:0100000000000000|oui:microsoft':
        ('Xbox', 'One', '2.4GHz'),

    'wifi4|probe:0,1,45,50,htcap:058f,htagg:03,htmcs:0000ffff|assoc:0,1,33,36,48,221(0050f2,2),45,htcap:058f,htagg:03,htmcs:0000ffff,txpow:1208|oui:microsoft':
        ('Xbox', 'One', '2.4GHz'),
    'wifi4|probe:0,1,3,45,50,htcap:058f,htagg:03,htmcs:0000ffff|assoc:0,1,48,50,221(0050f2,2),45,htcap:158d,htagg:03,htmcs:0000ffff|oui:microsoft':
        ('Xbox', 'One', '2.4GHz'),

    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:170d|oui:xiaomi':
        ('Xiaomi Redmi', '3', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:140d,extcap:0000000000000040|oui:xiaomi':
        ('Xiaomi Redmi Note', '3', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0201|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33907120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|oui:xiaomi':
        ('Xiaomi Redmi Note', '3', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:0000000000000040|oui:xiaomi':
        ('Xiaomi Redmi Note', '3', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,48,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff|oui:xiaomi':
        ('Xiaomi Redmi Note', '3', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0201|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012c,htagg:03,htmcs:000000ff,txpow:140d|oui:xiaomi':
        ('Xiaomi Redmi Note', '3', '2.4GHz'),

    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33901120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33901120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0200000040|oui:xiaomi':
        ('Xiaomi Mi', '4i', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33901120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0200000040|oui:xiaomi':
        ('Xiaomi Mi', '4i', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33901120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33901120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a0200000040|oui:xiaomi':
        ('Xiaomi Mi', '4i', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33800120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33901120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,txpow:1e0d,extcap:00000a0200000040|oui:xiaomi':
        ('Xiaomi Mi', '4i', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0200000040|oui:xiaomi':
        ('Xiaomi Mi', '4i', '5GHz'),
    'wifi4|probe:0,1,3,45,221(0050f2,8),191,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33901120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016e,htagg:03,htmcs:000000ff,vhtcap:33903120,vhtrxmcs:0000fffe,vhttxmcs:0000fffe,extcap:00000a0200000040|oui:xiaomi':
        ('Xiaomi Mi', '4i', '5GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,extcap:00000a0200000000|oui:xiaomi':
        ('Xiaomi Mi', '4i', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),htcap:012c,htagg:03,htmcs:000000ff|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012c,htagg:03,htmcs:000000ff,txpow:140d,extcap:00000a0200000000|oui:xiaomi':
        ('Xiaomi Mi', '4i', '2.4GHz'),

    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:040000000000004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1408,extcap:040000000000004080|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,191,3,127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1408,extcap:040000000000004080|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1408,extcap:0400000000000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400000000000040|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400000000000040|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1e08,extcap:0400000000000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a0201000040|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:040000000000004080|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1408,extcap:0400000000000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,221(0050f2,8),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:040000000000004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33903132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),3,127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a0201000040|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,48,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,45,191,221(0050f2,8),3,127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a0201000040|assoc:0,1,33,36,48,70,45,221(0050f2,2),191,127,htcap:016f,htagg:1f,htmcs:000000ff,vhtcap:33907132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,txpow:1e08,extcap:0400000000000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '5GHz'),
    'wifi4|probe:0,1,50,45,191,3,127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012d,htagg:1f,htmcs:000000ff,txpow:1408,extcap:040000000000000080|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:040000000000000080|assoc:0,1,50,33,48,70,45,221(0050f2,2),127,htcap:012d,htagg:1f,htmcs:000000ff,txpow:1408,extcap:040000000000000080|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:040000000000000080|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012d,htagg:1f,htmcs:000000ff,txpow:1408|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,45,191,221(0050f2,8),3,127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a0201000040|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:04000802|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:04000a0201|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:04000802|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:04|assoc:0,1,50,48,45,221(0050f2,2),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:04000802|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,45,191,221(0050f2,8),3,127,htcap:016f,htagg:df,htmcs:000000ff,vhtcap:33800132,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a0201000040|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012d,htagg:1f,htmcs:000000ff,txpow:1408|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),3,127,htcap:012f,htagg:1f,htmcs:000000ff,extcap:04000a020100004080|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012d,htagg:1f,htmcs:000000ff,txpow:1408|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),191,127,htcap:012d,htagg:1f,htmcs:000000ff,vhtcap:33907112,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:04000a020100004080|assoc:0,1,50,48,45,221(0050f2,2),127,221(00904c,4),htcap:012d,htagg:1f,htmcs:000000ff,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),191,127,htcap:012d,htagg:1f,htmcs:000000ff,vhtcap:33903112,vhtrxmcs:0186fffe,vhttxmcs:0186fffe,extcap:040000000000004080|assoc:0,1,50,48,45,221(0050f2,2),127,221(00904c,4),htcap:012d,htagg:1f,htmcs:000000ff,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,3,45,221(0050f2,8),127,htcap:012d,htagg:1f,htmcs:000000ff,extcap:04000a0201|assoc:0,1,50,33,48,70,45,221(0050f2,2),htcap:012d,htagg:1f,htmcs:000000ff,txpow:1408|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),
    'wifi4|probe:0,1,50,45,221(0050f2,8),3,127,htcap:012f,htagg:1f,htmcs:000000ff,extcap:04000a020100004080|assoc:0,1,50,48,45,221(0050f2,2),127,221(00904c,4),htcap:012d,htagg:1f,htmcs:000000ff,extcap:0400080200000040|oui:xiaomi':
        ('Xiaomi Mi', '5', '2.4GHz'),

    'wifi4|probe:0,1,50,221(0050f2,4),221(506f9a,9),wps:Z820|assoc:0,1,50,45,48,127,221(0050f2,2),htcap:1172,htagg:03,htmcs:000000ff,extcap:01':
        ('ZTE Obsidian', '', '2.4GHz'),


    # ACCESS POINT SIGNATURES

    'wifi4|beacon:0,1,3,5,48,45,61,127,221(0050f2,2),221(000b86,1),htcap:01ce,htagg:1b,htmcs:0000ffff,extcap:0000080000000000,cap:0411':
        ('Aruba AP-105', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,32,35,48,11,45,61,127,221(0050f2,2),221(000b86,1),221(000b86,1),htcap:01ef,htagg:1b,htmcs:0000ffff,extcap:0000080000000000,cap:0511':
        ('Aruba AP-135', '', '5GHz'),
    'wifi4|beacon:0,1,3,5,7,32,35,48,45,61,127,221(0050f2,2),221(000b86,1),221(000b86,1),htcap:01ef,htagg:1b,htmcs:0000ffff,extcap:0000080000000000,cap:0511':
        ('Aruba AP-135', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,32,35,48,11,45,61,127,191,192,195,221(000b86,1),221(000b86,1),221(0050f2,2),htcap:09ef,htagg:17,htmcs:0000ffff,vhtcap:0f825991,vhtrxmcs:0000ffea,vhttxmcs:0000ffea,extcap:0400080000000040,cap:1111':
        ('Aruba AP-22x', '', '5GHz'),
    'wifi4|beacon:0,1,3,5,7,32,35,48,11,45,61,127,191,192,195,221(000b86,1),221(000b86,1),221(0050f2,2),htcap:09ef,htagg:17,htmcs:0000ffff,vhtcap:0f8259b1,vhtrxmcs:0000ffea,vhttxmcs:0000ffea,extcap:0400080000000040,cap:1111':
        ('Aruba AP-22x', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,32,35,48,11,45,61,127,191,192,195,221(000b86,1),221(000b86,1),221(0050f2,2),htcap:09ad,htagg:17,htmcs:0000ffff,vhtcap:0f825991,vhtrxmcs:0000ffea,vhttxmcs:0000ffea,extcap:0400080000000040,cap:1111':
        ('Aruba AP-27x', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,32,35,11,48,45,61,74,127,191,192,195,221(0050f2,2),221(000b86,1),221(000b86,1),htcap:09ef,htagg:1b,htmcs:0000ffff,vhtcap:338b7991,vhtrxmcs:0000ffaa,vhttxmcs:0000ffaa,extcap:0100080000000040,cap:0111':
        ('Aruba AP-325', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,32,42,45,61,127,221(0050f2,2),48,191,192,221(002686,1),htcap:09ef,htagg:17,htmcs:0000ffff,vhtcap:3fc359b2,vhtrxmcs:0000ffaa,vhttxmcs:0000ffaa,extcap:0000000000000040,cap:0511':
        ('AT&T U-verse 5268AC', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,32,48,70,45,61,127,191,192,221(0050f2,2),htcap:010e,htagg:1b,htmcs:0000ffff,vhtcap:01800010,vhtrxmcs:0000ffea,vhttxmcs:0000ffea,extcap:0400000000000140,cap:1111':
        ('Google Fiber GFRG2x0', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,48,45,61,127,191,192,221(0050f2,2),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:0000ffea,vhttxmcs:0000ffea,extcap:0400080200000040,cap:0031':
        ('Google OnHub', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,48,45,61,127,191,192,221(0050f2,2),htcap:01ef,htagg:1b,htmcs:0000ffff,vhtcap:338139b2,vhtrxmcs:0000fffa,vhttxmcs:0000fffa,extcap:0400080200000040,cap:0031':
        ('Google Wifi', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,48,59,45,61,127,221(0050f2,2),htcap:01ce,htagg:1b,htmcs:0000ffff,extcap:0400000000000040,cap:0011':
        ('NetGEAR WNDR3800', '', '5GHz'),

    'wifi4|beacon:0,1,3,5,7,32,45,61,74,127,191,192,195,221(0050f2,2),221(00037f,1),48,221(0050f2,1),221(0050f2,4),htcap:09ef,htagg:1b,htmcs:0000ffff,vhtcap:338001b2,vhtrxmcs:0000ffea,vhttxmcs:0000ffea,extcap:0100000000000040,cap:0511':
        ('Technicolor DPC3941B', '', '5GHz'),
}

def identify_wifi_device(bssid, probeReq, assocReq, oui):
	"""Look up a wifi device by signature.

	Arguments:
	mac: MAC address of the client, a string of the form 'qq:rr:ss:tt:uu:vv'
	probeReq: probe request from the client in hex
	asssocReq: association request from the client in hex
	oui: client's oui vendor

	Returns:
		The model of the device if known
		If the signature is not known, return None
	"""
	try:
                process = ['./%s' % (TAXONOMY_C_FILE[:-2]), probeReq, assocReq]
                signature = subprocess.check_output(process)
        except Exception, e:
                print(e)
                return None
	sig = signature.strip()
#	opersys = dhcp.LookupOperatingSystem(mac)
	suffixes = []
#	for o in opersys:
#		suffixes.append('|os:' + o)
	if oui:
		suffixes.append('|oui:' + oui)
	suffixes.append
	for suffix in suffixes:
		parsed_sig = (sig + suffix).split('|')
		for key, value in database.iteritems():
			parsed_key = key.split('|')
			#check if there is a suffix in key. If suffix does not match, stop comparing
			if len(parsed_key) > 3:
				if parsed_key[3] != parsed_sig[3]:
					continue
			d_key = parsed_key[1:3]
			d_sig = parsed_sig[1:3]
			try:
				for i, elem in enumerate(d_sig):
					values_sig = d_sig[i].split(',')
					values_key = d_key[i].split(',')
					diff = [i for i, j in zip(values_sig, values_key) if i != j]
					if len(diff) < 2:
						return value[0]
			except:
				continue
	# We have no idea what the client is.
	return None
