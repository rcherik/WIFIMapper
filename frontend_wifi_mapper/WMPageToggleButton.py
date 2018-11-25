from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty

class WMPageToggleButton(ToggleButton):

    screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.page = kwargs.get('page', None)
        self.screen = kwargs.get('screen', None)
        self.init = False
        super(WMPageToggleButton, self).__init__(**kwargs)
        self.init = True

    def on_state(self, widget, value):
        if not self.init:
            return
        if value == 'down':
            self.screen.current_page = self.page
            self.screen.reload_gui()
