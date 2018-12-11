from __future__ import print_function
""" Kivy """
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.clock import Clock
""" Our stuff """
from CardInfoScreen import CardInfoScreen
import WMCard
import WMSelectableLabel

Builder.load_file("Static/stationcard.kv")

class StationCard(WMCard.WMCard):

    bssid = ObjectProperty(None)
    ap_bssid = ObjectProperty(None)
    model = ObjectProperty(None)
    probes = ObjectProperty(None)
    data_box = ObjectProperty(None)
    open_link = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(StationCard, self).__init__(**kwargs)
        self.key = kwargs['key']
        self.station = kwargs.get('station', None)
        self.args = kwargs.get('args', None)
        self.traffic = kwargs.get('traffic', None)
        self.width_mult = 8
        self.final_width = 0
        self.space = 2
        self.known_bg = False
        self.has_changed = False
        self.init_background()
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
        self.ready = False
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        self.update(self.station, self.traffic)
        self.ready = True
        self.open_link.card = self

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

    def _set_label(self, label, string, copy=""):
        if isinstance(label, WMSelectableLabel.WMSelectableLabel):
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
        self._set_label(self.bssid, s, copy=self.station.bssid)
        self._check_width(len(s))

    def _set_ap_bssid(self):
        s = ""
        if self.station.ap_bssid:
            s = "[i]AP:[/i] [b]%s[/b]" % (self.station.ap_bssid)
        if self.station.channel:
            s += " (%s)" % self.station.channel
        self._set_label(self.ap_bssid, s, copy=self.station.ap_bssid)
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
            s = "[b][i]%s[/i][/b]" % (model if model != False else "not found")
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

    def get_obj(self):
        return self.station

    def get_info_screen(self):
        #TODO
        return None

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
