from kivy.uix.actionbar import ActionGroup
from kivy.properties import ObjectProperty
from kivy.lang import Builder

class WMActionGroupPause(ActionGroup):

    screen = ObjectProperty()

    def __init__(self, **kwargs):
        super(WMActionGroupPause, self).__init__(**kwargs)
        self._dropdown.on_dissmiss = lambda x: print "lol"

    def on_press(self):
        print("LOL")
        self.screen.set_paused()

    def dismissed(self):
        print("LOL")
