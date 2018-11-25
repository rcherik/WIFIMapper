NAME=application.py
#INTERFACE=$(shell /sbin/ip route | awk 'NR==1{print $$5}')
#INTERFACE=$(shell /sbin/ifconfig | /bin/grep '^wl.*Link*.'\
	| /usr/bin/awk '{print $$1}')
INTERFACE=$(shell /sbin/iwconfig 2>&- |\
		  /bin/grep 'IEEE 802.11' |\
		  /usr/bin/awk '{print $$1}')
PYTHON=/usr/bin/python
SUDO=/usr/bin/sudo
APP=application.py
APP_DEBUG=$(APP) --debug

all: sniff

sniff:
	$(SUDO) $(PYTHON) $(APP_DEBUG) --interface $(INTERFACE)

test:
	$(SUDO) $(PYTHON) $(APP_DEBUG) --test

read:
	$(PYTHON) $(APP_DEBUG) --pcap Traces_pcap/unknown_ap.pcap
	make clean

read_1:
	$(PYTHON) $(APP_DEBUG) --pcap Traces_pcap/single_wpa.pcap
	make clean

read_2:
	$(PYTHON) $(APP_DEBUG) --pcap Traces_pcap/double_wpa_and_fail.pcap
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
