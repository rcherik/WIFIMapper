from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.app import App

class WMImageLink(Image):

    card = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WMImageLink, self).__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and hasattr(touch, "button")\
                and touch.button == "left":
            print("touched ! " + touch.button)
            self.pressed = touch.pos
            screen = self.card.get_info_screen()
            App.get_running_app().add_header(self.card.key, screen)
            return True
        return super(WMImageLink, self).on_touch_up(touch)

    def on_pressed(self, instance, pos):
        self._say("pressed at {pos}".format(pos=pos))
