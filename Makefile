NAME=application.py
INTERFACE=$(shell /sbin/ip route | awk 'NR==1{print $$5}')
PYTHON=/usr/bin/python
SUDO=/usr/bin/sudo

all: $(NAME)

$(NAME):
	$(SUDO) $(PYTHON) application.py

read:
	$(PYTHON) application.py --pcap Traces_pcap/unknown_ap.pcap

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
	rm -f front_wifi_mapper/*.pyc

.PHONY: managed monitor interface read clean
