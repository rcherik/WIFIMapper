from __future__ import print_function
""" Kivy """
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from operator import attrgetter
""" Our stuff """
import WMCard
from CardInfoScreen import CardInfoScreen

Builder.load_file("Static/apcard.kv")

class APCard(WMCard.WMCard):

    mac = ObjectProperty(None)
    essid = ObjectProperty(None)
    security_box = ObjectProperty(None)
    data_box = ObjectProperty(None)
    seen = ObjectProperty(None)
    vendor_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(APCard, self).__init__(**kwargs)
        self.key = kwargs['key']
        self.ap = kwargs.get('ap', None)
        self.args = kwargs.get('args', None)
        self.traffic = kwargs.get('traffic', None)
        self.width_mult = 8
        self.final_width = 0
        self.space = 2
        self.known_bg = False
        self.has_changed = False
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        self.update(self.ap, self.traffic)

    def update(self, ap, traffic):
        self.final_width = 0
        self.ap = ap
        if traffic:
            self.traffic = traffic
        self.has_changed = False
        self._set_mac()
        self._set_essid()
        self._set_security()
        self._set_data()
        self._check_width_changed()
        self._check_known()
        return self.has_changed

    def _check_known(self):
        if not self.known_bg and self.ap.known:
            self.known_bg = True
            self.draw_background(self, self.pos)
        elif self.known_bg and not self.ap.known:
            self.known_bg = False
            self.draw_background(self, self.pos)

    def _check_width(self, l):
        new_width = l * self.width_mult
        if new_width > self.final_width:
            self.final_width = new_width

    def _check_width_changed(self):
        if self.final_width < self.minimum_width\
            and self.width != self.minimum_width:
            self.width = self.minimum_width
        elif self.final_width > self.minimum_width and\
                self.width != self.final_width:
            self.width = self.final_width

    def _get_min_len(self, string, min_len):
        l = len(string) * self.width_mult
        return l if l > min_len else min_len

    def _set_label(self, label, string):
        if string != label.text:
            self.has_changed = True
            label.text = string

    def _set_mac(self):
        s = "[b]%s[/b]" % self.ap.bssid
        if self.ap.oui:
            s += " (%s)" % self.ap.oui
        self._set_label(self.mac, s)
        self._check_width(len(s))

    def _set_essid(self):
        s = ""
        if self.ap.ssid:
            s = "[b][i]%s[/i][/b]" % (self.ap.ssid)
        if self.ap.channel:
            s += " (%s)" % self.ap.channel
        self._set_label(self.essid, s)
        self._check_width(len(s))

    def _set_security(self):
        crypto = ""
        if self.ap.security:
            crypto = "[i]%s[/i]" % (self.ap.security or "")
        wps_str = "has wps" if self.ap.wps is True else ""
        if self.ap.wps is None:
            wps_str = ""
        wps = "[i]%s[/i]" % (wps_str)
        self._set_label(self.security_box.security, crypto)
        self._set_label(self.security_box.wps, wps)
        min_len = 0.5 * self.width
        fun = self._get_min_len
        self._check_width(len(crypto) + self.space + len(wps))

    def _set_data(self):
        sent = "sent: %d" % (self.traffic.sent if self.traffic else 0)
        rcv = "rcv: %d" % (self.traffic.recv if self.traffic else 0)
        beacons = "beacons: %d" % self.ap.beacons
        signal = "sig: %d" % self.ap.rssi or 0
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.beacons, beacons)
        self._set_label(self.data_box.signal, signal)
        len1 = len(rcv) + len(beacons)
        len2 = len(sent) + len(signal)
        self._check_width(len1 if len1 > len2 else len2)

    def get_obj(self):
        return self.ap
   
    def draw_background(self, widget, prop):
        self.canvas.before.clear()
	with self.canvas.before:
            if self.clicked:
	        Color(0, 0, 1, 0.25)
            elif self.ap.known:
	        Color(1, 1, 1, 0.25)
            else:
	        Color(1, 0, 0, 0.25)
	    Rectangle(pos=self.pos, size=self.size)
