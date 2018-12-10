from __future__ import print_function
import copy
""" Kivy """
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.uix.tabbedpanel import TabbedPanelHeader, TabbedPanel
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import Image
""" Our stuff """
from CardListScreen import CardListScreen

Builder.load_file('Static/wmpanel.kv')

class WMScreenManager(ScreenManager):

    ap_screen = ObjectProperty(None)
    station_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Init screens before super for WMTabbedPanel switch_to """
        self.to_init_screens = []
        self.args = kwargs.get('args', None)
        self._init_screens(**kwargs)
        self.app = kwargs.get('app', None)
        self.pcapthread = kwargs.get('pcapthread', None)
        super(WMScreenManager, self).__init__(**kwargs)
        self.transition = SlideTransition()
        for screen in self.to_init_screens:
            self.add_widget(screen)
        del self.to_init_screens
        self.img_open = Image(source="Static/images/open2.png")
        self.img_home = Image(source="Static/images/home.png")
	Clock.schedule_once(self._manager_ready)

    def _manager_ready(self, *args):
        """ When kv loaded, may start thread """
        if not self.pcapthread.started:
            self.pcapthread.start()

    def is_ready(self):
        """ Called to check if all screens are init """
        for screen in self.screens:
            if not screen.ready:
                return False
        return True

    def set_input_stop(self, val):
        for screen in self.screens:
            screen.set_stop(val)

    def keyboard_down(self, keyboard, keycode, text, modifiers):
        screen = self.get_screen(self.current)
        if screen:
            screen.keyboard_down(keyboard, keycode, text, modifiers)
        return True

    def update_gui(self, dic):
        for screen in self.screens:
            if self.current == screen.name:
                screen.update_gui(dic, current=True)
            else:
                screen.update_gui(dic, current=False)

    def remove(self, screen_name):
        widget = self.get_screen(screen_name)
        if widget:
            self.remove_widget(widget)

    def _to_init_screen(self, **kwargs):
        """ Create and postpone adding """
        screen = CardListScreen(**kwargs)
        self.to_init_screens.append(screen)

    def _init_screens(self, **kwargs):
        """ Init screens for later adding """
        self._to_init_screen(ap=True,
                name="ap", **kwargs)
        self._to_init_screen(station=True,
                name="station", **kwargs)

    def add_cardlist_screen(self, **kwargs):
        screen = CardListScreen(**kwargs)
        self.add_widget(screen)

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)
        else:
            print(s, **kwargs)

    def __repr__(self):
        return "{c} with screens: {l}"\
                .format(c=self.__class__.__name__, l=self.screens)

    def change_screen(self, name):
        self.transition.direction = self.get_transition_direction(name)
        self.current = name

    def get_transition_direction(self, name):
        found = False
        for screen in self.screens:
            if screen.name == name:
                found = True
            if screen.name == self.current:
                if found:
                    return "right"
                break
        return "left"

class WMTabbedPanel(TabbedPanel):
    """ One day maybe for transition """

    ap_tab = ObjectProperty(None)
    station_tab = ObjectProperty(None)

    def set_tab(self, key, **kwargs):
        tab = WMPanelHeader(**kwargs)
        self.header_dic[key] = tab

    def _init_tabs(self):
        self.set_tab("Stations",
                text="Stations",
                screen="station",
                args=self.args,
                content=self.manager,
                can_remove=False)

    def __init__(self, **kwargs):
	self.manager = kwargs.get('manager', None)
	self.ap_tab = kwargs.get('ap', None)
        self.args = kwargs.get('args', None)
        self.header_dic = {}
        self._init_tabs()
        super(WMTabbedPanel, self).__init__(**kwargs)
        for key, value in self.header_dic.iteritems():
            self.add_widget(value)
        self.header_dic["AP"] = self.default_tab

    def change_header(self, key, txt):
        if key in self.header_dic:
            self.header_dic[key].text = txt

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
            self.manager.change_screen(header.screen)
        else:
            super(WMTabbedPanel, self).switch_to(header)
        # we have to replace the functionality of the original switch_to
        self.current_tab.state = "normal"
        header.state = 'down'
        self._current_tab = header

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
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
            if not hasattr(touch, "button"):
                return super(WMPanelHeader, self).on_touch_down(touch)
            if touch.button == "middle" and self.can_remove:
                self.master.remove_header(self.text)
                return True
            if touch.button in ("middle", "right"):
                return False
        return super(WMPanelHeader, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        self._say('Panel: pressed at {pos}'.format(pos=pos))

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)
