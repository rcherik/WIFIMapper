from __future__ import print_function
""" Kivy """
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.tabbedpanel import TabbedPanelHeader, TabbedPanel
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
""" Our stuff """
from CardListScreen import CardListScreen

Builder.load_file('Static/wmpanel.kv')

class WMScreenManager(ScreenManager):

    ap_screen = ObjectProperty(None)
    station_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.ap_screen = CardListScreen(ap=True,
                name="ap", **kwargs)
        self.station_screen = CardListScreen(station=True,
                name="station", **kwargs)
        super(WMScreenManager, self).__init__(**kwargs)
        self.app = kwargs.get('app', None)
        self.pcapthread = kwargs.get('pcapthread', None)
        self.args = kwargs.get('args', None)
        self.add_widget(self.ap_screen)
        self.add_widget(self.station_screen)
	Clock.schedule_once(self.start_pcapthread)

    def start_pcapthread(self, *args):
        if not self.pcapthread.started:
            self.pcapthread.start()

    def is_ready(self):
        return self.ap_screen.ready and self.station_screen.ready

    def update_gui(self, dic):
        self.ap_screen.update_gui(dic)
        self.station_screen.update_gui(dic)

    def remove(self, screen_name):
        widget = self.get_screen(screen_name)
        if widget:
            self.remove_widget(widget)

    def _say(self, s, **kwargs):
        if self.args and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)

    def __repr__(self):
        return "{c} with screens: {l}"\
                .format(c=self.__class__.__name__, l=self.screens)

class WMTabbedPanel(TabbedPanel):
    """ One day maybe for transition """

    ap_tab = ObjectProperty(None)
    station_tab = ObjectProperty(None)

    def __init__(self, **kwargs):
	self.manager = kwargs.get('manager', None)
	self.ap_tab = kwargs.get('ap', None)
	self.station_tab = kwargs.get('station', None)
        super(WMTabbedPanel, self).__init__(**kwargs)
        self.add_widget(self.station_tab)
        self.header_dic = {"AP": self.ap_tab, "Station": self.station_tab}
        self.args = kwargs.get('args', None)

    def add_header(self, key, screen, **kwargs):
        if key not in self.header_dic:
            self.manager.add_widget(screen)
            header = WMPanelHeader(text=key,
                    master=self,
                    screen=key,
                    content=self.manager,
                    **kwargs)
            self.add_widget(header)
            self.header_dic[key] = header
        else:
            self.switch_to(self.header_dic[key])

    def remove_header(self, string):
        header = self.header_dic.pop(string, None)
        if header:
            self.manager.remove(header.screen)
            self.remove_widget(header)

    def switch_to(self, header):
        # set the Screen manager to load  the appropriate screen
        # linked to the tab head instead of loading content
        if self.manager.screens:
            self.manager.current = header.screen
        else:
            super(WMTabbedPanel, self).switch_to(header)
        # we have to replace the functionality of the original switch_to
        self.current_tab.state = "normal"
        header.state = 'down'
        self._current_tab = header

    def _say(self, s, **kwargs):
        if self.args and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)

class WMPanelHeader(TabbedPanelHeader):

    def __init__(self, **kwargs):
        self.screen = kwargs.get("screen", None)
        self.master = kwargs.get("master", None)
        self.can_remove = kwargs.get("can_remove", True)
        self.ready = False
        super(WMPanelHeader, self).__init__(**kwargs)
        self.args = kwargs.get('args', None)
	Clock.schedule_once(self._created_view)

    def _created_view(self, *args):
        self.ready = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            if touch.button == "middle" and self.can_remove:
                self.master.remove_header(self.text)
                return True
            if touch.button in ("middle", "right"):
                return False
        return super(WMPanelHeader, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        self._say('Panel: pressed at {pos}'.format(pos=pos))

    def _say(self, s, **kwargs):
        if self.args and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)
