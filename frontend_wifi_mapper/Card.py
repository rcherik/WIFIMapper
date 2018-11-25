from __future__ import print_function
""" Kivy """
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen
""" Our stuff """
import WMCard
from CardInfoScreen import CardInfoScreen

Builder.load_file("Static/card.kv")

class Card(WMCard.WMCard):

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.key = kwargs['key']
        self.elem_lst = {}
        self.width = 0
        self.card_mult = 8
        self.connected = False
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
        self.create(**kwargs)

    def get_args(self, **kwargs):
        self.text = kwargs.get('text', None)
        self.station = kwargs.get('station', None)

    def create(self, **kwargs):
        self.get_args(**kwargs)
        if self.text:
            self.create_text()
        elif self.station:
            self.create_station()
	    self.is_connected()

    def get_obj(self):
        return self.station

    def parent_get_value(self):
        parent = self.parent
        while not isinstance(parent, Screen):
            parent = parent.parent
        value = parent.sort_by
        return self.get_value(value)

    def _get_nested_attr(self, value):
        try:
            return attrgetter(value)(self)
        except:
            return None

    def get_value(self, value):
        return self._get_nested_attr(value)

    def add_label(self, key, text, max_height):
        text = text or ""
        l = len(text)
        label = Label(text=text,
                    size_hint=(1, max_height))
        self.width = l * self.card_mult\
                if self.width < l * self.card_mult else self.width
        self.elem_lst[key] = label
        self.add_widget(label)

    def create_station(self):
        self.max_height = 0.2
        s = "bssid: " + (self.station.bssid or "")
        self.add_label("station", s, self.max_height)
        s = "ap: " + (self.station.ap_bssid or "")
        self.add_label("bssid", s, self.max_height)
        s = "probes: " + self.station.get_probes()
        self.add_label("probes", s, self.max_height)
        self.add_label("vendor", self.station.vendor, self.max_height)

    def create_text(self):
        infos = self.text.split(';')
        self.max_height = 1.0 / len(infos)
        for i, info in enumerate(infos):
           self.add_label(str(i), info, self.max_height)
 
    def update(self, **kwargs):
        self.get_args(**kwargs)
        if self.text:
            self.update_text()
        elif self.station:
            self.is_connected()
            self.update_station()

    def update_label(self, key, value):
        if not value or self.elem_lst[key].text == value:
            return
        l = len(value)
        self.width = l * self.card_mult\
                if self.width < l * self.card_mult else self.width
        self.elem_lst[key].text = value

    def update_station(self):
        s = "bssid: " + (self.station.bssid or "")
        self.update_label("station", s)
        s = "ap: " + (self.station.ap_bssid or "")
        self.update_label("bssid", s)
        s = "probes: " + self.station.get_probes()
        self.update_label("probes", s)
        self.update_label("vendor", self.station.vendor)

    def update_text(self):
        infos = self.text.split(';')
        for i, info in enumerate(infos):
            self.update_label(str(i), info)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Card: Touched !")
            self.pressed = touch.pos
            screen = CardInfoScreen(name=self.key)
            App.get_running_app().add_header(self.key, screen)
            #TODO open a tab with card infos screen
            return True
        return super(Card, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('Card: pressed at {pos}'.format(pos=pos))

    def is_connected(self):
        if not self.connected and self.station and self.station.ap_bssid:
            self.connected = True
            self.draw_background(self, self.pos)
        elif self.connected and self.station and not self.station.ap_bssid:
            self.connected = False
            self.draw_background(self, self.pos)

    def draw_background(self, widget, prop):
        self.canvas.before.clear()
	with self.canvas.before:
            if self.connected:
	        Color(0, 1, 0, 0.25)
            else:
	        Color(1, 1, 1, 0.1)
	    Rectangle(pos=self.pos, size=self.size)
