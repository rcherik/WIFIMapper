from __future__ import print_function
""" Kivy """
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.app import App
""" Our stuff """

Builder.load_file("Static/card.kv")

class Card(BoxLayout):

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)
        self.id = kwargs['id']
        self.elem_lst = {}
        self.width = 0
        self.connected = False
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
        self.create(**kwargs)

    def get_args(self, **kwargs):
        self.text = kwargs.get('text', None)
        self.ap = kwargs.get('ap', None)
        self.station = kwargs.get('station', None)
        self.vendor = kwargs.get('vendor', None)

    def create(self, **kwargs):
        self.get_args(**kwargs)
        if self.text:
            self.create_text()
        elif self.ap:
            self.create_ap()
        elif self.station:
            self.create_station()
	    self.is_connected()

    def add_label(self, key, text, max_height):
        text = text or ""
        l = len(text)
        label = Label(text=text,
                    size_hint=(1, max_height))
        self.width = l * 10 if self.width < l * 10 else self.width
        self.elem_lst[key] = label
        self.add_widget(label)

    def create_ap(self):
        self.max_height = 0.33
        s = "ssid: " + (self.ap.ssid or "")
        self.add_label("ssid", s, self.max_height)
        s = "bssid: " + (self.ap.bssid or "")
        self.add_label("bssid", s, self.max_height)
        self.add_label("vendor", self.vendor, self.max_height)

    def create_station(self):
        self.max_height = 0.2
        s = "ssid: " + (self.station.station or "")
        self.add_label("station", s, self.max_height)
        s = "ap: " + (self.station.bssid or "")
        self.add_label("bssid", s, self.max_height)
        s = "probes: " + self.station.get_probes()
        self.add_label("probes", s, self.max_height)
        self.add_label("vendor", self.vendor, self.max_height)

    def create_text(self):
        infos = self.text.split(';')
        self.max_height = 1.0 / len(infos)
        for i, info in enumerate(infos):
           self.add_label(str(i), info, self.max_height)
 
    def update(self, **kwargs):
        self.get_args(**kwargs)
        if self.text:
            self.update_text()
        elif self.ap:
            self.update_ap()
        elif self.station:
            self.is_connected()
            self.update_station()

    def update_label(self, key, value):
        if not value or self.elem_lst[key].text == value:
            return
        l = len(value)
        self.width = l * 10 if self.width < l * 10 else self.width
        self.elem_lst[key].text = value

    def update_ap(self):
        s = "ssid: " + (self.ap.ssid or "")
        self.update_label("ssid", s)
        s = "bssid: " + (self.ap.bssid or "")
        self.update_label("bssid", s)
        self.update_label("vendor", self.vendor)

    def update_station(self):
        s = "ssid: " + (self.station.station or "")
        self.update_label("station", s)
        s = "ap: " + (self.station.bssid or "")
        self.update_label("bssid", s)
        s = "probes: " + self.station.get_probes()
        self.update_label("probes", s)
        self.update_label("vendor", self.vendor)

    def update_text(self):
        infos = self.text.split(';')
        for i, info in enumerate(infos):
            self.update_label(str(i), info)

    def on_touch_down(self, touch):
        #TODO open a tab with card infos
        if self.collide_point(*touch.pos):
            print("Card: Touched !")
            self.pressed = touch.pos
            App.get_running_app().add_panel(str(self.id), self)
            return True
        return super(Card, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('Card: pressed at {pos}'.format(pos=pos))

    def is_connected(self):
        if not self.connected and self.station and self.station.bssid:
            self.connected = True
            self.draw_background(self, self.pos)
        elif self.connected and self.station and not self.station.bssid:
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

