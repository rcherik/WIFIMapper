""" System """

import time
import os
import sys

""" Kivy """

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty

""" Our stuff """

import WMConfig
from WMUtilityClasses import WMInterfacesPopup
from WMFileChooser import LoadDialog, SaveDialog


Builder.load_file(os.path.join('Static', 'wmmainmenu.kv'))

class WMMainMenu(Popup):

    layout = ObjectProperty()

    def __init__(self, app, **kwargs):
        self.app = app
        self.width_mult = WMConfig.conf.label_width_mult
        self.popup = None
        self.event = None
	super(WMMainMenu, self).__init__(**kwargs)
        self.auto_dismiss = False
	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        self._set_channels()
        self.layout.channel_input.bind(focus=self._on_channel_input_focus)
        self.layout.channel_input.bind(
                on_text_validate=self._on_channel_input_validate)
        self.layout.sniff_button.disabled = True if os.geteuid() else False
        self._set_save_button(self.app.pcap_thread)
        self.update()
        self.event = Clock.schedule_interval(self.update, 0.9)

    """ Input """

    def _on_channel_input_focus(self, widget, value):
        if not value:
            self.app.get_focus()

    def _on_channel_input_validate(self, widget):
        self.app.get_focus()
        t = self.app.pcap_thread
        if not t or not t.channel_thread:
            return
        if t.channel_thread.set_channel(widget.text):
            widget.text = ', '.join(str(c) for c in t.channel_thread.channels)
        else:
            self._set_channels()

    """ Set UI """

    def _set_label(self, label, text):
        if not isinstance(text, basestring):
            return
        if label.text != text:
            label.text = text

    def _set_status_label(self, thread):
        s = "Chilling"
        if thread.reading:
            s = "Reading"
        elif thread.sniffing:
            s = "Sniffing"
        elif os.geteuid():
            s = "Cannot sniff (need Root)"
        self._set_label(self.layout.status_label, s)

    def _set_sniffing_interfaces(self, ifaces):
        if ifaces:
            s = ', '.join(ifaces)
            s = "Interfaces: " + s
        else:
            s = "No interface"
        self._set_label(self.layout.sniff_interfaces, s)

    def _set_time(self):
        now = time.time()
        passed = now - self.app.start_time
        hours, remain = divmod(passed, 3600)
        minutes, seconds = divmod(remain, 60)
        s = "Time: "
        if hours:
            s += "{:0>2}:{:0>2}:{:0>2}".format(int(hours),
                    int(minutes), int(seconds))
        else:
            s += "{:0>2}:{:0>2}".format(int(minutes), int(seconds))
        self.layout.time_label.text = s

    def _set_memory(self):
        s = "Mem: "
        giga, remain = divmod(self.app.process.memory_info()[0], 1000000000)
        mega, rest = divmod(remain, 1000000)
        if giga:
            s += "{}G:{}M".format(giga, mega)
        else:
            s += "{}M".format(mega)
        self._set_label(self.layout.memory_label, s)

    def _set_packets(self, n):
        s = "%d packets" % n
        self._set_label(self.layout.packet_label, s)

    def _set_capture(self, thread):
        if not thread.sniffing:
            self.layout.capture_button.disabled = True
            return
        else:
            self.layout.capture_button.disabled = False
        s = ""
        if thread.save_pkts:
            s = "Stop capturing (%d)" % thread.n_saved_pkts
        else:
            s = "Capture packets"
        self._set_label(self.layout.capture_button, s)

    def update(self, *args):
        t = self.app.pcap_thread
        if t:
            self._set_status_label(t)
            self._set_sniffing_interfaces(t.ifaces)
            self._set_packets(t.n_pkts)
            self.layout.channel_button.disabled = False\
                    if t.channel_thread else True
            self._set_capture(t)
        self._set_memory()
        self._set_time()

    def _set_save_button(self, thread):
        s = "Save Pcap"
        if thread and thread.n_saved_pkts:
            self.layout.save_button.disabled = False
            s = "Save Pcap (%d)" % thread.n_saved_pkts
        else:
            self.layout.save_button.disabled = True
        self._set_label(self.layout.save_button, s)

    def _set_channels(self, *args):
        t = self.app.pcap_thread
        if t and t.channel_thread:
            self.layout.channel_input.disabled = False
            self.layout.channel_stat_button.disabled = False
            s = ', '.join(str(c) for c in t.channel_thread.channels)\
                    if t.channel_thread.channels else ""
            self._set_label(self.layout.channel_input, s)
        else:
            self.layout.channel_input.disabled = True
            self.layout.channel_stat_button.disabled = True

    """ Save Load Pcap """

    def save_pcap_input_focus(self, widget, value):
        if not value:
            self.app.get_focus()

    def dismiss_popup(self):
        if self.popup:
            self.popup.dismiss()
            self.popup = None

    def read_pcap(self):
        if self.popup:
            self.popup.dismiss()
        content = LoadDialog(load=self.load,
                path=os.path.join(self.app.path, 'Traces_pcap'),
                cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file",
                            content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def save_pcap(self):
        if self.popup:
            self.popup.dismiss()
        content = SaveDialog(save=self.save,
                path=os.path.join(self.app.path, 'Traces_pcap'),
                cancel=self.dismiss_popup)
        content.text_input.bind(focus=self.save_pcap_input_focus)
        self.popup = Popup(title="Save file",
                            content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def load(self, path, filename):
        self.app.start_reading_pcap(os.path.join(path, filename[0]))
        self.dismiss_popup()
        self.app.get_focus()

    def save(self, path, filename):
        if self.app.pcap_thread:
            self.app.pcap_thread.write_pcap(os.path.join(path, filename))
            self.app.pcap_thread.reset_saved_pkts()
            self._set_save_button(self.app.pcap_thread)
        self.dismiss_popup()
        self.app.get_focus()

    """ Set buttons """

    def open_channel_stat(self):
        t = self.app.pcap_thread
        if t:
            print(t.pkt_stats)

    def capture_pcap(self):
        t = self.app.pcap_thread
        if t:
            if not t.start_saving_pkts():
                self._set_save_button(t)
            self._set_capture(t)

    def _channel_interfaces_popup_dismissed(self, widget):
        t = self.app.pcap_thread
        if t and t.channel_thread and widget.confirmed() and widget.selected:
            t.channel_thread.set_interface(widget.selected[0])
        self.popup = None

    def set_channel_interface(self):
        t = self.app.pcap_thread
        to_down = []
        if t and t.channel_thread:
            to_down.append(t.channel_thread.iface)
        if not self.popup:
            self.popup = WMInterfacesPopup(group=True, to_down=to_down)
            self.popup.bind(on_dismiss=self._channel_interfaces_popup_dismissed)
            self.popup.open()

    def _interfaces_popup_dismissed(self, widget):
        if widget.confirmed():
            self.app.start_sniffing(widget.selected)
            Clock.schedule_once(self._set_channels)
        self.popup = None

    def sniff(self):
        if not self.popup:
            to_down = []
            if self.app.pcap_thread and self.app.pcap_thread.ifaces:
                to_down = self.app.pcap_thread.ifaces
            self.popup = WMInterfacesPopup(to_down=to_down)
            self.popup.bind(on_dismiss=self._interfaces_popup_dismissed)
            self.popup.open()

    def on_dismiss(self):
        Clock.unschedule(self.event)
        if self.popup:
            self.popup.dismiss()

    def confirm(self):
        self.dismiss()

    def cancel(self):
        self.dismiss()