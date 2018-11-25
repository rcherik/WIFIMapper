from kivy.uix.label import Label
from kivy.uix.actionbar import ActionItem

class WMActionLabel(Label, ActionItem):
    def __init__(self, **kwargs):
        super(WMActionLabel, self).__init__(**kwargs)
