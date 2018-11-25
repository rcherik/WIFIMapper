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
from kivy.lang import Builder
from kivy.core.window import Window
""" Our stuff """
from Card import Card
from APCard import APCard
from backend_wifi_mapper.wifi_mapper import WM_AP, WM_STATION, WM_TRAFFIC
from PcapThread import WM_VENDOR
import WMScreen
import WMActionDropDown
import WMActionSpinner
import WMActionLabel
import WMActionToggleButton
import WMPageActionToggleButton

Builder.load_file("Static/cardlistscreen.kv")

def _compare_gt_sort(val1, val2):
    return val1 > val2

def _compare_lt_sort(val1, val2):
    return val1 < val2

class CardListScreen(WMScreen.WMScreen):

    scroll_view = ObjectProperty(None)
    main_layout = ObjectProperty(None)
    btn_layout = ObjectProperty(None)

    action_bar = ObjectProperty(None)
    action_previous = ObjectProperty(None)
    toggle = ObjectProperty(None)
    dropdown_group = ObjectProperty(None)
    overflow_group = ObjectProperty(None)

    def __init__(self, **kwargs):
        """ Delays view creation because some views are init in kv langage """
        self.args = kwargs.get('args', None)
        self._set_screen_type(**kwargs)
	super(CardListScreen, self).__init__(**kwargs)
        self.ready = False
	self.card_dic = {}
        self.cards = []
        self.has_to_sort = False
        self.monitor_change = ["essid"]
        self.reloading = False
        self.n_card = 0
        self.max_cards = 40
        self.current_page = 1
        self.pages = 1
        
        """ Python background color """
	with self.canvas.before:
	    Color(0, 0, 0, 0)
	    self.rect = Rectangle(size=self.size, pos=self.pos)
	self.bind(size=self._update_rect, pos=self._update_rect)

	Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        """ Create layout """
        self.stack_layout.bind(
                minimum_height=self.stack_layout.setter('height'))
        self.toggle.screen = self
        self.toggle.group = 'ap' if self.show_ap else 'station'
        self.important.text = "Page %d" % self.current_page
        self.ready = True

    def _set_screen_type(self, **kwargs):
        """ Get type of pkt to show and base sorting """
        self.show_ap = kwargs.get('ap', False)
	self.show_station = kwargs.get('station', False)
        if self.show_ap:
            self.sort_by = 'ap.bssid'
            self.cmp_reverse = False
            self.toggle_val = 'known'
            self.toggle_check = False
        elif self.show_station:
            self.sort_by = 'station.bssid'
            self.cmp_reverse = False
            self.toggle_val = 'connected'
            self.toggle_check = False

    def _update_rect(self, instance, value):
        """ Update background color """
	self.rect.pos = instance.pos
	self.rect.size = instance.size

    def _make_pages(self):
        pages = (len(self.cards) / self.max_cards) + 1
        self.pages = pages
        """
        from_page = self.pages
        if pages == self.pages:
            return
        print(self.pages, pages)
        if pages < self.pages:
            from_page = 0
            self.overflow_group.clear_widgets()
            print("Removing")
        for i in range(from_page + 1, pages + 1):
            print("Adding page %i" % i)
            btn = WMPageActionToggleButton.WMPageActionToggleButton(
                    text="Page %d" % i,
                    group='page',
                    page=i,
                    state='down' if self.current_page == i else 'normal',
                    screen=self)
            if self.current_page == i:
                self.page_btn = btn
            self.overflow_group.add_widget(btn)
        """

    def _remove_card(self, key):
        card = self.card_dic[key]
        self.stack_layout.remove_widget(card)
        if card in self.cards:
            self.cards.remove(card)
        self.n_card -= 1

    def _clear_cards(self):
        self.stack_layout.clear_widgets()
        self.cards = []
        self.n_card = 0

    def _add_card(self, card):
        if self.n_card > self.max_cards:
            return False
        self.stack_layout.add_widget(card)
        self.n_card += 1
        return True

    def _should_remove(self, mac, obj):
        """ If card is not in sorting, remove """
        ret = False
        if getattr(obj, self.toggle_val) == self.toggle_check\
                and self.toggle.state == 'down': 
            ret = True
        return ret

    def _set_ap_card(self, mac, ap, traffic):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            if self._should_remove(mac, ap):
                return
            card = APCard(key=mac,
                    ap=ap,
                    traffic=traffic,
                    args=self.args,
                    monitor_fields=self.monitor_change)
            self.card_dic[mac] = card
            self._insert_card(card)
            return
        if self._should_remove(mac, ap):
            self._remove_card(mac)
            return
        if self.card_dic[mac].update(ap=ap,
                traffic=traffic):
            #self._sort_cards()
            #TODO not yet
            pass

    def _set_station_card(self, mac, station):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            if self._should_remove(mac, station):
                return
            card = Card(key=mac, station=station)
            self.card_dic[mac] = card
            self._insert_card(card)
            return
        if self._should_remove(mac, station):
            self._remove_card(mac)
            return
        if self.card_dic[mac].update(id=mac,
                station=station):
            #self._sort_cards()
            #TODO not yet
            pass

    def _swap_cards(self, old_card, new_card, i):
        """ Remove the upper element from stack, insert, and puts back """
        for card in self.cards[i:]:
            self.stack_layout.remove_widget(card)
        self.cards[i:i] = [new_card]
        for card in self.cards[i:]:
            if not self._add_card(card):
                return

    def _sort_cards(self):
        """ Sort cards and check if already sorted """
        lst = sorted(self.cards,
                key=attrgetter(self.sort_by),
                reverse=self.cmp_reverse)
        if lst != self.cards:
            self._clear_cards()
            self.cards = lst
            for card in self.cards[
                    (self.current_page - 1) * self.max_cards:
                    self.current_page * self.max_cards]:
                if not self._add_card(card):
                    return
        self._make_pages()

    def _insert_card(self, new_card):
        """ Check where to insert new card in stack """
        i = 0
        #cmp_fun = _compare_lt_sort if self.cmp_reverse else _compare_gt_sort
        #newval = new_card.get_value(self.sort_by)
        for card in self.cards[(self.current_page - 1) * self.max_cards:
                    self.current_page * self.max_cards]:
            #val = card.get_value(self.sort_by)
            #if cmp_fun(val, newval):
            #    self._swap_cards(card, new_card, i)
            #    return
            i += 1
        #self._swap_cards(None, new_card, i)
        self.cards.append(new_card)
        self._add_card(new_card)

    def update_gui(self, dic):
        """ Update GUI """
        while self.reloading:
            pass
        if self.show_ap:
            ap = dic[WM_AP]
            for key, value in ap.iteritems():
                #vendor = dic[WM_VENDOR].get(key[:8].upper(), "")
                traffic = dic[WM_TRAFFIC].get(key, None)
                self._set_ap_card(key, ap[key], traffic)
        if self.show_station:
            sta = dic[WM_STATION]
            for key, value in sta.iteritems():
                probes = sta[key].get_probes()
                s = "%s;%s;%s" % (key, probes, key)
                #vendor = dic[WM_VENDOR].get(key[:8].upper(), "")
                self._set_station_card(key, sta[key])
        self._sort_cards()

    def reload_gui(self):
        while self.reloading:
            pass
        self.reloading = True
        self.important.text = "Page %d" % self.current_page
        self._clear_cards()
        for key, value in self.card_dic.iteritems():
            if not self._should_remove(value.key, value.get_obj()):
                self.cards.append(value)
        self._sort_cards()
        self.reloading = False


    def __repr__(self):
        s = "%s: showing " % (self.__class__.__name__)
        s += "ap" if self.show_ap else ""
        s += "station" if self.show_station else ""
        return s
