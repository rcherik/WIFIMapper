from __future__ import print_function
""" Kivy """
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
""" Our stuff """
from Card import Card

Builder.load_file("Static/mainscreen.kv")

class MainScreen(Screen):

    view = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Delays view creation """
	super(MainScreen, self).__init__(**kwargs)
        self.ready = False
	self.card_dic = {}
        self.app = kwargs.get('app', None)
        self.show_ap = kwargs.get('ap', False)
	self.show_station = kwargs.get('station', False)

        """ Python background color """
	with self.canvas.before:
	    Color(0, 0, 0, 0)
	    self.rect = Rectangle(size=self.size, pos=self.pos)
	self.bind(size=self._update_rect, pos=self._update_rect)

	Clock.schedule_once(self.create_view)

    def _update_rect(self, instance, value):
        """ Update background color """
	self.rect.pos = instance.pos
	self.rect.size = instance.size

    def create_view(self, dt):
        """ Create layout """
        self.layout = StackLayout(orientation="lr-tb",
                padding=10,
                spacing=10,
                size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.view.add_widget(self.layout)
        self.ready = True

    def add_ap_card(self, mac, ap, vendor):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = Card(id=mac, ap=ap, vendor=vendor)
            self.layout.add_widget(card)
            self.card_dic[mac] = card
        else:
            self.card_dic[mac].update(id=mac, ap=ap, vendor=vendor)

    def add_station_card(self, mac, station, vendor):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = Card(id=mac, station=station, vendor=vendor)
            self.layout.add_widget(card)
            self.card_dic[mac] = card
        else:
            self.card_dic[mac].update(id=mac, station=station, vendor=vendor)

    def add_card(self, mac, s, vendor):
        """ Add button or update it """
        if mac not in self.card_dic:
            s = s or ""
            card = Card(id=mac, text=s, vendor=vendor)
            self.layout.add_widget(card)
            self.card_dic[mac] = card
        else:
            self.card_dic[mac].update(id=mac, text=s, vendor=vendor)

    def update_gui(self, dic, vendor_dic):
        """ Update GUI """
        if self.show_ap:
            ap = dic['AP']
            for key, value in ap.iteritems():
                vendor = vendor_dic.get(key[:8].upper(), "")
                self.add_ap_card(key, ap[key], vendor)
        if self.show_station:
            sta = dic['Station']
            for key, value in sta.iteritems():
                probes = sta[key].get_probes()
                s = "%s;%s;%s" % (key, probes, key)
                vendor = vendor_dic.get(key[:8].upper(), "")
                self.add_station_card(key, sta[key], vendor)


