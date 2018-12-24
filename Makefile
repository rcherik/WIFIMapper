OS := $(shell uname)

ifeq ($(OS),Linux)
	SHELL := /bin/bash
	GREP := /bin/grep
else
	SHELL := /bin/sh
	GREP := /usr/bin/grep
endif


#Get wifi interface off for monitoring first
INTERFACE=$(shell /sbin/iwconfig 2>&- |\
	  $(GREP) 'IEEE 802.11  Mode:Monitor' |\
	  /usr/bin/awk '{print $$1}' |\
	  head -1)
TYPE="already_monitored"

#Get fallback wifi interface 2 if possible
ifeq ($(INTERFACE),)
    INTERFACE=$(shell /sbin/iwconfig 2>&- |\
	  $(GREP) 'IEEE 802.11  ESSID:off' |\
	  /usr/bin/awk '{print $$1}' |\
	  head -1)
    TYPE="two_iface"
endif

#Get fallback wifi interface
ifeq ($(INTERFACE),)
    INTERFACE=$(shell /sbin/iwconfig 2>&- |\
	  $(GREP) 'IEEE 802.11' |\
	  /usr/bin/awk '{print $$1}' |\
	  head -1)
    TYPE="one_iface"
endif

NAME=main.py
INSTALL_FOLDER=Install_Folder
PYTHON=/usr/bin/python
SUDO=/usr/bin/sudo
APP=$(NAME)
APP_DEBUG=$(APP) --debug

SCAPY := $(shell command -v scapy 2> /dev/null)

all: sniff

install:
	@printf "Installing dependencies for wifi mapper\n\n"
	$(SUDO) /usr/bin/apt install git gcc python-kivy python-matplotlib python-docutils python-psutil
	pip install kivy-garden --user
	garden install matplotlib
ifndef SCAPY
	@if [ -d "$(INSTALL_FOLDER)/scapy"]; then \
		/bin/mkdir -p $(INSTALL_FOLDER) &&\
		/usr/bin/git clone https://github.com/secdev/scapy.git $(INSTALL_FOLDER)/scapy; \
	fi
	@cd $(INSTALL_FOLDER)/scapy &&\
	$(PYTHON) setup.py build &&\
	$(SUDO) $(PYTHON) setup.py install --record files.txt && cd -
else
	@printf "\nScapy already installed\n\n"
endif

# To remove scapy, go to $(INSALL_FOLDER)/scapy and make: cat files.txt | xargs rm -rf

sniff:
ifeq ($(INTERFACE),)
	$(error $$INTERFACE is [${INTERFACE}] -- Cannot sniff from Makefile !)
endif
	$(SUDO) $(PYTHON) $(APP_DEBUG) --interface $(INTERFACE)
	@make clean

test:
	$(SUDO) $(PYTHON) $(APP_DEBUG) --test
	@make clean

read:
	$(PYTHON) $(APP_DEBUG) --pcap Traces_pcap/unknown_ap.pcap
	@make clean

read_1:
	$(PYTHON) $(APP_DEBUG) --pcap Traces_pcap/single_wpa.pcap
	@make clean

read_2:
	$(PYTHON) $(APP_DEBUG) --pcap Traces_pcap/double_wpa_and_fail.pcap
	@make clean

managed:
	$(SUDO) /usr/sbin/airmon-ng check kill &&\
	$(SUDO) /sbin/ifconfig $(INTERFACE) down &&\
	$(SUDO) /sbin/iwconfig $(INTERFACE) mode managed &&\
	$(SUDO) /sbin/ifconfig $(INTERFACE) up &&\
	$(SUDO) /etc/init.d/network-manager start

monitor:
	$(SUDO) /usr/sbin/airmon-ng check kill &&\
	$(SUDO) /sbin/ifconfig $(INTERFACE) down &&\
	$(SUDO) /sbin/iwconfig $(INTERFACE) mode monitor &&\
	$(SUDO) /sbin/ifconfig $(INTERFACE) up &&\
	if [ $(TYPE) == "two_ifaces" ]; then \
	    $(SUDO) /etc/init.d/network-manager start ; \
	fi

interface:
	@echo "using interface: $(INTERFACE)"

clean:
	rm -f *.pyc
	rm -f backend_wifi_mapper/*.pyc
	rm -f frontend_wifi_mapper/*.pyc

fclean:
	rm -rf logs/*.txt
	rm -f wifimapper.ini
	rm -rf backend_wifi_mapper/Utilities/C/create_signature

.PHONY: managed monitor interface read read_1 read_2 clean sniff test install fclean
.IGNORE:
.SILENT: clean fclean

