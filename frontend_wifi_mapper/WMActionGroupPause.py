from kivy.uix.actionbar import ActionGroup
from kivy.properties import ObjectProperty
from kivy.lang import Builder

class WMActionGroupPause(ActionGroup):

    screen = ObjectProperty()

    def __init__(self, **kwargs):
        super(WMActionGroupPause, self).__init__(**kwargs)
        self._dropdown.bind(on_dismiss=self.dismissed)
        self._dropdown.auto_dismiss = False

    def on_press(self):
        pass

    def dismissed(self, widget):
        pass
