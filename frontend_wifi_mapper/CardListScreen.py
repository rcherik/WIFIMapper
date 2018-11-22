""" System """
from __future__ import print_function
import sys
sys.path.append('../')
from operator import itemgetter, attrgetter, methodcaller
""" Kivy """
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
""" Our stuff """
from Card import Card
from APCard import APCard
from backend_wifi_mapper.wifi_mapper import WM_AP, WM_STATION, WM_TRAFFIC
from PcapThread import WM_VENDOR

Builder.load_file("Static/cardlistscreen.kv")

def _compare_gt_sort(val1, val2):
    return val1 > val2

def _compare_lt_sort(val1, val2):
    return val1 < val2

class CardListScreen(Screen):

    scroll_view = ObjectProperty(None)
    main_layout = ObjectProperty(None)
    btn_layout = ObjectProperty(None)
    some_static_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Delays view creation because some views are init in kv langage """
	super(CardListScreen, self).__init__(**kwargs)
        self.ready = False
	self.card_dic = {}
        self.args = kwargs.get('args', None)
        self.show_ap = kwargs.get('ap', False)
	self.show_station = kwargs.get('station', False)
        self.cards = []
        self.has_to_sort = False
        self.monitor_change = ["essid"]
        if self.show_ap:
            self.sort_by = 'ap.known'
            self.cmp_reverse = True
        elif self.show_station:
            self.sort_by = 'connected'
            self.cmp_reverse = True

        """ Python background color """
	with self.canvas.before:
	    Color(0, 0, 0, 0)
	    self.rect = Rectangle(size=self.size, pos=self.pos)
	self.bind(size=self._update_rect, pos=self._update_rect)

	Clock.schedule_once(self._create_view)

    def _update_rect(self, instance, value):
        """ Update background color """
	self.rect.pos = instance.pos
	self.rect.size = instance.size

    def _create_view(self, *args):
        """ Create layout """
        self.stack_layout.bind(
                minimum_height=self.stack_layout.setter('height'))
        self.ready = True

    def _set_ap_card(self, mac, ap, traffic, vendor):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = APCard(key=mac,
                    ap=ap,
                    traffic=traffic,
                    vendor=vendor,
                    args=self.args,
                    monitor_fields=self.monitor_change)
            self.card_dic[mac] = card
            self._insert_card(card)
        else:
            if self.card_dic[mac].update(ap=ap,
                    traffic=traffic,
                    vendor=vendor):
                #self._sort_cards()
                #TODO not yet
                pass

    def _set_station_card(self, mac, station, vendor):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = Card(id=mac, station=station, vendor=vendor)
            self.card_dic[mac] = card
            self._insert_card(card)
        else:
            if self.card_dic[mac].update(id=mac,
                    station=station,
                    vendor=vendor):
                #self._sort_cards()
                #TODO not yet
                pass

    def _swap_cards(self, card, new_card, i):
        """ Remove the upper element from stack, insert, and puts back """
        for card in self.cards[i:]:
            self.stack_layout.remove_widget(card)
        self.cards[i:i] = [new_card]
        for card in self.cards[i:]:
            self.stack_layout.add_widget(card)

    def _sort_cards(self):
        """ Sort cards and check if already sorted """
        lst = sorted(self.cards,
                key=attrgetter(self.sort_by),
                reverse=self.cmp_reverse)
        if lst != self.cards:
            self.cards = lst
            self.stack_layout.clear_widgets()
            for card in self.cards:
                self.stack_layout.add_widget(card)

    def _insert_card(self, new_card):
        """ Check where to insert new card in stack """
        i = 0
        cmp_fun = _compare_lt_sort if self.cmp_reverse else _compare_gt_sort
        newval = new_card.get_value(self.sort_by)
        for card in self.cards:
            val = card.get_value(self.sort_by)
            if cmp_fun(val, newval):
                self._swap_cards(card, new_card, i)
                return
            i += 1
        self._swap_cards(None, new_card, i)

    def update_gui(self, dic):
        """ Update GUI """
        if self.show_ap:
            ap = dic[WM_AP]
            for key, value in ap.iteritems():
                vendor = dic[WM_VENDOR].get(key[:8].upper(), "")
                traffic = dic[WM_TRAFFIC].get(key, None)
                self._set_ap_card(key, ap[key], traffic, vendor)
        if self.show_station:
            sta = dic[WM_STATION]
            for key, value in sta.iteritems():
                probes = sta[key].get_probes()
                s = "%s;%s;%s" % (key, probes, key)
                vendor = dic[WM_VENDOR].get(key[:8].upper(), "")
                self._set_station_card(key, sta[key], vendor)
        self._sort_cards()

    def _say(self, s, **kwargs):
        if self.args and self.args.debug:
            s = "%s: " % (self.__class__.__name__) + s
            print(s, **kwargs)
        else:
            print(s, **kwargs)
