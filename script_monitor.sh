#!/bin/sh
sudo airmon-ng check kill &&\
sudo ifconfig wlp59s0 down &&\
sudo iwconfig wlp59s0 mode monitor &&\
sudo ifconfig wlp59s0 up
