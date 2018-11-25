from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation

class WMCardScrollView(ScrollView):

    def __init__(self, **kwargs):
	super(WMCardScrollView, self).__init__(**kwargs)

    def key_scroll_y(self, value, animate=True):
	dsx, dsy = self.convert_distance_to_scroll(0, value)
	sxp = min(1, max(0, self.scroll_x - dsx))
	syp = min(1, max(0, self.scroll_y - dsy))
	print(syp)
	if animate:
	    if animate is True:
		animate = {'d': 0.2, 't': 'out_quad'}
	    Animation.stop_all(self, 'scroll_x', 'scroll_y')
	    Animation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
	else:
	    self.scroll_y = syp

    def key_scroll_down(self, animate=True):
	return self.key_scroll_y(60, animate)

    def key_scroll_up(self, animate=True):
	return self.key_scroll_y(-60, animate)

    def on_touch_down(self, touch):
	super(WMCardScrollView, self).on_touch_down(touch)

    def on_touch_up(self, touch):
	super(WMCardScrollView, self).on_touch_up(touch)

    def on_touch_move(self, touch):
	super(WMCardScrollView, self).on_touch_move(touch)
