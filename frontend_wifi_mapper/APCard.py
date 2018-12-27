from __future__ import print_function
import os
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
from kivy.utils import escape_markup
""" Our stuff """
import WMConfig
from APCardInfoScreen import APCardInfoScreen
from WMUtilityClasses import WMSelectableLabel, WMImageLink, WMCard

class APCard(WMCard):

    info_box = ObjectProperty(None)
    security_box = ObjectProperty(None)
    data_box = ObjectProperty(None)
    open_link = ObjectProperty(None)

    def __init__(self, key=None, ap=None, args=None, traffic=None, **kwargs):
        self.key = key
        self.ap = ap
        self.args = args
        self.traffic = traffic
        self.width_mult = WMConfig.conf.label_width_mult
        self.final_width = 0
        self.space = 2
        self.known_bg = False
        self.has_changed = False
        super(APCard, self).__init__(**kwargs)
        self.card_type = "AP"
        self.init_background()
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        self.update(self.ap, self.traffic)
        self.open_link.wmtype = self.card_type
        self.open_link.wmkey = self.ap.bssid
        #self.bssid.bind(on_click_right=self.open_link)

    def update(self, ap, traffic):
        if ap:
            self.ap = ap
        if traffic:
            self.traffic = traffic
        if not self.ap:
            return
        self.has_changed = False
        self.final_width = 0
        self._set_bssid()
        self._set_ssid()
        self._set_security()
        if self.traffic:
            self._set_data()
        self._check_width_changed()
        self._check_known()
        return self.has_changed

    """ Setter for labels """

    def _set_label(self, label, string, copy=""):
        if isinstance(label, WMSelectableLabel):
            if label.check_select_label_text(string):
                self.has_changed = True
                label.set_select_label_text(string)
            label.set_copy(copy)
        elif string != label.text:
            self.has_changed = True
            label.text = string

    def _set_bssid(self):
        s = "[b]%s[/b]" % self.ap.bssid
        if self.ap.oui:
            s += " (%s)" % self.ap.oui
        self._set_label(self.info_box.bssid, s, copy=self.ap.bssid)
        self._check_width(len(s))

    def _set_ssid(self):
        s = ""
        if self.ap.ssid:
            s = "[b][i]%s[/i][/b]" % (self.ap.ssid)
        if self.ap.channel:
            s += " (%s)" % self.ap.channel
        self._set_label(self.info_box.ssid, s, copy=self.ap.ssid)
        self._check_width(len(s))

    def _set_security(self):
        crypto = ""
        if self.ap.security:
            crypto = "[i]%s[/i]" % (self.ap.get_security())
        connected = "co: %d" % self.ap.n_clients
        self._set_label(self.security_box.security, crypto)
        self._set_label(self.security_box.co, connected)
        min_len = 0.5 * self.width
        fun = self._get_min_len
        self._check_width(len(crypto) + self.space + len(connected))

    def _set_data(self):
        sent = "sent: %d" % (self.traffic.sent if self.traffic else 0)
        rcv = "rcv: %d" % (self.traffic.recv if self.traffic else 0)
        beacons = "beacons: %d" % self.ap.beacons
        signal = "sig: %d" % (self.ap.rssi if self.ap.rssi else 0)
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.beacons, beacons)
        self._set_label(self.data_box.signal, signal)
        len1 = len(rcv) + len(beacons)
        len2 = len(sent) + len(signal)
        self._check_width(len1 if len1 > len2 else len2)

    """ Override WMCard """

    def get_name(self):
        return self.ap.get_name()

    def get_obj(self):
        return self.ap

    """ Resize card """

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
  
    """ Background """

    def init_background(self):
	with self.canvas.before:
            if self.clicked:
	        self._color = Color(0, 0, 1, 0.25)
            elif self.ap and self.ap.known:
	        self._color = Color(1, 1, 1, 0.25)
            else:
	        self._color = Color(1, 0, 0, 0.25)
	    self._rectangle = Rectangle(pos=self.pos, size=self.size)

    def draw_background(self, widget, prop):
        self._rectangle.pos = self.pos
        self._rectangle.size = self.size
        if self.clicked:
            self._color.rgba = (0, 0, 1, 0.25)
        elif self.ap and self.ap.known:
            self._color.rgba = (1, 1, 1, 0.25)
        else:
            self._color.rgba = (1, 0, 0, 0.25)
        if self.open_link:
            self.open_link.y = self.y
            self.open_link.x = self.right - self.open_link.width
            #self.open_link.pos = self.pos

Builder.load_file(os.path.join("Static", "apcard.kv"))
