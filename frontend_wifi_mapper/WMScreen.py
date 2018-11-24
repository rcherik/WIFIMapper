from __future__ import print_function
from kivy.uix.screenmanager import Screen

class WMScreen(Screen):

    def __init__(self, **kwargs):
        super(WMScreen, self).__init__(**kwargs)
        #TODO

    def update_gui(self, dic):
        pass

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)
