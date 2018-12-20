import os

class WMConfig():
    #pcap thread config
    gui_update_time = 0.5
    pcap_read_pause = 0.005
    pcap_read_pkts_pause = 5

    #channel thread config
    channel_hop_time = 0.25
    channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    #app config
    version = "0.5"
    app_icon = os.path.join('Static', 'images', 'icon.png')
    taxo_file = os.path.join('backend_wifi_mapper', 'C_Utilities', 'create_signature.c')
    mac_list_file = os.path.join('mac_list')

conf = WMConfig()
