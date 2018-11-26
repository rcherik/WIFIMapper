from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionToggleButton

class WMActionPauseToggleButton(ActionToggleButton):

    screen = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(WMActionPauseToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, state):
        if hasattr(self, 'screen') and self.screen:
            if state == 'down':
                self.paused = self.screen.pause_input()
            if state == 'normal':
                self.paused = self.screen.resume_input()
