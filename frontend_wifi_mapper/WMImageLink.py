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

"""
class WMImageLink(Widget):

    card = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WMImageLink, self).__init__(**kwargs)
        self.bind(size=self.draw_background)
        self.bind(pos=self.draw_background)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and hasattr(touch, "button")\
                and touch.button == "left":
            print("touched ! " + touch.button)
            self.pressed = touch.pos
            screen = self.card.get_info_screen()
            App.get_running_app().add_header(self.card.key, screen)
            return True
        return super(WMImageLink, self).on_touch_up(touch)

    def draw_background(self, widget, prop):
        self.canvas.before.clear()
	with self.canvas.before:
	    Color(1, 0, 0, 0.25)
	    Rectangle(source="Static/images/open2.png",
                    size_hint=(None, 1),
                    pos=self.pos,
                    size=(40, 40))

    def on_pressed(self, instance, pos):
        self._say("pressed at {pos}".format(pos=pos))
"""
