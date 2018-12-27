#encoding: utf-8

from __future__ import print_function
import os
import time
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
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES
from WMUtilityClasses import WMRedCheckBox, WMPressableLabel, WMSelectableLabel, WMScreen
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

class StationCardInfoScreen(WMScreen):

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

    def __init__(self, station=None, traffic=None, **kwargs):
        self.station = station
        self.traffic = traffic
        self.ready = False
        self.last_idx_hist = 0
        self.ui_paused = False
        self.graph_canvas = None
        self.graph_btn_create = None
        self.graph_btn_cancel = None
        self.graph_btn_update = None
        self.attacking = False
	super(StationCardInfoScreen, self).__init__(**kwargs)
        self.name = self.station.bssid
        self.screen_type = "Sta"
	Clock.schedule_once(self._create_view)

    @classmethod
    def from_obj(cls, obj):
        return cls(station=obj, traffic=obj.traffic)

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
        self.attack_box.disco_button.bind(on_press=self.disconnect_station)
        self.attack_box.taxonomy_button.bind(on_press=self.get_taxonomy)
        self.attack_box.channel_button.bind(on_press=self.stick_on_channel)
        self.update_gui(None, current=True)

    def update_gui(self, dic, current=True):
        self.current_screen = current
        if not current\
            or not self.ready\
            or self.ui_paused:
            return
        if dic and (self.station.bssid not in dic[WM_CHANGES][WM_STATION]):
            return
        self._set_info_box()
        self._set_data_box()
        self._set_probes()
        self._set_model()
        self._set_history()
       
    def reload_gui(self, current=True):
        self.update_gui(None, current)

    """ Setter for labels """

    def _set_label(self, label, string, copy=""):
        if string is None:
            string = ""
        try:
            uni = unicode(string)
        except UnicodeDecodeError as e:
            self._say(e)
            self._say(self.station)
            self._say(string)
            return
        if isinstance(label, WMSelectableLabel):
            if label.check_select_label_text(string):
                label.set_select_label_text(string)
            label.set_copy(copy)
        elif label and string != label.text:
            label.text = string

    def _set_info_box(self):
        s = self.station.bssid
        if self.station.oui:
            s += " (%s)" % self.station.oui
        self._set_label(self.info_box.bssid, s, copy=self.station.bssid)
        ap_bssid = self.station.ap_bssid
        s = "AP: %s" % (self.station.get_ap_name(ap_bssid))\
                if ap_bssid else "not connected"
        if self.station.channel:
            s += " (%s)" % self.station.channel
        self._set_label(self.info_box.ap_bssid, s, copy=self.station.ap_bssid)

    def _set_data_box(self):
        sent = "sent: %d" % (self.traffic.sent if self.traffic else 0)
        rcv = "rcv: %d" % (self.traffic.recv if self.traffic else 0)
        signal = "sig: %d" % (self.station.rssi if self.station.rssi else 0)
        self._set_label(self.data_box.sent, sent)
        self._set_label(self.data_box.rcv, rcv)
        self._set_label(self.data_box.signal, signal)

    def _set_probes(self):
        s = ""
        probes = self.station.get_ap_probed()
        if probes:
            s = "[i]probed: %s[/i]" % (probes)
        self._set_label(self.probes, s, copy=probes)

    def _set_model(self):
        s = ""
        model = self.station.model
        if model != None:
            s = "model: "
            s += "[b][i]%s[/i][/b]" % (model if model != False else "not found")
        self._set_label(self.model, s, copy=model)

    def _open_ap(self, widget):
        App.get_running_app().open_screen("AP", widget.key)

    def _add_history_traffic(self, string, bssid):
        string = "{} (s:{send:d}, r:{recv:d})".format(
                    string,
                    send=self.traffic.get_sent_all(bssid),
                    recv=self.traffic.get_recv_all(bssid),
                )
        return string

    def _set_history(self):
        size = len(self.station.connected_history)
        if size != self.last_idx_hist:
            self.station_hist_lst.box.clear_widgets()
        else:
            return
        #tuple is (time, name, status, bssid)
        for tupl in self.station.connected_history:
            s = "{time:s} - {name:s}".format(time=tupl[0], name=tupl[1])
            connected = True if tupl[2] == 'connected' else False
            if not connected:
                color = "#FF0000"
                s = self._add_history_traffic(s, tupl[3])
            else:
                color = "#00FF00"
            s = "[color=%s]%s[/color]" % (color, s)
            label = WMPressableLabel(text=s,
                    markup=True, key=tupl[3])
            label.bind(on_press=self._open_ap)
            self.station_hist_lst.box.add_widget(label)
        self.last_idx_hist = size

    """ Graph """

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
        ax.set_xticks(np.arange(0, keys[-1] + 1, step=1))
        ax.set_xticklabels(np.arange(0, (len(keys) + 1) * step, step=step))
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

    """ Attack """

    def disconnect_station(self, widget):
        app = App.get_running_app()
        if self.station.channel and self.station.ap_bssid:
            self._say("Deauth from AP %s to Station %s"
                    % (self.station.ap_bssid, self.station.bssid))
            packets = self.station.get_deauth()
            for packet in packets:
                print(packet.summary())
            app.send_packet(packets)
            print()

    def get_taxonomy(self, widget):
        self.attack_box.taxonomy_button.disabled = True
        app = App.get_running_app()
        channel_hang_time = float(app.config.get("Attack", "ChannelWaitTime"))
        if self.station.channel and self.station.ap_bssid:
            self._say("Deauth from AP %s to Station %s"
                    % (self.station.ap_bssid, self.station.bssid))
            packets = self.station.get_deauth()
            for packet in packets:
                print(packet.summary())
            app.stay_on_channel(self.station.channel, stay=channel_hang_time)
            app.send_packet(packets)
            print()
            time.sleep(channel_hang_time)
        self.attack_box.taxonomy_button.disabled = False

    def stick_on_channel(self, widget):
        app = App.get_running_app()
        app.stay_on_channel(self.station.channel)

    """ Overrides WMScreen """

    def get_name(self):
        return self.station.get_name()

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

Builder.load_file(os.path.join("Static", "stationcardinfoscreen.kv"))
