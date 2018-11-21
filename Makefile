NAME=application.py
INTERFACE=$(shell /sbin/ip route | awk 'NR==1{print $$5}')
PYTHON=/usr/bin/python
SUDO=/usr/bin/sudo

all: sniff

sniff:
	$(SUDO) $(PYTHON) application.py

read:
	$(PYTHON) application.py --pcap Traces_pcap/unknown_ap.pcap
	make clean

read_1:
	$(PYTHON) application.py --pcap Traces_pcap/single_wpa.pcap
	make clean

read_2:
	$(PYTHON) application.py --pcap Traces_pcap/double_wpa_and_fail.pcap
	make clean

managed:
	$(SUDO) /sbin/ifconfig $(INTERFACE) down &&\
	$(SUDO) /sbin/iwconfig $(INTERFACE) mode managed &&\
	$(SUDO) /sbin/ifconfig $(INTERFACE) up &&\
	$(SUDO) /etc/init.d/network-manager start

monitor:
	$(SUDO) /usr/sbin/airmon-ng check kill &&\
	$(SUDO) /sbin/ifconfig $(INTERFACE) down &&\
	$(SUDO) /sbin/iwconfig $(INTERFACE) mode monitor &&\
	$(SUDO) /sbin/ifconfig $(INTERFACE) up

interface:
	@echo "using interface: $(INTERFACE)"

clean:
	rm -f *.pyc
	rm -f backend_wifi_mapper/*.pyc
	rm -f frontend_wifi_mapper/*.pyc

.PHONY: managed monitor interface read clean sniff
