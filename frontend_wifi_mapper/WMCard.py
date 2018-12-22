from __future__ import print_function
from kivy.uix.boxlayout import BoxLayout

class WMCard(BoxLayout):

    def __init__(self, **kwargs):
        self.clicked = False
        self.type = None
        super(WMCard, self).__init__(**kwargs)

    def _get_nested_attr(self, value):
        try:
            return attrgetter(value)(self)
        except:
            return None

    def get_name(self):
        return ""

    def get_value(self, value):
        return self._get_nested_attr(value)

    def get_obj(self):
        pass

    def get_info_screen(self):
        return None

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)
        else:
            print(s, **kwargs)
 
    def on_pressed(self, instance, pos):
        self._say("pressed at {pos}".format(pos=pos))

    def on_touch_up(self, touch):
        ret = super(WMCard, self).on_touch_up(touch)
        if not ret and self.collide_point(*touch.pos)\
                and hasattr(touch, "button")\
                and touch.button == "left":
            self.pressed = touch.pos
            self.clicked = not self.clicked
            self.draw_background(self, self.pos)
        return ret

    def draw_background(self, widget, prop):
        pass
