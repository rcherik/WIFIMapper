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

Builder.load_file("Static/card.kv")

class StationCard(BoxLayout):

    def __init__(self, **kwargs):
        super(StationCard, self).__init__(**kwargs)
        self.key = kwargs['key']
        self.station = kwargs.get('station', None)
        self.vendor = kwargs.get('vendor', None)
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)
        self.connected = False
        self.draw_background(self, self.pos)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("StationCard: Touched !")
            self.pressed = touch.pos
            screen = CardInfoScreen(name=self.id)
            App.get_running_app().add_header(self.id, screen)
            #TODO open a tab with station card infos screen
            return True
        return super(StationCard, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('StationCard: pressed at {pos}'.format(pos=pos))

    def is_connected(self):
        if not self.connected and self.station.bssid:
            self.connected = True
            self.draw_background(self, self.pos)
        elif self.connected and self.station.bssid:
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
