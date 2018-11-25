from kivy.uix.actionbar import ActionToggleButton
from kivy.properties import ObjectProperty

class WMPageActionToggleButton(ActionToggleButton):

    screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.page = kwargs.get('page', None)
        self.screen = kwargs.get('screen', None)
        self.init = False
        super(WMPageActionToggleButton, self).__init__(**kwargs)
        self.init = True

    def on_state(self, widget, value):
        if not self.init:
            return
        if self.screen.page_btn and self.screen.page_btn == self:
            return
        if value == 'down':
            self.screen.current_page = self.page
            self.screen.page_btn = self
            self.screen.reload_gui()
