from __future__ import print_function
import os
""" Kivy """
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.properties import ObjectProperty, ListProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.stacklayout import StackLayout
from kivy.lang import Builder
from kivy.metrics import sp
from kivy.app import App
""" Our stuff """
import WMScreen
#import CardInfoScreen
import WMScreen
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES
from WMUtilityClasses import WMRedCheckBox, WMPressableLabel, WMSelectableLabel
""" Graph """
import collections
import numpy as np

CAN_USE_GRAPH = False

try:
    from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
    import matplotlib.pyplot as plt
    CAN_USE_GRAPH = True
except:
    pass

""" Important no nesting rule """

class APCardInfoInfoBox(BoxLayout):
    pass

class APCardInfoSecurityBox(BoxLayout):
    pass

class APCardInfoDataBox(BoxLayout):
    pass

class APCardInfoClientConnectedBox(BoxLayout):
    pass

class APCardInfoClientHistoryBox(BoxLayout):
    pass

class APCardInfoAttackBox(BoxLayout):
    pass

class APCardInfoGraphBox(BoxLayout):
    pass

Builder.load_file(os.path.join("Static", "apcardinfoscreen.kv"))

class APCardInfoScreen(WMScreen.WMScreen):

    main_layout = ObjectProperty(None)
    card_layout = ObjectProperty(None)
    station_lst = ObjectProperty(None)
    station_hist_lst = ObjectProperty(None)
    graph = ObjectProperty(None)
    info_box = ObjectProperty(None)
    security_box = ObjectProperty(None)
    data_box = ObjectProperty(None)
    station_box = ObjectProperty(None)
    graph_box = ObjectProperty(None)
    checkbox_all = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.ap = kwargs.get('ap', None)
        self.traffic = kwargs.get('traffic', None)
        self.ready = False
        self.last_n_clients = 0
        self.last_idx_hist = 0
        self.ui_paused = False
        self.graph_btn_create = None
        self.graph_btn_cancel = None
        self.graph_btn_update = None
        self.checkboxed_station = set()
	super(APCardInfoScreen, self).__init__(**kwargs)
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args): 
       	self.ready = True
        self.graph_btn_create = Button(text="Create")
        if not CAN_USE_GRAPH:
            self.graph_btn_create.disabled = True
        self.graph_btn_update = Button(text="Update")
        self.graph_btn_cancel = Button(text="Cancel")
        self.graph_btn_create.bind(on_press=self.graph_callback)
        self.graph_btn_update.bind(on_press=self.graph_callback)
        self.graph_btn_cancel.bind(on_press=self.remove_graph)
        self.checkbox_all.bind(active=self.on_checkbox_all_active)
        self._set_graph_btn()
        self.update_gui(None, current=True)

    def get_plot(self, traffic):
        print('PLOTTING')
        if len(traffic.timeline) < 2:
            return None
        if traffic.timeline[-1] - traffic.timeline[0] >= 7200:
            div = 3600
            time_value = 'hour'
            step = 1
        elif traffic.timeline[-1] - traffic.timeline[0] >= 1200:
            div = 600
            time_value = 'minutes'
            step = 10
        elif traffic.timeline[-1] - traffic.timeline[0] >= 180:
            div = 60
            time_value = 'minutes'
            step = 1
        else:
            div = 10
            time_value = 'seconds'
            step = 10
        d = collections.OrderedDict()
        for elem in traffic.timeline:
            elem = elem / div
            if elem in d:
                d[elem] += 1
            else:
                d[elem] = 1
        keys = []
        start = d.keys()[0]
        for elem in d:
            keys.append(elem - start)
        fig, ax = plt.subplots()
        ax.bar(list(keys), d.values())
        ax.set_ylabel('packets')
        ax.set_xlabel(time_value)
        print(traffic.timeline)
        print(d)
        print(keys)
        print(list(np.arange(0, keys[-1] + 1, step=1)))
        print(list(np.arange(0, (len(keys)) * step, step=step)))
        ax.set_xticks(np.arange(0, keys[-1] + 1, step=1))
        ax.set_xticklabels(np.arange(0, (len(keys) + 1) * step, step=step))
        #ax.set_xticks(list(np.arange(0, keys[-1] + 1, step=1)), np.arange(0, (len(keys)) * step, step=step))
        return fig.canvas

    def _set_graph_btn(self):
        self.graph_box.graph_buttons.clear_widgets()
        if CAN_USE_GRAPH:
            if not self.graph_canvas:
                self.graph_box.graph_buttons.add_widget(self.graph_btn_create)
            else:
                self.graph_box.graph_buttons.add_widget(self.graph_btn_update)
                self.graph_box.graph_buttons.add_widget(self.graph_btn_cancel)
        else:
            self.graph_box.graph_buttons.add_widget(self.graph_btn_create)

    def remove_graph(self, widget):
    	self.graph_box.graph.clear_widgets()
        self.graph_canvas = None
        self._set_graph_btn()

    def graph_callback(self, widget):
    	self.remove_graph(self.graph_canvas)
	self.graph_canvas = self.get_plot(self.traffic)
	if self.graph_canvas is not None:
            self.graph_box.graph.add_widget(self.graph_canvas)
            self._set_graph_btn()

    def reload_gui(self, current=True):
        self.update_gui(None, current)

    def _set_label(self, label, string, copy=""):
        if isinstance(label, WMSelectableLabel):
            if label.check_select_label_text(string):
                self.has_changed = True
                label.set_select_label_text(string)
            label.set_copy(copy)
        elif string != label.text:
            self.has_changed = True
            label.text = string

    def set_info_box(self):
        s = self.ap.bssid
        if self.ap.oui:
            s += " (%s)" % self.ap.oui
        self._set_label(self.info_box.bssid, s, copy=self.ap.bssid)
        s = "ssid: %s" % self.ap.ssid if self.ap.ssid else ""
        if self.ap.channel:
            s += " (%s)" % self.ap.channel
        self._set_label(self.info_box.ssid, s, copy=self.ap.ssid)

    def set_security_box(self):
        self._set_label(self.security_box.co, "co: %d" % self.ap.n_clients)
        self._set_label(self.security_box.security, self.ap.get_security())

    def set_data_box(self):
        sent = "sent: %d" % (self.traffic.sent if self.traffic else 0)
        rcv = "rcv: %d" % (self.traffic.recv if self.traffic else 0)
        beacons = "beacons: %d" % self.ap.beacons
        signal = "sig: %d" % (self.ap.rssi if self.ap.rssi else 0)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.beacons, beacons)
        self._set_label(self.data_box.signal, signal)

    def on_checkbox_all_active(self, widget, active):
        for child in self.station_lst.box.children:
            if isinstance(child, CheckBox):
                child.active = active

    def on_checkbox_active(self, widget, active):
        if active:
            self.checkboxed_station.add(widget.bssid)
        else:
            self.checkboxed_station.remove(widget.bssid)

    def open_station(self, widget):
        App.get_running_app().open_card_link("Station", widget.key)

    def set_connected(self):
        if self.ap.n_clients != self.last_n_clients:
            self.station_lst.box.clear_widgets()
            for bssid in self.ap.client_co:
                """ Ensure label has text=bssid or change open_station """
                label = WMPressableLabel(text=self.ap.get_station_name(bssid),
                        #size_hint=(1, None), size=(0, 20),
                        markup=True, key=bssid)
                label.bind(on_press=self.open_station)
                check = WMRedCheckBox(allow_stretch=True,
                        size_hint=(None, 1),
                        size=(sp(10), 0),
                        color=[1, 0, 0, 1])
                check.bssid = bssid
                if bssid in self.checkboxed_station:
                    check.active = True
                check.bind(active=self.on_checkbox_active)
                self.station_lst.box.add_widget(check)
                self.station_lst.box.add_widget(label)
            self.last_n_clients = self.ap.n_clients

    def set_history(self):
        size = len(self.ap.client_hist_co)
        if size != self.last_idx_hist:
            self.station_hist_lst.box.clear_widgets()
        else:
            return
        #tuple is (time, name, status, bssid)
        for tupl in self.ap.client_hist_co:
            color = "#00FF00" if tupl[2] == 'connected' else "#FF0000"
            label = WMPressableLabel(text="[color=%s]%s - %s[/color]"
                    % (color, tupl[0], tupl[1]),
                    #size_hint=(1, None), size=(0, 20),
                    markup=True, key=tupl[3])
            label.bind(on_press=self.open_station)
            self.station_hist_lst.box.add_widget(label)
        self.last_idx_hist = size

    def update_gui(self, dic, current=True):
        self.current_screen = current
        if not current\
                or not self.ready\
                or self.ui_paused:
            return
        if dic and (self.ap.bssid not in dic[WM_CHANGES][WM_AP]):
            return
        self.set_info_box()
        self.set_security_box()
        self.set_data_box()
        self.set_connected()
        self.set_history()
        
    def set_ui_paused(self):
        self.ui_paused = True

    def set_ui_unpaused(self):
        self.ui_paused = False
        self.reload_gui(current=True)

    def on_pre_enter(self):
        if self.ready:
            self.set_ui_unpaused()

    def on_pre_leave(self):
        if self.ready:
            self.set_ui_paused()

    def keyboard_down(self, keyboard, keycode, text, modifiers):
        """
            Handles keyboard input sent by App to screen manager
            Always handle escape here - and spammy input
        """
        if not self.current_screen:
            return False
        return False

    def keyboard_up(self, keyboard, keycode):
        """ Handles keyboard input sent by App to screen manager """
        if not self.current_screen:
            return False
