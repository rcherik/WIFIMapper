from kivy.uix.actionbar import ActionToggleButton
from kivy.properties import ObjectProperty

class WMSortActionToggleButton(ActionToggleButton):

    def __init__(self, **kwargs):
        self.screen = kwargs.get('screen', None)
        self.key = kwargs.get('key', None)
        self.no_trigger = False
        super(WMSortActionToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, state):
        if self.no_trigger:
            self.no_trigger = False
            return
        if hasattr(self, 'screen') and self.screen:
            if state == 'down':
                self.screen.set_sort(self.key)
