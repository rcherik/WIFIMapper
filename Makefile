NAME=application.py

#Get wifi interface off for monitoring first
INTERFACE=$(shell /sbin/iwconfig 2>&- |\
	  /bin/grep 'IEEE 802.11  Mode:Monitor' |\
	  /usr/bin/awk '{print $$1}' |\
	  head -1)

#Get fallback wifi interface 2 if possible
ifeq ($(INTERFACE),)
    INTERFACE=$(shell /sbin/iwconfig 2>&- |\
	  /bin/grep 'IEEE 802.11  ESSID:off' |\
	  /usr/bin/awk '{print $$1}' |\
	  head -1)
endif

#Get fallback wifi interface
ifeq ($(INTERFACE),)
    INTERFACE=$(shell /sbin/iwconfig 2>&- |\
	  /bin/grep 'IEEE 802.11' |\
	  /usr/bin/awk '{print $$1}' |\
	  head -1)
endif

ifeq ($(INTERFACE),)
    $(info WARNING $$INTERFACE interface [${INTERFACE}])
endif

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

.PHONY: managed monitor interface read read_1 read_2 clean sniff test
