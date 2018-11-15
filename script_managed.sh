#!/bin/sh
sudo ifconfig wlp59s0 down &&\
sudo iwconfig wlp59s0 mode managed &&\
sudo ifconfig wlp59s0 up &&\
sudo /etc/init.d/network-manager start
