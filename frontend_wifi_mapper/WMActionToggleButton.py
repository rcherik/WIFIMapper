from kivy.uix.actionbar import ActionToggleButton
from kivy.properties import ObjectProperty

class WMActionToggleButton(ActionToggleButton):

    screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WMActionToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, value):
        if hasattr(self, 'screen') and self.screen:
            self.screen.reload_gui()
