from __future__ import print_function
""" Kivy """
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanelHeader
""" Our stuff """
from MainScreen import MainScreen

class WMScreenManager(ScreenManager):

    def __init__(self, **kwargs):
        """ Add screen for thread accessibility """
        super(WMScreenManager, self).__init__(**kwargs)
        self.app = kwargs.get('app', None)
        self.screen = MainScreen(**kwargs)
        self.add_widget(self.screen)

class WMPanelHeader(TabbedPanelHeader):
    def __init__(self, **kwargs):
        super(WMPanelHeader, self).__init__(**kwargs)
        self.master = kwargs.get('master', None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Panel: Touched ! " + touch.button)
            self.pressed = touch.pos
            if touch.button == "right" and self.text != "Station":
                self.master.remove_widget(self)
                return True
        return super(WMPanelHeader, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print('Panel: pressed at {pos}'.format(pos=pos))
