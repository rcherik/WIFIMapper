from kivy.properties import ObjectProperty
from kivy.uix.actionbar import ActionToggleButton

class WMActionScreenToggleButton(ActionToggleButton):

    do_down = ObjectProperty(None)
    do_normal = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(WMActionScreenToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, state):
        if self.do_down and state == 'down':
            self.do_down()
        if self.do_normal and state == 'normal':
            self.do_normal()
