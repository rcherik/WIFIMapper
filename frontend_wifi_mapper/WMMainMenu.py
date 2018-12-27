# encoding: utf-8

""" System """

from __future__ import print_function
import time
import os
import sys

""" Kivy """

from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ObjectProperty

""" Our stuff """

from PcapThread import PcapThread

import WMConfig
from WMUtilityClasses import WMInterfacesPopup
from WMFileChooser import LoadDialog, SaveDialog


Builder.load_file(os.path.join('Static', 'wmmainmenu.kv'))

class WMMainMenu(Popup):

    layout = ObjectProperty()

    def __init__(self, app, **kwargs):
        self.app = app
        assert_class = self.app.__class__
        assert hasattr(assert_class, 'get_focus'), "Broken"
        assert hasattr(assert_class, 'parse_file'), "Broken"
        assert hasattr(assert_class, 'start_sniffing'), "Broken"

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
        t = self.app.get_channel_thread()
        if not t:
            return
        if t.set_channel(widget.text):
            widget.text = ','.join(str(c) for c in t.channels)
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
            s += "{} {}Mb".format(giga, mega)
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
        s = "Save Capture"
        if thread and thread.n_saved_pkts:
            self.layout.save_button.disabled = False
            self.layout.clear_capture_button.disabled = False
            s = "%s (%d)" % (s, thread.n_saved_pkts)
        else:
            self.layout.save_button.disabled = True
            self.layout.clear_capture_button.disabled = True
        self._set_label(self.layout.save_button, s)

    def _set_channels(self, *args):
        t = self.app.pcap_thread
        if t and t.channel_thread:
            self.layout.channel_input.disabled = False
            self.layout.channel_stat_button.disabled = False
            self.layout.channel_reset_button.disabled = False
            s = ','.join(str(c) for c in t.channel_thread.channels)\
                    if t.channel_thread.channels else ""
            self._set_label(self.layout.channel_input, s)
        else:
            self.layout.channel_input.disabled = True
            self.layout.channel_stat_button.disabled = True
            self.layout.channel_reset_button.disabled = True

    """ Save Load File/Pcap """

    def _remove_input_focus(self, widget, value):
        if not value:
            self.app.get_focus()

    def dismiss_popup(self):
        if self.popup:
            self.popup.dismiss()
            self.popup = None

    def read_file(self):
        if self.popup:
            self.popup.dismiss()
        content = LoadDialog(load=self.load_file,
                path=os.path.join(self.app.path, 'Traces_pcap'),
                cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file",
                            content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def capture_pcap(self):
        t = self.app.pcap_thread
        if not t:
            return
        if not t.start_saving_pkts():
            self._set_save_button(t)
        self._set_capture(t)

    def save_capture(self):
        if self.popup:
            self.popup.dismiss()
        content = SaveDialog(save=self.save_pcap,
                path=os.path.join(self.app.path, 'Traces_pcap'),
                cancel=self.dismiss_popup)
        content.text_input.bind(focus=self._remove_input_focus)
        self.popup = Popup(title="Save file",
                            content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    assert hasattr(PcapThread, 'reset_saved_pkts'), "Broken"

    def clear_capture(self):
        if self.app.pcap_thread:
            self.app.pcap_thread.reset_saved_pkts()
            self._set_save_button(self.app.pcap_thread)

    def load_file(self, path, filename):
        self.app.parse_file(os.path.join(path, filename[0]))
        self.dismiss_popup()
        self.app.get_focus()

    assert hasattr(PcapThread, 'write_pcap'), "Broken"

    def save_pcap(self, path, filename):
        if self.app.pcap_thread:
            final_filename = os.path.join(path, filename)
            if not final_filename.endswith('.pcap'):
                final_filename += ".pcap"
            self.app.pcap_thread.write_pcap(final_filename)
            self.app.pcap_thread.reset_saved_pkts()
            self._set_save_button(self.app.pcap_thread)
        self.dismiss_popup()
        self.app.get_focus()

    """ Set buttons """

    def reset_channels(self):
        t = self.app.get_channel_thread()
        if t:
            t.reset_channels()
            self._set_channels()

    def open_settings(self):
        self.app.open_settings()

    assert hasattr(PcapThread, 'dump_data'), "Broken"

    def dump_wm_data_to_file(self, path, filename):
        if self.app.pcap_thread:
            final_filename = os.path.join(path, filename)
            if not final_filename.endswith(WMConfig.conf.wm_extension):
                final_filename += WMConfig.conf.wm_extension
            self.app.pcap_thread.dump_data(final_filename)
        self.dismiss_popup()
        self.app.get_focus()

    def dump_wm_data(self):
        if self.popup:
            self.popup.dismiss()
        content = SaveDialog(save=self.dump_wm_data_to_file,
                path=os.path.join(self.app.path, 'Traces_pcap'),
                cancel=self.dismiss_popup)
        content.text_input.bind(focus=self._remove_input_focus)
        self.popup = Popup(title="Dump Wifi Mapper Data",
                            content=content,
                            size_hint=(0.9, 0.9))
        self.popup.open()

    def open_channel_stat(self):
        t = self.app.pcap_thread
        if t:
            print("Channels Stats:")
            for i, stat in enumerate(t.pkt_stats):
                if i > 0 and i % 3 == 0:
                    print()
                print("\t{}: {}\t\t".format(i, stat), end="")
            print()

    def _channel_interfaces_popup_dismissed(self, widget):
        t = self.app.get_channel_thread()
        if t and widget.confirmed() and widget.selected:
            t.set_interface(widget.selected[0])
        self.popup = None

    def set_channel_interface(self):
        t = self.app.get_channel_thread()
        to_down = []
        if t:
            to_down.append(t.iface)
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
