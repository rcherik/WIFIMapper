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

Builder.load_file("Static/apcard_2.kv")

class APCard(BoxLayout):

    mac = ObjectProperty(None)
    essid = ObjectProperty(None)
    security_box = ObjectProperty(None)
    data_box = ObjectProperty(None)
    seen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(APCard, self).__init__(**kwargs)
        self.key = kwargs['key']
        self.ap = kwargs.get('ap', None)
        self.traffic = kwargs.get('traffic', None)
        self.vendor = kwargs.get('vendor', None)
        self.width_mult = 8
        self.final_width = 0
        self.space = 2
        self.known = False
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        self.update(self.ap, self.traffic, self.vendor)

    def update(self, ap, traffic, vendor):
        self.final_width = 0
        self.ap = ap
        self.traffic = traffic
        self.vendor = vendor
        self._set_mac()
        self._set_essid()
        self._set_security()
        self._set_data()
        self._set_signal()
        self._set_seen()
        self._check_width_changed()
        self._check_known()

    def _check_known(self):
        if not self.known and self.ap.is_known():
            self.known = True
            self.draw_background(self, self.pos)
        elif self.known and not self.ap.is_known():
            self.known = False
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
            label.text = string

    def _set_mac(self):
        s = "[b]mac: %s[/b]" % self.ap.bssid
        self._set_label(self.mac, s)
        self._check_width(len(s))

    def _set_essid(self):
        s = "[b][i]essid: %s[/i][/b]" % (self.ap.ssid or "")
        self._set_label(self.essid, s)
        self._check_width(len(s))

    def _set_security(self):
        crypto = "crypto: [i]%s[/i]" % (self.ap.crypto or "")
        wps = "no wps yet"
        self._set_label(self.security_box.security, crypto)
        self._set_label(self.security_box.wps, wps)
        min_len = 0.5 * self.width
        fun = self._get_min_len
        self._check_width(len(crypto) + self.space + len(wps))

    def _set_data(self):
        rcv = "r: %s" % (self.traffic.recv if self.traffic else 0)
        sent = "s: %s" % (self.traffic.sent if self.traffic else 0)
        beacons = "b: %s" % self.ap.beacons
        connected = "prsp: %s" % self.ap.proberesp
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.beacons, beacons)
        self._set_label(self.data_box.connected, connected)
        len1 = len(rcv) + len(beacons)
        len2 = len(sent) + len(connected)
        self._check_width(len1 if len1 > len2 else len2)
        #self._check_width(sum(len(s) + self.space\
        #        for s in (rcv, sent, beacons, connected)))

    def _set_signal(self):
        min_sig = "mi: %s" % (self.traffic.min_sig if self.traffic else 0)
        avg_sig = "a: %s" % (self.traffic.get_rssi_avg() if self.traffic else 0)
        max_sig = "m: %s" % (self.traffic.max_sig if self.traffic else 0)
        self._set_label(self.signal_box.min_sig, min_sig)
        self._set_label(self.signal_box.avg_sig, avg_sig)
        self._set_label(self.signal_box.max_sig, max_sig)
        self._check_width(len(min_sig) + len(avg_sig) + len(max_sig))

    def _set_seen(self):
        if self.known:
            s = ""
        else:
            s = self.ap.get_seen()
        self._set_label(self.seen, s)
        self._check_width(len(s))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.button == "left":
            print("APCard: Touched !")
            self.pressed = touch.pos
            screen = CardInfoScreen(name=self.key)
            App.get_running_app().add_header(self.key, screen)
            #TODO open a tab with ap card infos screen
            return True
        return super(APCard, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('APCard: pressed at {pos}'.format(pos=pos))

    def draw_background(self, widget, prop):
        self.canvas.before.clear()
	with self.canvas.before:
            if self.known:
	        Color(1, 1, 1, 0.25)
            else:
	        Color(1, 0, 0, 0.25)
	    Rectangle(pos=self.pos, size=self.size)