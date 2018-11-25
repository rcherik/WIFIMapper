from kivy.uix.spinner import Spinner
from kivy.uix.actionbar import ActionItem

class WMActionSpinner(Spinner, ActionItem):
    def __init__(self, **kwargs):
        super(WMActionSpinner, self).__init__(**kwargs)
