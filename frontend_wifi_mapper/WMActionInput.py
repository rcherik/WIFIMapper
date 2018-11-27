from kivy.uix.actionbar import ActionItem
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

class WMActionInput(TextInput, ActionItem):
    def __init__(self, **kwargs):
        super(WMActionInput, self).__init__(**kwargs)
