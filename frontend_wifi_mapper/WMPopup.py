from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty

Builder.load_string("""
<WMConfirmPopup>:
    auto_dismiss: True
    title: 'Confirm'
    size_hint: (0.2, 0.2)
    label_text: label_text
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: 0.60
            Label:
                id: label_text
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.4
            Button:
                text: 'Cancel'
                on_release: root.cancel()
            Button:
                text: 'Confirm'
                on_release: root.confirm()
""")

class WMConfirmPopup(Popup):

    label_text = ObjectProperty()

    def __init__(self, text="Smth", **kwargs):
        self.ret = False
        self.text = text
	super(WMConfirmPopup, self).__init__(**kwargs)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args): 
        self.label_text.text = self.text

    def cancel(self):
        self.ret = False
        self.dismiss()

    def confirm(self):
        self.ret = True
        self.dismiss()

    def confirmed(self):
        return self.ret
