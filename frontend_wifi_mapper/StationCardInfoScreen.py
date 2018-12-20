from __future__ import print_function
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
""" Our stuff """
import WMScreen
#import CardInfoScreen
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES
from WMUtilityClasses import WMRedCheckBox
import WMSelectableLabel
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

Builder.load_file("Static/stationcardinfoscreen.kv")

class StationCardInfoScreen(WMScreen.WMScreen):

    main_layout = ObjectProperty(None)
    card_layout = ObjectProperty(None)
    station_hist_lst = ObjectProperty(None)
    graph = ObjectProperty(None)
    info_box = ObjectProperty(None)
    data_box = ObjectProperty(None)
    probes = ObjectProperty(None)
    model = ObjectProperty(None)
    station_box = ObjectProperty(None)
    graph_box = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.station = kwargs.get('station', None)
        self.traffic = kwargs.get('traffic', None)
        self.ready = False
        self.last_n_clients = 0
        self.last_idx_hist = 0
        self.ui_paused = False
        self.graph_btn_create = None
        self.graph_btn_cancel = None
        self.graph_btn_update = None
	super(StationCardInfoScreen, self).__init__(**kwargs)
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
        if string is None:
            string = ""
        if isinstance(label, WMSelectableLabel.WMSelectableLabel):
            if label.check_select_label_text(string):
                label.set_select_label_text(string)
            label.set_copy(copy)
        elif label and string != label.text:
            label.text = string

    def set_info_box(self):
        s = self.station.bssid
        if self.station.oui:
            s += " (%s)" % self.station.oui
        self._set_label(self.info_box.bssid, s, copy=self.station.bssid)
        s = self.station.ap_bssid or ""
        if self.station.channel:
            s += " (%s)" % self.station.channel
        self._set_label(self.info_box.ap_bssid, s, copy=self.station.ap_bssid)

    def set_data_box(self):
        sent = "sent: %d" % (self.traffic.sent if self.traffic else 0)
        rcv = "rcv: %d" % (self.traffic.recv if self.traffic else 0)
        signal = "sig: %d" % (self.station.rssi if self.station.rssi else 0)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.signal, signal)

    def set_probes(self):
        s = ""
        probes = self.station.get_ap_probed()
        if probes:
            s = "[i]probed: %s[/i]" % (probes)
        self._set_label(self.probes, s, copy=probes)

    def set_model(self):
        s = ""
        model = self.station.model
        if model != None:
            s = "[b][i]%s[/i][/b]" % (model if model != False else "not found")
        self._set_label(self.model, s, copy=model)

    def set_history(self):
        """
        for tupl in reversed(self.ap.client_hist_co[self.last_idx_hist:]):
            color = "#00FF00" if tupl[2] == 'connected' else "#FF0000"
            #TODO label open station
            l = Label(text="[color=%s]%s - %s[/color]"
                    % (color, tupl[0], tupl[1]),
                    markup=True)
            self.station_hist_lst.box.add_widget(l)
        self.last_idx_hist = len(self.ap.client_hist_co)
        """

    def update_gui(self, dic, current=True):
        self.current_screen = current
        if not current\
                or not self.ready\
                or self.ui_paused:
            return
        if dic and (self.station.bssid not in dic[WM_CHANGES][WM_STATION]):
            return
        self.set_info_box()
        self.set_data_box()
        self.set_probes()
        self.set_model()
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
