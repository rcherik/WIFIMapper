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
""" Our stuff """
from StationCardInfoScreen import StationCardInfoScreen
from WMUtilityClasses import WMSelectableLabel, WMCard
import WMConfig

Builder.load_file(os.path.join("Static", "stationcard.kv"))

class StationCard(WMCard):

    info_box = ObjectProperty(None)
    data_box = ObjectProperty(None)
    model = ObjectProperty(None)
    probes = ObjectProperty(None)
    open_link = ObjectProperty(None)

    def __init__(self, key=None, station=None, args=None, traffic=None, **kwargs):
        self.key = key
        self.station = station
        self.args = args
        self.traffic = traffic
        self.width_mult = WMConfig.conf.label_width_mult
        self.final_width = 0
        self.space = 2
        self.known_bg = False
        self.has_changed = False
        super(StationCard, self).__init__(**kwargs)
        self.card_type = "Sta"
        self.init_background()
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        self.update(self.station, self.traffic)
        self.open_link.wmtype = self.card_type
        self.open_link.wmkey = self.station.bssid

    def update(self, station, traffic):
        self.final_width = 0
        self.station = station
        if traffic:
            self.traffic = traffic
        self.has_changed = False
        self._set_bssid()
        self._set_ap_bssid()
        self._set_model()
        self._set_probes()
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
        if string != label.text:
            self.has_changed = True
            label.text = string

    def _set_bssid(self):
        s = "[b]%s[/b]" % self.station.bssid
        if self.station.oui:
            s += " (%s)" % self.station.oui
        self._set_label(self.info_box.bssid, s, copy=self.station.bssid)
        self._check_width(len(s))

    def _set_ap_bssid(self):
        s = ""
        ap_bssid = self.station.ap_bssid
        if ap_bssid:
            s = "[i]AP:[/i] [b]%s[/b]" % (self.station.get_ap_name(ap_bssid))
        if self.station.channel:
            s += " (%s)" % self.station.channel
        self._set_label(self.info_box.ap_bssid, s, copy=ap_bssid)
        self._check_width(len(s))

    def _set_probes(self):
        s = ""
        probes = self.station.get_ap_probed()
        if probes:
            s = "[i]probed: %s[/i]" % (probes)
        self._set_label(self.probes, s, copy=probes)
        #self._check_width(len(s))

    def _set_model(self):
        s = ""
        model = self.station.model
        if model != None:
            s = "model: "
            s += "[b][i]%s[/i][/b]" % (model if model != False else "not found")
        self._set_label(self.model, s, copy=model)
        self._check_width(len(s))

    def _set_data(self):
        sent = "sent: %d" % (self.traffic.sent if self.traffic else 0)
        rcv = "rcv: %d" % (self.traffic.recv if self.traffic else 0)
        sig = "sig: %d" % (self.station.rssi if self.station.rssi else 0)
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.sig, sig)
        size = len(sent) + len(rcv) + len(sig)
        self._check_width(size)

    """ Override WMCard """

    def get_name(self):
        return self.station.get_name()

    def get_obj(self):
        return self.station

    """ Resize Card """

    def _check_known(self):
        if not self.known_bg and self.station.connected:
            self.known_bg = True
            self.draw_background(self, self.pos)
        elif self.known_bg and not self.station.connected:
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
            elif self.station.connected:
	        self._color = Color(0, 1, 0, 0.25)
            else:
	        self._color = Color(1, 1, 1, 0.25)
	    self._rectangle = Rectangle(pos=self.pos, size=self.size)

    def draw_background(self, widget, prop):
        self._rectangle.pos = self.pos
        self._rectangle.size = self.size
        if self.clicked:
            self._color.rgba = (0, 0, 1, 0.25)
        elif self.station.connected:
            self._color.rgba = (0, 1, 0, 0.25)
        else:
            self._color.rgba = (1, 1, 1, 0.25)
        if self.open_link:
            self.open_link.y = self.y
            self.open_link.x = self.right - self.open_link.width
            #self.open_link.pos = self.pos
