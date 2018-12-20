from __future__ import print_function
import copy
""" Kivy """
from kivy.uix.tabbedpanel import TabbedPanelHeader, TabbedPanel
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string("""
<WMTabbedPanel>:
	tab_width: 150
""")

class WMTabbedPanel(TabbedPanel):
    """ One day maybe for transition """

    ap_tab = ObjectProperty(None)
    station_tab = ObjectProperty(None)

    def set_tab(self, key, **kwargs):
        tab = WMPanelHeader(**kwargs)
        self.header_dic[key] = tab

    def _init_tabs(self):
        self.set_tab("Stations",
                text="Stations",
                screen="station",
                args=self.args,
                #background_color=(80, 0, 80, 0.25),
                content=self.manager,
                can_remove=False)

    def __init__(self, **kwargs):
	self.manager = kwargs.get('manager', None)
	self.ap_tab = kwargs.get('ap', None)
        self.args = kwargs.get('args', None)
        self.header_dic = {}
        self._init_tabs()
        super(WMTabbedPanel, self).__init__(**kwargs)
        for key, value in self.header_dic.iteritems():
            self.add_widget(value)
        self.header_dic["AP"] = self.default_tab

    def change_header(self, key, txt):
        if key in self.header_dic:
            self.header_dic[key].text = txt

    def add_header(self, key, screen, **kwargs):
        if key not in self.header_dic:
            self.manager.add_widget(screen)
            header = WMPanelHeader(text=key,
                    master=self,
                    screen=key,
                    content=self.manager,
                    **kwargs)
            self.add_widget(header)
            self.header_dic[key] = header
        else:
            self.switch_to(self.header_dic[key])

    def remove_header(self, string):
        header = self.header_dic.pop(string, None)
        if header:
            self.manager.remove(header.screen)
            self.remove_widget(header)


    def switch_to(self, header):
        # set the Screen manager to load  the appropriate screen
        # linked to the tab head instead of loading content
        if self.manager.screens:
            self.manager.change_screen(header.screen)
        else:
            super(WMTabbedPanel, self).switch_to(header)
        # we have to replace the functionality of the original switch_to
        self.current_tab.state = "normal"
        header.state = 'down'
        self._current_tab = header

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
            print(s, **kwargs)
        else:
            print(s, **kwargs)

class WMPanelHeader(TabbedPanelHeader):

    def __init__(self, **kwargs):
        self.screen = kwargs.get("screen", None)
        self.master = kwargs.get("master", None)
        self.can_remove = kwargs.get("can_remove", True)
        self.ready = False
        super(WMPanelHeader, self).__init__(**kwargs)
        self.args = kwargs.get('args', None)
	Clock.schedule_once(self._created_view)

    def _created_view(self, *args):
        self.ready = True

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            if not hasattr(touch, "button"):
                return super(WMPanelHeader, self).on_touch_down(touch)
            if touch.button == "middle" and self.can_remove:
                self.master.remove_header(self.text)
                return True
            if touch.button in ("middle", "right"):
                return False
        return super(WMPanelHeader, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        self._say('Panel: pressed at {pos}'.format(pos=pos))

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)

from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_string("""
<WMSeparator>
    size_hint_y: None
    thickness: 2
    margin: 2
    height: self.thickness + 2 * self.margin
    color: [47 / 255., 167 / 255., 212 / 255., 1.]
    canvas:
        Color:
            rgb: self.color
        Rectangle:
            pos: self.x + self.margin, self.y + self.margin + 1
            size: self.width - 2 * self.margin , self.thickness
""")

class WMSeparator(Widget):
    pass

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty

Builder.load_string("""
<WMConfirmPopup>:
    auto_dismiss: True
    title: 'Confirm'
    size_hint: (None, None)
    size: (300, 200)
    label_text: label_text
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: 0.60
            Label:
                id: label_text
        WMSeparator:
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.4
            Widget:
                size_hint_x: None
                width: 100
            Button:
                text: 'Cancel'
                size_hint_y: None
                height: 50
                on_release: root.cancel()
            Button:
                text: 'Confirm'
                size_hint_y: None
                height: 50
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


from kivy.uix.checkbox import CheckBox

Builder.load_string('''
<WMRedCheckBox@Checkbox>:
    canvas.before:
        Color:
            rgb: 1,0,0
        Rectangle:
            pos:self.center_x-8, self.center_y-8
            size:[16,16]
        Color:
            rgb: 0,0,0
        Rectangle:
            pos:self.center_x-7, self.center_y-7
            size:[14,14]
''')

class WMRedCheckBox(CheckBox):
    pass
