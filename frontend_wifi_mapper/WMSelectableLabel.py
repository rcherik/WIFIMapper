from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.utils import escape_markup
from kivy.clock import Clock

from toast import toast

Clipboard = None

class WMSelectableLabel(Label):

    def __init__(self, **kwargs):
        self.hidden_text = kwargs.get('hidden_text', "")
        self.can_copy = kwargs.get('can_copy', True)
	self.register_event_type('on_double_tap')
	super(WMSelectableLabel, self).__init__(**kwargs)
	self._touch_count = 0
        self.markup = True
	if platform == 'linux':
	    self._ensure_clipboard()
        self.no_color_text = ""
        self.event_unclick = None

    def _ensure_clipboard(self):
	global Clipboard
	if not Clipboard:
	    from kivy.core.clipboard import Clipboard

    def set_clicked(self, value):
        if not self.no_color_text:
            self.no_color_text = value
            self.text = "[color=0000ff]%s[/color]" % value

    def set_unclicked(self, *args):
        if self.no_color_text:
            self.text = self.no_color_text
            self.no_color_text = ""

    def set_copy(self, value):
        if isinstance(value, basestring):
            self.hidden_text = value
        else:
            self.hidden_text = ""

    def is_clicked(self):
        return self.no_color_text

    def set_select_label_text(self, value):
        if self.is_clicked():
            self.set_clicked(value)
        else:
            self.text = value

    def check_select_label_text(self, value):
        if self.is_clicked():
            return value != self.no_color_text
        else:
            return value != self.text

    def add_event(self):
        if self.event_unclick:
            Clock.unschedule(self.event_unclick)
            self.event_unclick = None
        self.event_unclick = Clock.schedule_once(self.set_unclicked, 0.2)

    def on_touch_down(self, touch):
	if self.disabled:
	    return False
	if not self.collide_point(*touch.pos):
	    return False
	if super(WMSelectableLabel, self).on_touch_down(touch):
	    return True
        if not self.can_copy or (hasattr(touch, "button") and touch.button != 'left'):
            return True
        self.set_clicked(self.text)
        self.add_event()
	touch.grab(self)
	self._touch_count += 1
	if hasattr(touch, "is_double_tap") and touch.is_double_tap:
	    self.dispatch('on_double_tap')
        return True

    def on_double_tap(self, *args):
        if self.hidden_text:
            Clipboard.copy(self.hidden_text)
            toast('Copied', False)
        else:
            toast('No value to copy', False)
        self.set_unclicked()
