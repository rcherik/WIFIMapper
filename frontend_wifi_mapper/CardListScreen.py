""" System """
from __future__ import print_function
import sys
from operator import itemgetter, attrgetter, methodcaller
""" Kivy """
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
""" Our stuff """
from Card import Card
from APCard import APCard
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR
import WMScreen
import WMActionDropDown
import WMActionSpinner
import WMActionLabel
import WMActionToggleButton
import WMSortActionToggleButton
import WMPageToggleButton
import WMCardScrollView
import WMActionPauseToggleButton
import WMActionInput

Builder.load_file("Static/cardlistscreen.kv")

class CardListScreen(WMScreen.WMScreen):

    scroll_view = ObjectProperty(None)
    main_layout = ObjectProperty(None)
    btn_layout = ObjectProperty(None)

    action_bar = ObjectProperty(None)
    action_previous = ObjectProperty(None)
    action_pause = ObjectProperty(None)
    toggle = ObjectProperty(None)
    dropdown_group = ObjectProperty(None)
    page_layout = ObjectProperty(None)

    label_curr_sort = ObjectProperty(None)
    label_curr_page = ObjectProperty(None)

    def _set_screen_type(self, **kwargs):
        """ Get type of pkt to show and base sorting """
        self.show_ap = kwargs.get('ap', False)
        self.show_station = kwargs.get('station', False)
        self.sort_by = None
        self.sort_by_key = None
        self.sort_values = {}
        self.cmp_reverse = False
        if self.show_ap:
            self.toggle_val = 'known'
            self.toggle_check = False
        elif self.show_station:
            self.toggle_val = 'connected'
            self.toggle_check = False

    def __init__(self, **kwargs):
        """ Delays view creation because some views are init in kv langage """
        self.args = kwargs.get('args', None)
        self._set_screen_type(**kwargs)
        super(CardListScreen, self).__init__(**kwargs)
        self.ready = False
        self.card_dic = {}
        self.cards = []
        self.loading = False
        self.has_to_sort = False
        self.current_screen = False
        self.event = None
        self.browsing_card = False
        """ Pages """
        self.n_card = 0
        self.max_cards = 20
        self.current_page = 1
        self.pages = 0
        
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
        self.action_pause.screen = self
        self.toggle.screen = self
        self.label_curr_page.text = "Page %d" % self.current_page
        self._create_sort_by()
        #self.action_previous.on_release = self.pause_input
        self.ready = True

    def _update_rect(self, instance, value):
        """ Update background color """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def pause_input(self):
        app = App.get_running_app()
        return app.pause_input()

    def resume_input(self):
        app = App.get_running_app()
        return app.resume_input()

    def set_sort(self, value):
        dic = self.sort_values[value]
        self.sort_by_key = value
        self.sort_by = dic['value']
        self.cmp_reverse = dic['cmp']
        self.label_curr_sort.text = "Sorting by %s" % value
        self.reload_gui()

    def _add_sort_value(self, key, value, cmp_reverse):
        self.sort_values[key] = {
                "value": value,
                "cmp": cmp_reverse
                }
        btn = WMSortActionToggleButton.WMSortActionToggleButton(
                text=key,
                key=key,
                group="ap" if self.show_ap else "station",
                allow_no_selection=False,
                state="down" if key == 'bssid' else "normal",
                screen=self)
        self.dropdown_group.add_widget(btn)

    def _create_sort_by(self):
        if self.show_ap:
            self._add_sort_value('bssid', 'ap.bssid', False)
            #TODO change sort: separate those with sig and those with not, sort them and
            self._add_sort_value('signal', 'ap.rssi', True)
            self._add_sort_value('crypto', 'ap.security', True)
            self._add_sort_value('sent', 'traffic.sent', True)
            self._add_sort_value('recv', 'traffic.recv', True)
            self._add_sort_value('beacons', 'ap.beacons', True)
            #self._add_sort_value('probe resp', 'ap.proberesp', True)
        if self.show_station:
            #TODO change after card station
            self._add_sort_value('bssid', 'station.bssid', False)
            self._add_sort_value('ap', 'station.ap_bssid', True)
             
    def _select_page(self):
        for children in self.page_layout.children:
            if children.page == self.current_page:
                children.state = "down"
            else:
                children.state = "normal"

    def _make_pages(self):
        pages = ((len(self.cards) - 1) / self.max_cards) + 1
        from_page = self.pages
        if pages == self.pages:
            return
        #self._say(self.pages, pages)
        if pages < self.pages:
            from_page = 0
            if self.current_page > pages:
                self.current_page = pages
            self.page_layout.clear_widgets()
            #self._say("Removing")
        for i in range(from_page + 1, pages + 1):
            #self._say("Adding page %i" % i)
            btn = WMPageToggleButton.WMPageToggleButton(
                    text="Page %d" % i,
                    group='page',
                    page=i,
                    size_hint=(None, 1),
                    state='down' if self.current_page == i else 'normal',
                    screen=self)
            self.page_layout.add_widget(btn)
        self.pages = pages
        self.label_curr_page.text = "Page %d" % self.current_page

    def _remove_card(self, key):
        card = self.card_dic[key]
        if self.current_screen\
                and card in self.stack_layout.children:
            self.stack_layout.remove_widget(card)
        if card in self.cards:
            self.cards.remove(card)
        self.n_card -= 1
        self.has_to_sort = True

    def _clear_cards(self):
        if self.current_screen:
            self.stack_layout.clear_widgets()
        self.cards = []
        self.n_card = 0
        self.has_to_sort = True

    def _add_card(self, card):
        if self.n_card >= self.max_cards:
            return False
        if self.current_screen:
            self.stack_layout.add_widget(card)
        self.n_card += 1
        self.has_to_sort = True
        return True

    def _should_remove(self, mac, obj):
        """ If card is not in sorting, remove """
        ret = False
        if getattr(obj, self.toggle_val) == self.toggle_check\
                and self.toggle.state == 'down':
            ret = True
        return ret

    def _sort_cards(self, add=False):
        """ Sort cards and check if already sorted """
        if not self.has_to_sort or not self.sort_by:
            return
        lst = sorted(self.cards,
                key=attrgetter(self.sort_by),
                reverse=self.cmp_reverse)
        if lst != self.cards or add:
            self._clear_cards()
            self.cards = lst
            for card in self.cards[
                    (self.current_page - 1) * self.max_cards
                    :
                    self.current_page * self.max_cards
                    ]:
                self._add_card(card)

    def _insert_card(self, new_card):
        """ Check where to insert new card in stack """
        if not self._should_remove(new_card.id, new_card.get_obj()):
            self.cards.append(new_card)
            self._add_card(new_card)

    def _set_ap_card(self, mac, ap, traffic):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = APCard(key=mac,
                    ap=ap,
                    traffic=traffic,
                    args=self.args)
            while self.browsing_card:
                pass
            self.card_dic[mac] = card
            self._insert_card(card)
            return
        if self._should_remove(mac, ap):
            self._remove_card(mac)
            return
        elif self.card_dic[mac] not in self.cards:
            self.cards.append(self.card_dic[mac])
        self.card_dic[mac].update(ap=ap, traffic=traffic)

    def _set_station_card(self, mac, station):
        """ Fill card with access point info """
        if mac not in self.card_dic:
            card = Card(key=mac, station=station)
            while self.browsing_card:
                pass
            self.card_dic[mac] = card
            self._insert_card(card)
            return
        if self._should_remove(mac, station):
            self._remove_card(mac)
            return
        elif self.card_dic[mac] not in self.cards:
            self.cards.append(self.card_dic[mac])
        self.card_dic[mac].update(id=mac, station=station)

    def update_gui(self, dic, current=True):
        """ Update GUI """
        self.current_screen = current
        #if self.loading:
            #self.current_screen = False
        self.event = None
        if self.show_ap:
            ap = dic[WM_AP]
            for key, value in ap.iteritems():
                traffic = dic[WM_TRAFFIC].get(key, None)
                if value.new_data:
                    self._set_ap_card(key, value, traffic)
                    self.has_to_sort = True
                value.new_data = False
        if self.show_station:
            sta = dic[WM_STATION]
            for key, value in sta.iteritems():
                if value.new_data:
                    self._set_station_card(key, value)
                    self.has_to_sort = True
                value.new_data = False
        self._make_pages()
        self._sort_cards()
        self._update_header()

    def reload_gui(self, current=True):
        if self.loading:
            return
        self.current_screen = current
        self.loading = True
        self.event = None
        self._say("Reloading GUI")
        self._clear_cards()
        self.browsing_card = True
        for key, value in self.card_dic.iteritems():
            if not self._should_remove(value.key, value.get_obj()):
                self.cards.append(value)
        self.browsing_card = False
        self._make_pages()
        self._sort_cards(add=True)
        self._update_header()
        self.loading = False

    def _update_header(self):
        if self.show_ap:
            key = "AP"
            s = "Access Points"
        else:
            key = "Stations"
            s = "Stations"
        l = len(self.cards)
        if l:
            s += " (%d)" % l
        app = App.get_running_app().change_header(key, s)

    def keyboard_down(self, keyboard, keycode, text, modifiers):
        #self._say(keycode)
        if keycode[1] == 'left':
            if self.current_page > 1:
                self.current_page -= 1
                self._select_page()
            return True
        if keycode[1] == 'right':
            if self.current_page + 1 <= self.pages:
                self.current_page += 1
                self._select_page()
            return True
        if keycode[1] == 'up':
            self.scroll_view.key_scroll_up()
            return True
        if keycode[1] == 'down':
            self.scroll_view.key_scroll_down()
            return True
        if keycode[1] == 'p':
            if self.action_pause.state == 'down':
                self.resume_input()
            else:
                self.pause_input()
            return True
        if keycode[1] == 'spacebar':
            self.toggle.state = 'down'\
                    if self.toggle.state == 'normal' else 'normal'
            return True
        return False

    def set_pause(self, val):
        self.action_pause.state = 'down' if val is True else 'normal'

    def on_pre_enter(self):
        #self._say("pre enter")
        if self.ready:
            self.reload_gui()
        pass

    def __repr__(self):
        s = "%s: showing " % (self.__class__.__name__)
        s += "ap" if self.show_ap else ""
        s += "station" if self.show_station else ""
        return s
