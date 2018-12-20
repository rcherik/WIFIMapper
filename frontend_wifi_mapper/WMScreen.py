from __future__ import print_function
from kivy.uix.screenmanager import Screen

class WMScreen(Screen):

    def __init__(self, **kwargs):
        self.current_screen = False
        super(WMScreen, self).__init__(**kwargs)

    def update_gui(self, dic, **kwargs):
        pass

    def set_stop(self, val):
        pass

    def set_pause(self, val):
        pass

    def keyboard_down(self, keyboard, keycode, text, modifiers):
        pass

    def keyboard_up(self, keyboard, keycode):
        pass

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)
        else:
            print(s, **kwargs)
