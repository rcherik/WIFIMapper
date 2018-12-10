from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView

from toast import toast

Clipboard = None
CutBuffer = None

class WMSelectableLabel(Label):

    def __init__(self, **kwargs):
        self.hidden_text = kwargs.get('hidden_text', "")
	super(WMSelectableLabel, self).__init__(**kwargs)
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
	if not self.collide_point(*touch.pos):
	    return False
	if super(WMSelectableLabel, self).on_touch_down(touch):
	    return True
	touch.grab(self)
	self._touch_count += 1
	if touch.is_double_tap:
	    self.dispatch('on_double_tap')

    def on_double_tap(self, *args):
        if self.hidden_text:
            Clipboard.copy(self.hidden_text)
            toast('Copied', False)
        else:
            toast('No value to copy', False)
