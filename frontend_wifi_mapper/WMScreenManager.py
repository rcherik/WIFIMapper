from __future__ import print_function
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.app import App
""" Our stuff """
from CardListScreen import CardListScreen
from toast import toast

class WMScreenManager(ScreenManager):

    ap_screen = ObjectProperty(None)
    station_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Init screens before super for WMTabbedPanel switch_to """
        self.to_init_screens = []
        self.args = kwargs.get('args', None)
        self._init_screens(**kwargs)
        self.app = kwargs.get('app', None)
        self.pcap_thread = kwargs.get('pcap_thread', None)
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
        if not self.pcap_thread.started:
            self.pcap_thread.start()
        self.app.app_ready()

    def is_ready(self):
        """ Called to check if all screens are init """
        for screen in self.screens:
            if not screen.ready:
                return False
        return True

    def set_input_stop(self, val):
        for screen in self.screens:
            screen.set_stop(val)

    def keyboard_up(self, keyboard, keycode):
        screen = self.get_screen(self.current)
        if screen:
            return screen.keyboard_up(keyboard, keycode)
        return False

    def keyboard_down(self, keyboard, keycode, text, modifiers):
        screen = self.get_screen(self.current)
        if screen:
            return screen.keyboard_down(keyboard, keycode, text, modifiers)
        return False

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

    def open_card_link(self, which, key):
        if which not in ('AP', 'Station'):
            self._say("open_card_link: bad which")
            return
        card = None
        for screen in self.screens:
            if isinstance(screen, CardListScreen)\
                    and screen.wm_screen_type == which:
                card = screen.get_card(key)
                break
        if card:
            screen = card.get_info_screen()
            App.get_running_app().add_header(
                    "%s: %s" % (card.type, card.get_name()),
                    card.key, screen)
        else:
            toast("%s not found" % key)

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and hasattr(self.args, "debug")\
                and self.args.debug:
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
