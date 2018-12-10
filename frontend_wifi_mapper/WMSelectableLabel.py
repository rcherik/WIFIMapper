from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.utils import platform

Clipboard = None
CutBuffer = None

class WMSelectableLabel(Label):

    def __init__(self, **kwargs):
	super(WMSelectableLabel, self).__init__(**kwargs)
        self.hidden_text = ""
	self._touch_count = 0
	self.register_event_type('on_double_tap')
	if platform == 'linux':
	    self._ensure_clipboard()

    def _ensure_clipboard(self):
	global Clipboard, CutBuffer
	if not Clipboard:
	    from kivy.core.clipboard import Clipboard

    def on_touch_down(self, touch):
	if self.disabled:
	    return
	touch_pos = touch.pos
	if not self.collide_point(*touch_pos):
	    return False
	if super(WMSelectableLabel, self).on_touch_down(touch):
	    return True
	touch.grab(self)
	self._touch_count += 1
	if touch.is_double_tap:
	    self.dispatch('on_double_tap')

    def on_double_tap(self, *args):
	Clipboard.copy(self.text)  # <-- How do I do this the correct way?
	print("Copied :D")
