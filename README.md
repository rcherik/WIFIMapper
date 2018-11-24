# WIFIMapper

Sniff wifi on an interface or read pcap file using python scapy with kivy graphical UI

## Start sniffing

#### Start monitoring
```
make monitor
```

- To see which interface is used: ``` make interface ```

#### Sniff wifi
```
sudo python application.py
```

- To force sniffing on an interface use: ``-i or --interface <iface_to_use>``
- Remove channel hopping use: ```-n or --no-hop```

#### Return to managed mode
```
make managed
```

## Read pcap file
```
python application.py --pcap <pcap_file>
```

## Authors

* **Rémi Cherik** - *Lady Killer* - [github](https://github.com/rcherik)
* **Maxence Dufaud** - *Fajo* - [github](https://github.com/mdufaud)
