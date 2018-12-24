from __future__ import print_function
import copy
import re
""" Kivy """
from kivy.uix.tabbedpanel import TabbedPanelHeader, TabbedPanel
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
import WMConfig

Builder.load_string("""
<WMTabbedPanel>:
	tab_width: 170
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
        self.previous_header = None
        self._init_tabs()
        super(WMTabbedPanel, self).__init__(**kwargs)
        for key, value in self.header_dic.iteritems():
            self.add_widget(value)
        self.header_dic["AP"] = self.default_tab

    def change_header(self, key, txt):
        if key in self.header_dic:
            self.header_dic[key].text = txt

    def add_header(self, text, key, screen, *args, **kwargs):
        if key not in self.header_dic:
            self.manager.add_widget(screen)
            header = WMPanelHeader(text=text,
                    master=self,
                    screen=key,
                    content=self.manager,
                    **kwargs)
            self.add_widget(header)
            self.header_dic[key] = header
        else:
            self.switch_to(self.header_dic[key])

    def remove_header(self, key):
        header = self.header_dic.pop(key, None)
        if header:
            if header == self.previous_header:
                self.previous_header = None
            if header == self.current_tab:
                if header == self.previous_header:
                    self.previous_header = None
                if self.previous_header:
                    self.switch_to(self.previous_header)
                    self.previous_header = None
                elif not self.go_back():
                    self.go_forth()
            self.manager.remove(header.screen)
            self.remove_widget(header)

    def go_forth(self):
        return self._go_step(-1)

    def go_back(self):
        return self._go_step(1)

    def _go_step(self, direction):
        found = False
        loop = -1 if direction == -1 else 0
        for header in self.tab_list[::direction]:
            if found:
                self.switch_to(header)
                return True
            if header == self.current_tab:
                found = True
        if found:
            self.switch_to(self.tab_list[loop])
        return found

    def go_to(self, number):
        for header in reversed(self.tab_list):
            number -= 1
            if number == 0:
                self.switch_to(header)
                return True
        return False

    def switch_to(self, header):
        # set the Screen manager to load  the appropriate screen
        # linked to the tab head instead of loading content
        if self.manager.screens:
            self.manager.change_screen(header.screen)
        else:
            super(WMTabbedPanel, self).switch_to(header)
        # we have to replace the functionality of the original switch_to
        self.previous_header = self.current_tab
        self.current_tab.state = "normal"
        header.state = 'down'
        self._current_tab = header

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and hasattr(self.args, "debug")\
                and self.args.debug:
            s = "%s: %s" % (self.__class__.__name__, s)
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
            if not hasattr(touch, "button"):
                return super(WMPanelHeader, self).on_touch_down(touch)
            if touch.button == "middle" and self.can_remove:
                self.master.remove_header(self.screen)
                return True
            if touch.button in ("middle", "right"):
                return False
        return super(WMPanelHeader, self).on_touch_down(touch)

    def _say(self, s, **kwargs):
        if hasattr(self, "args") and hasattr(self.args, "debug")\
                and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)

from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_string("""
<WMSeparator>
    size_hint_y: None
    thickness: 2
    margin: 2
    height: self.thickness + 2 * self.margin
    #color: [47 / 255., 167 / 255., 212 / 255., 1.]
    color: [0.4, 0.4, 0.4, 1]
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
            Button:
                text: 'Cancel'
                size_hint: (None, None)
                height: 50
                width: self.texture_size[0] + 32
                on_release: root.cancel()
            Button:
                text: 'Confirm'
                size_hint: (None, None)
                height: 50
                width: self.texture_size[0] + 29
                on_release: root.confirm()
""")

class WMConfirmPopup(Popup):

    label_text = ObjectProperty()

    def __init__(self, text="Smth", **kwargs):
        self.ret = False
        self.text = text
        self.width_mult = WMConfig.conf.label_width_mult
	super(WMConfirmPopup, self).__init__(**kwargs)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args): 
        self.label_text.text = self.text
        l = len(self.text) * self.width_mult
        if self.width < l:
            diff = l - self.width
            self.width = l
            self.x -= diff / 2

    def cancel(self):
        self.ret = False
        self.dismiss()

    def confirm(self):
        self.ret = True
        self.dismiss()

    def confirmed(self):
        return self.ret

import interface_utilities

Builder.load_string("""
<WMInterfacesPopup>:
    auto_dismiss: True
    title: 'Choose interfaces'
    size_hint: (None, None)
    size: (400, 300)
    interfaces_box: interfaces_box
    BoxLayout:
        orientation: 'vertical'
        ScrollView:
            canvas.before:
                Color:
                    rgba: (1, 1, 1, 0.33)
                Rectangle:
                    pos: self.pos
                    size: self.size
            GridLayout:
                id: interfaces_box
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: (10, 20)
                spacing: (0, 5)
        WMSeparator:
        BoxLayout:
            size_hint_y: 0.4
            orientation: 'horizontal'
            Widget:
            Button:
                text: 'Cancel'
                size_hint: (None, None)
                height: 50
                width: self.texture_size[0] + 32
                on_release: root.cancel()
            Button:
                text: 'Confirm'
                size_hint: (None, None)
                height: 50
                width: self.texture_size[0] + 29
                on_release: root.confirm()
""")

class WMInterfacesPopup(Popup):

    interfaces_box = ObjectProperty()

    def __init__(self, group=False, to_down=[], **kwargs):
        self.ret = False
        self.selected = []
        self.to_down = to_down
        self.should_group = group
        self.wireless_lst, self.iface_lst = interface_utilities.list_interfaces()
        self.width_mult = WMConfig.conf.label_width_mult
	super(WMInterfacesPopup, self).__init__(**kwargs)
        self.auto_dismiss = False
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        for iface in self.wireless_lst:
            s = iface
            if interface_utilities.is_interface_monitoring(iface):
                s += " (monitoring)"
            toggle = ToggleButton(text=s,
                    size_hint=(1, None), size=(0, 40))
            if self.should_group:
                toggle.group = 'if'
            if iface in self.to_down:
                toggle.state = 'down'
            toggle.iface = iface
            self.interfaces_box.add_widget(toggle)

    def cancel(self):
        self.ret = False
        self.dismiss()

    def confirm(self):
        self.ret = True
        self.selected = []
        for child in self.interfaces_box.children:
            if child.state == 'down':
                self.selected.append(child.iface)
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
        self.click_color = WMConfig.conf.click_color
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
            if value.find('color') >= 0:
                match = re.search(r'#[0-9a-fA-F]+', value)
                if match:
                    self.text = value.replace(match.group(0), self.click_color)
                    return
            self.text = "[color=%s]%s[/color]"\
                % (self.click_color, value)

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
	if self.disabled or not self.hidden_text:
	    return False
	if not self.collide_point(*touch.pos):
	    return False
	if super(WMSelectableLabel, self).on_touch_down(touch):
	    return True
        if not self.can_copy\
            or (hasattr(touch, "button") and touch.button == 'right'):
            return True
        self.set_clicked(self.text)
        self.add_event()
	touch.grab(self)
	self._touch_count += 1
	if hasattr(touch, "is_double_tap") and touch.is_double_tap:
	    self.dispatch('on_double_tap')
        elif (hasattr(touch, "button") and touch.button == 'middle'):
	    self.dispatch('on_double_tap')
        return True

    def on_double_tap(self, *args):
        if self.hidden_text:
            Clipboard.copy(self.hidden_text)
            toast('Copied', False)
        else:
            toast('No value to copy', False)

from kivy.uix.behaviors import ButtonBehavior

class WMPressableLabel(ButtonBehavior, Label):

    def __init__(self, **kwargs):
        self.key = kwargs.get('key', None)
        super(WMPressableLabel, self).__init__(**kwargs)
        self.markup = True
        self.no_color_text = ""
        self.event_unclick = None
        self.click_color = WMConfig.conf.click_color

    def set_clicked(self, value):
        if not self.no_color_text:
            self.no_color_text = value
            if value.find('color') >= 0:
                match = re.search(r'#[0-9a-fA-F]+', value)
                if match:
                    self.text = value.replace(match.group(0), self.click_color)
                    return
            self.text = "[color=%s]%s[/color]"\
                % (self.click_color, value)

    def set_unclicked(self, *args):
        if self.no_color_text:
            self.text = self.no_color_text
            self.no_color_text = ""

    def add_event(self):
        if self.event_unclick:
            Clock.unschedule(self.event_unclick)
            self.event_unclick = None
        self.event_unclick = Clock.schedule_once(self.set_unclicked, 0.2)

    def on_press(self):
        self.set_clicked(self.text)
        self.add_event()
        pass

from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.image import Image
from kivy.app import App

class WMImageLink(Image):

    card = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WMImageLink, self).__init__(**kwargs)

    def on_touch_up(self, touch):
        if not self.card:
            return
        if self.collide_point(*touch.pos) and hasattr(touch, "button")\
                and touch.button == "left":
            screen = self.card.get_info_screen()
            App.get_running_app().add_header(
                    "%s: %s" % (self.card.type, self.card.get_name()),
                    self.card.key, screen)
            return True
        return super(WMImageLink, self).on_touch_up(touch)

from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty

class WMPageToggleButton(ToggleButton):

    screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.page = kwargs.get('page', None)
        self.screen = kwargs.get('screen', None)
        self.init = False
        super(WMPageToggleButton, self).__init__(**kwargs)
        self.init = True

    def on_state(self, widget, value):
        if not self.init:
            return
        if value == 'down':
            self.screen.current_page = self.page
            self.screen.reload_gui()
