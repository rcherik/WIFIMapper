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
        self.monitor_fields = kwargs.get('monitor_fields', None)
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
        self._set_signal()
        self._set_seen()
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
            for mon in self.monitor_fields:
                if label == self._get_nested_attr(mon):
                    self.has_changed = True
            label.text = string

    def _set_mac(self):
        s = "[b]%s[/b]" % self.ap.bssid
        if self.ap.vendor:
            s += " (%s)" % self.ap.vendor
        self._set_label(self.mac, s)
        self._check_width(len(s))

    def _set_essid(self):
        s = ""
        if self.ap.ssid:
            s = "[b][i]%s[/i][/b]" % (self.ap.ssid)
        self._set_label(self.essid, s)
        self._check_width(len(s))

    def _set_security(self):
        crypto = ""
        if self.ap.crypto:
            crypto = "[i]%s[/i]" % (self.ap.crypto or "")
        wps = "[i]/WPS/[/i]"
        self._set_label(self.security_box.security, crypto)
        self._set_label(self.security_box.wps, wps)
        min_len = 0.5 * self.width
        fun = self._get_min_len
        self._check_width(len(crypto) + self.space + len(wps))

    def _set_data(self):
        rcv = "rcv: %s" % (self.traffic.recv if self.traffic else 0)
        sent = "sent: %s" % (self.traffic.sent if self.traffic else 0)
        beacons = "beacons: %s" % self.ap.beacons
        connected = "prsp: %s" % self.ap.proberesp
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.beacons, beacons)
        self._set_label(self.data_box.connected, connected)
        len1 = len(rcv) + len(beacons)
        len2 = len(sent) + len(connected)
        self._check_width(len1 if len1 > len2 else len2)

    def _set_signal(self):
        min_sig = "min: %s" % (self.traffic.min_sig\
                if self.traffic else 0)
        avg_sig = "avg: %s" % (self.traffic.get_rssi_avg()\
                if self.traffic else 0)
        max_sig = "max: %s" % (self.traffic.max_sig\
                if self.traffic else 0)
        self._set_label(self.signal_box.min_sig, min_sig)
        self._set_label(self.signal_box.avg_sig, avg_sig)
        self._set_label(self.signal_box.max_sig, max_sig)
        self._check_width(len(min_sig) + len(avg_sig) + len(max_sig))

    def _set_seen(self):
        if self.ap.known:
            s = ""
        else:
            s = self.ap.get_seen()
        self._set_label(self.seen, s)
        self._check_width(len(s))

    def get_obj(self):
        return self.ap
    
    def on_touch_up(self, touch):
        """ Create a tab with card info when touched """
        if self.collide_point(*touch.pos) and hasattr(touch, "button")\
                and touch.button == "left":
            self._say("touched ! " + touch.button)
            self.pressed = touch.pos
            screen = CardInfoScreen(name=self.key)
            App.get_running_app().add_header(self.key, screen)
            #TODO open a tab with ap card infos screen
            return True
        return super(APCard, self).on_touch_up(touch)

    def on_pressed(self, instance, pos):
        self._say("pressed at {pos}".format(pos=pos))

    def draw_background(self, widget, prop):
        self.canvas.before.clear()
	with self.canvas.before:
            if self.ap.known:
	        Color(1, 1, 1, 0.25)
            else:
	        Color(1, 0, 0, 0.25)
	    Rectangle(pos=self.pos, size=self.size)
