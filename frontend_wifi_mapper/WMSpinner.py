from kivy.uix.spinner import Spinner
from kivy.uix.actionbar import ActionItem

class WMSpinner(Spinner, ActionItem):
    def __init__(self, **kwargs):
        super(WMSpinner, self).__init__(**kwargs)
