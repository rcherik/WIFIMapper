from __future__ import print_function
""" Kivy """
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
""" Our stuff """
import WMScreen
import CardInfoScreen
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES

Builder.load_file("Static/apcardinfoscreen.kv")

class APCardInfoScreen(CardInfoScreen.CardInfoScreen):

    main_layout = ObjectProperty(None)
    card_layout = ObjectProperty(None)
    station_lst = ObjectProperty(None)
    station_hist_lst = ObjectProperty(None)
    info_box = ObjectProperty(None)
    security_box = ObjectProperty(None)
    data_box = ObjectProperty(None)
    station_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.ap = kwargs.get('ap', None)
        self.traffic = kwargs.get('traffic', None)
        self.ready = False
        self.last_n_clients = 0
        self.last_idx_hist = 0
        self.ui_paused = False
	super(APCardInfoScreen, self).__init__(**kwargs)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args): 
       	self.ready = True
        self.update_gui(None, current=True)

    def reload_gui(self, current=True):
        self.update_gui(None, current)

    def set_label(self, label, text):
        if text and label.text != text:
            label.text = text

    def set_info_box(self):
        s = self.ap.bssid
        if self.ap.oui:
            s += " (%s)" % self.ap.oui
        self.set_label(self.info_box.bssid, s)
        s = self.ap.ssid
        if self.ap.channel:
            s += " (%s)" % self.ap.channel
        self.set_label(self.info_box.ssid, s)

    def set_security_box(self):
        self.set_label(self.security_box.co, "co: %d" % self.ap.n_clients)
        self.set_label(self.security_box.security, self.ap.get_security())

    def set_data_box(self):
        sent = "sent: %d" % (self.traffic.sent if self.traffic else 0)
        rcv = "rcv: %d" % (self.traffic.recv if self.traffic else 0)
        beacons = "beacons: %d" % self.ap.beacons
        signal = "sig: %d" % (self.ap.rssi if self.ap.rssi else 0)
        self.set_label(self.data_box.sent, sent)
        self.set_label(self.data_box.rcv, rcv)
        self.set_label(self.data_box.beacons, beacons)
        self.set_label(self.data_box.signal, signal)

    def set_connected(self):
        if self.ap.n_clients != self.last_n_clients:
            self.station_lst.box.clear_widgets()
            for bssid in self.ap.client_co:
                l = Label(text=bssid)
                self.station_lst.box.add_widget(l)
            self.last_n_clients = self.ap.n_clients

    def set_history(self):
        for tupl in reversed(self.ap.client_hist_co[self.last_idx_hist:]):
            if tupl[2] == 'connected':
                l = Label(text="[color=#00FF00]%s - %s[/color]" % (tupl[0], tupl[1]),
                        markup=True)
            else:
                l = Label(text="[color=#FF0000]%s - %s[/color]" % (tupl[0], tupl[1]),
                        markup=True)
            self.station_hist_lst.box.add_widget(l)
        self.last_idx_hist = len(self.ap.client_hist_co)

    def update_gui(self, dic, current=True):
        if not current\
                or not self.ready\
                or self.ui_paused:
            return
        if dic and (self.ap.bssid not in dic[WM_CHANGES][WM_AP]):
            return
        self.set_info_box()
        self.set_security_box()
        self.set_data_box()
        self.set_connected()
        self.set_history()
        
    def set_ui_paused(self):
        self.ui_paused = True

    def set_ui_unpaused(self):
        self.ui_paused = False
        self.reload_gui(current=True)

    def on_pre_enter(self):
        if self.ready:
            self.set_ui_unpaused()

    def on_pre_leave(self):
        if self.ready:
            self.set_ui_paused()
