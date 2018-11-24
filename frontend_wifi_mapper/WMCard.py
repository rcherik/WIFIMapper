from __future__ import print_function
from kivy.uix.boxlayout import BoxLayout

class WMCard(BoxLayout):

    def __init__(self, **kwargs):
        super(WMCard, self).__init__(**kwargs)
        #TODO

    def _get_nested_attr(self, value):
        try:
            return attrgetter(value)(self)
        except:
            return None

    def get_value(self, value):
        return self._get_nested_attr(value)

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)
