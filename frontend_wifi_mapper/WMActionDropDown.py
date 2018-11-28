from kivy.uix.actionbar import ActionItem
from kivy.uix.actionbar import ActionDropDown
from kivy.lang import Builder

Builder.load_file('Static/wmactiondropdown.kv')

class WMActionDropDown(ActionDropDown):

    def __init__(self, **kwargs):
        super(WMActionDropDown, self).__init__(**kwargs)
