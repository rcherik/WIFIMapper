""" System """
from __future__ import print_function
import sys
import os
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
from APCard import APCard
from StationCard import StationCard
from backend_wifi_mapper.wifi_mapper_utilities import WM_AP, WM_STATION,\
        WM_TRAFFIC, WM_VENDOR, WM_CHANGES
import WMConfig
from WMUtilityClasses import WMPageToggleButton, WMScreen, WMCard

Builder.load_file(os.path.join("Static", "cardlistscreen.kv"))

class CardListScreen(WMScreen):

    scroll_view = ObjectProperty(None)
    main_layout = ObjectProperty(None)
    btn_layout = ObjectProperty(None)

    action_bar = ObjectProperty(None)
    page_layout = ObjectProperty(None)

    def _set_screen_type(self, **kwargs):
        """ Get type of pkt to show and base sorting """
        self.show_ap = kwargs.get('ap', False)
        self.show_station = kwargs.get('station', False)
        self.sort_by = None
        self.sort_by_key = None
        self.sort_values = {}
        self.cmp_reverse = False
        self.ui_paused = False
        if self.show_ap:
            self.toggle_val = 'known'
            self.toggle_check = False
            self.to_search_fields = ['bssid', 'ssid', 'oui']
        elif self.show_station:
            self.toggle_val = 'connected'
            self.toggle_check = False
            self.to_search_fields = ['bssid', 'ap_bssid', 'oui']

    def __init__(self, **kwargs):
        """ Delays view creation because some views are init in kv langage """
        self.args = kwargs.get('args', None)
        self.card_memory = kwargs.get('card_memory', False)
        self._set_screen_type(**kwargs)
        self.wm_screen_type = "AP" if self.show_ap else "Station"
        self.ready = False
        self.card_obj = {}
        self.card_dic = {}
        self.cards = []
        self.loading = False
        self.has_to_sort = False
        self.to_search = None
        """ Important """
        self.browsing_card = False
        """ Pages """
        self.n_card = 0
        self.max_cards = WMConfig.conf.max_card_per_screen
        self.current_page = 1
        self.pages = 0
        super(CardListScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._create_view)

    def _create_view(self, *args):
        """ Create layout when builder has made objects """
        self.stack_layout.bind(
                minimum_height=self.stack_layout.setter('height'))
        self._create_sort_by()
        self.action_bar.sort_dropdown._dropdown.auto_dismiss = False
        self.action_bar.hide_toggle.screen = self
        self.action_bar.actions.action_stop.do_down = self.stop_input
        self.action_bar.actions.action_stop.do_normal = self.resume_input
        self.action_bar.actions.action_pause.do_down = self.set_ui_paused
        self.action_bar.actions.action_pause.do_normal = self.set_ui_unpaused
        self.action_bar.search_input.bind(on_text_validate=self.on_input_enter)
        self.action_bar.search_input.bind(focus=self.on_input_focus)
        self.action_bar.label_curr_page.text = "Page %d" % self.current_page
        self.action_bar.clear_button.bind(on_press=self._clear_input)
        self.action_bar.action_previous.bind(on_press=self.open_main_menu)
        Clock.schedule_once(self._is_ready)

    def open_main_menu(self, widget):
        App.get_running_app().open_main_menu()

    def _is_ready(self, *args):
        """ All is done by now """
        self.ready = True

    def on_input_focus(self, widget, value):
        if not value:
            App.get_running_app().get_focus()

    def on_input_enter(self, value):
        """ Called when pressed enter on input action bar """
        self.to_search = value.text
        App.get_running_app().get_focus()
        self.reload_gui(current=True)

    def _clear_input(self, *args):
        inpt = self.action_bar.search_input
        if inpt.text:
            inpt.text = ""
            self.on_input_enter(inpt)

    def set_sort(self, value):
        """ Handles current sorting value """
        dic = self.sort_values[value]
        self.sort_by_key = value
        self.sort_by = dic['value']
        self.cmp_reverse = dic['cmp']
        self.action_bar.label_curr_sort.text = "Sorting by %s" % value
        self.reload_gui(current=True)

    def _add_sort_value(self, key, value, cmp_reverse):
        """ Adds a sorting button """
        self.sort_values[key] = {
                "value": value,
                "cmp": cmp_reverse
                }
        btn = WMSortActionToggleButton(
                text=key,
                key=key,
                group="ap" if self.show_ap else "station",
                allow_no_selection=False,
                state="down" if key == self.first_sort else "normal",
                screen=self)
        btn.bind(on_press=self.action_bar.sort_dropdown._dropdown.dismiss)
        self.action_bar.sort_dropdown.add_widget(btn)

    def _create_sort_by(self):
        """ Handles sort dropdown text, values and direction """
        self.first_sort = 'clients' if self.show_ap else 'bssid'
        prefix = ""
        if self.card_memory:
            prefix = "ap." if self.show_ap else "station."
        if self.show_ap:
            self._add_sort_value('bssid', prefix + 'bssid', False)
            self._add_sort_value('oui', prefix + 'oui', False)
            self._add_sort_value('signal', prefix + 'rssi', True)
            self._add_sort_value('clients', prefix + 'n_clients', True)
            self._add_sort_value('channels', prefix + 'channel', False)
            self._add_sort_value('sent', 'traffic.sent', True)
            self._add_sort_value('recv', 'traffic.recv', True)
            self._add_sort_value('beacons', prefix + 'beacons', True)
            self._add_sort_value('secu', prefix + 'security', True)
            self._add_sort_value('wps', prefix + 'wps', True)
        if self.show_station:
            self._add_sort_value('bssid', prefix + 'bssid', False)
            self._add_sort_value('ap', prefix + 'ap_bssid', False)
            self._add_sort_value('oui', prefix + 'oui', False)
            self._add_sort_value('signal', prefix + 'rssi', True)
            self._add_sort_value('sent', 'traffic.sent', True)
            self._add_sort_value('recv', 'traffic.recv', True)
            self._add_sort_value('model', prefix + 'model', True)
            self._add_sort_value('probes', prefix + 'ap_probed_str', True)
             
    def _select_page(self):
        """ Goes through every page buttons and change state of actual """
        for children in self.page_layout.children:
            if children.page == self.current_page:
                children.state = "down"
            else:
                children.state = "normal"

    def _make_pages(self):
        """ Handles pagination """
        pages = ((len(self.cards) - 1) / self.max_cards) + 1
        if pages != self.pages:
            from_page = self.pages
            #If new amount of pages is fewer than actual remove all
            if pages < self.pages:
                from_page = 0
                if self.current_page > pages:
                    self.current_page = pages
                self.page_layout.clear_widgets()
            if self.current_page == 0:
                self.current_page = 1
            #Makes pages widget button based on old present buttons
            for i in range(from_page + 1, pages + 1):
                btn = WMPageToggleButton(
                        text="Page %d" % i,
                        group='page',
                        page=i,
                        size_hint=(None, 1),
                        state='down' if self.current_page == i else 'normal',
                        screen=self)
                self.page_layout.add_widget(btn)
            self.pages = pages
        #Actualise label on action bar
        self.action_bar.label_curr_page.text = "Page %d" % self.current_page

    def _should_remove(self, bssid, obj):
        """ Returns True if card does not match input or wanted stuff """
        ret = False
        if getattr(obj, self.toggle_val) == self.toggle_check\
                and self.action_bar.hide_toggle.state == 'down':
            ret = True
        if self.to_search and not ret:
            for field in self.to_search_fields:
                value = attrgetter(field)(obj)
                if isinstance(value, basestring):
                    if value.lower().find(self.to_search.lower()) != -1:
                        return False
            return True
        return ret

    def _sort_cards(self, add=False):
        """
            Sort virtual stack of card
            If virtual stack is not in same order as layout stack
            Clear layout stack and apply new virtual stack
        """
        if not self.has_to_sort or not self.sort_by:
            return
        to_sort = []
        no_sort = []
        for card in self.cards:
            value = attrgetter(self.sort_by)(card)
            if value:
                to_sort.append(card)
            else:
                no_sort.append(card)
        lst = sorted(to_sort,
                key=attrgetter(self.sort_by),
                reverse=self.cmp_reverse)
        lst.extend(no_sort)
        """
        lst = sorted(self.cards,
                key=attrgetter(self.sort_by),
                reverse=self.cmp_reverse)
        """
        if lst != self.cards or add:
            self._clear_cards()
            self.cards = lst
            for card in self.cards[
                    (self.current_page - 1) * self.max_cards
                    :
                    self.current_page * self.max_cards
                    ]:
                self._add_card(card)
            self.has_to_sort = False

    def _remove_card(self, key):
        """ Remove a card of both virtual and layout stack """
        if self.ui_paused:
            return
        card = self.card_dic.get(key, None)
        if card:
            if self.current_screen and card.parent:
                self.stack_layout.remove_widget(card)
                self.n_card = self.n_card - 1 if self.n_card - 1 >= 0 else 0
        if not self.card_memory:
            item = self.card_obj.get(key, None)
        else:
            item = card
        if item in self.cards:
            self.cards.remove(item)
        self.has_to_sort = True

    def _clear_cards(self, full_clear=False):
        """ Remove all virtual and layout stack of cards """
        if self.current_screen:
            self.n_card = 0
            self.stack_layout.clear_widgets()
        self.cards = []
        if full_clear and not self.card_memory:
            self.card_dic = {}
        self.has_to_sort = True

    def _add_card(self, item):
        """ Add a card to stacklayout if user sees screen """
        if self.ui_paused:
            return False
        if self.n_card >= self.max_cards:
            return False
        #No memory has to buid card on the go
        if self.current_screen:
            if not isinstance(item, WMCard):
                if item.bssid in self.card_dic:
                    card = self.card_dic[item.bssid]
                else:
                    card = self._get_card_from_obj(item)
            else:
                card = item
            if card and not card.parent:
                if not self.card_memory:
                    self.card_dic[card.key] = card
                self.stack_layout.add_widget(card)
                self.n_card = self.n_card + 1
                self.has_to_sort = True
        return True

    def _insert_card(self, item):
        """ Add card to virtual stack of card and in stacklayout """
        if isinstance(item, WMCard):
            obj = item.get_obj()
            key = item.key
        else:
            obj = item
            key = item.bssid
        if not self._should_remove(key, obj):
            self.cards.append(item)
            self._add_card(item)

    def _get_card_from_obj(self, obj, retry=True):
        card = None
        try: #################3
            if self.show_ap:
                card = APCard(key=obj.bssid,
                        ap=obj,
                        traffic=obj.traffic,
                        args=self.args)
            else:
                card = StationCard(key=obj.bssid,
                        station=obj,
                        traffic=obj.traffic,
                        args=self.args)
        except AssertionError as e:
            self._say("===========WTF==========")
            self._say(e)
            self._say(obj)
            if card:
                self._say(card)
                card._print_rules()
            self._say("===========WTF==========")
            if retry:
                return self._get_card_from_obj(obj, retry=False)
        return card

    def _set_card(self, bssid, obj):
        """ Fill card with access point info and displays it if it can"""
        if bssid not in self.card_obj:
            self.card_obj[bssid] = obj
        if self.card_memory:
            #Create if not in cards dic
            if bssid not in self.card_dic:
                card = self._get_card_from_obj(obj)
                #Protection against reloading while adding
                while self.browsing_card:
                    pass
                self.card_dic[bssid] = card
                self._insert_card(card)
                return
        #If paused do not update
        if self.ui_paused and self.card_memory:
            return
        #Remove if not wanted or add if wanted
        dic = self.card_dic if self.card_memory else self.card_obj
        if self._should_remove(bssid, obj):
            self._remove_card(bssid)
            return
        elif dic[bssid] not in self.cards:
            self.cards.append(dic[bssid])
            if not self.card_memory:
                self._add_card(obj)
        if self.ui_paused:
            return
        #Update
        card = self.card_dic.get(bssid, None)
        if card:
            obj_name = "ap" if self.show_ap else "station"
            update_dic = {obj_name: obj, "traffic": obj.traffic}
            card.update(**update_dic)

    def update_gui(self, dic, current=True):
        """ Updates GUI - must never stop adding cards while parsing pcap """
        self.current_screen = current

        if self.show_ap:
            ap = dic[WM_AP]
            for key in dic[WM_CHANGES][WM_AP]:
                traffic = dic[WM_TRAFFIC].get(key, None)
                self._set_card(key, ap[key])
                self.has_to_sort = True

        if self.show_station:
            sta = dic[WM_STATION]
            for key in dic[WM_CHANGES][WM_STATION]:
                traffic = dic[WM_TRAFFIC].get(key, None)
                self._set_card(key, sta[key])
                self.has_to_sort = True

        if not self.ui_paused:
            #Pagination
            self._make_pages()
            #Sort cards in stack
            self._sort_cards()
        #Update number of cards in header
        self._update_header()

    def reload_gui(self, current=True):
        """
            Handles full clear and new stack of cards
            Clear all stacks of cards both virtual and layout
            Then browse all cards made
                and decides if it should be added to stacks
            Then handles pagnination, sorting and header update
        """
        if self.loading:
            return
        #self._say("Reloading GUI")
        self.current_screen = current
        self.loading = True
        self._clear_cards(full_clear=True)
        self.browsing_card = True
        if self.card_memory:
            iterator = self.card_dic.iteritems()
        else:
            iterator = self.card_obj.iteritems()
        for key, value in iterator:
            obj = value.get_obj() if self.card_memory else value
            if not self._should_remove(key, obj):
                self.cards.append(value)
        self.browsing_card = False
        if not self.ui_paused:
            self._make_pages()
        #Will add all cards to GUI
        self._sort_cards(add=True)
        if not self.ui_paused\
                or (self.ui_paused and current is False):
            self._update_header()
        self.loading = False

    def get_card(self, key):
        return self.card_dic.get(key, None)

    def get_screen(self, key):
        return self.card_dic.get(key, None)

    def _update_header(self):
        """ Update its header with all cards present on screen """
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
        """
            Handles keyboard input sent by App to screen manager
            Always handle escape here - and spammy input
        """
        if not self.current_screen:
            return False
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
        if keycode[1] == 'escape':
            if self.action_bar.sort_dropdown._dropdown.attach_to is not None:
                self.action_bar.sort_dropdown._dropdown.dismiss()
                return True
            if self.action_bar.search_input.text:
                self._clear_input()
                return True
        return False

    def keyboard_up(self, keyboard, keycode):
        """ Handles keyboard input sent by App to screen manager """
        if not self.current_screen:
            return False
        if keycode[1] == 'f5':
            self.reload_gui()
            return True
        if keycode[1] == 'p':
            self.action_bar.actions.action_pause.state = 'down'\
                    if self.action_bar.actions.action_pause.state == 'normal'\
                    else 'normal'
            return True
        if keycode[1] == 's':
            self.action_bar.actions.action_stop.state = 'down'\
                    if self.action_bar.actions.action_stop.state == 'normal'\
                    else 'normal'
            return True
        if keycode[1] == 'spacebar':
            self.action_bar.hide_toggle.state = 'down'\
                    if self.action_bar.hide_toggle.state == 'normal'\
                    else 'normal'
            return True
        return False

    """ Stop sniffing / pcap read methods """

    def stop_input(self):
        app = App.get_running_app()
        return app.stop_input()

    def resume_input(self):
        app = App.get_running_app()
        return app.resume_input()

    def set_stop(self, val):
        self.action_bar.actions.action_stop.state = 'down'\
                if val is True else 'normal'

    """ Pause ui methods """

    def set_ui_paused(self):
        #self._say("Paused")
        self.ui_paused = True

    def set_ui_unpaused(self):
        #self._say("Unpaused")
        self.ui_paused = False
        self.reload_gui(current=True)

    """ Screen methods """

    def on_pre_enter(self):
        if self.ready:
            self.set_ui_unpaused()

    def on_pre_leave(self):
        if self.ready:
            self.set_ui_paused()
            if self.action_bar.sort_dropdown._dropdown.attach_to is not None:
                self.action_bar.sort_dropdown._dropdown.dismiss()

    def __repr__(self):
        s = "%s: showing " % (self.__class__.__name__)
        s += "ap" if self.show_ap else ""
        s += "station" if self.show_station else ""
        return s

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.actionbar import ActionItem

class ImageButton(ButtonBehavior, Image, ActionItem):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)
        self.source = os.path.join('Static', 'images', 'cross32-3.png')
        self.color = (1, 1, 1, 1)

    def on_press(self):
        self.color = (0, 0, 0, 1)
        pass

    def on_release(self):
        self.color = (1, 1, 1, 1)
        pass

from kivy.uix.label import Label

class WMActionLabel(Label, ActionItem):
    def __init__(self, **kwargs):
        super(WMActionLabel, self).__init__(**kwargs)

from kivy.uix.actionbar import ActionToggleButton

class WMActionToggleButton(ActionToggleButton):

    screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WMActionToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, value):
        if self.screen:
            self.screen.reload_gui(current=True)

from kivy.uix.actionbar import ActionItem
from kivy.uix.textinput import TextInput

class WMActionInput(TextInput, ActionItem):
    def __init__(self, **kwargs):
        super(WMActionInput, self).__init__(**kwargs)

from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation

class WMCardScrollView(ScrollView):

    def __init__(self, **kwargs):
	super(WMCardScrollView, self).__init__(**kwargs)

    def key_scroll_y(self, value, animate=True):
	dsx, dsy = self.convert_distance_to_scroll(0, value)
	sxp = min(1, max(0, self.scroll_x - dsx))
	syp = min(1, max(0, self.scroll_y - dsy))
	if animate:
	    if animate is True:
		animate = {'d': 0.2, 't': 'out_quad'}
	    Animation.stop_all(self, 'scroll_x', 'scroll_y')
	    Animation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
	else:
	    self.scroll_y = syp

    def key_scroll_down(self, animate=True):
	return self.key_scroll_y(60, animate)

    def key_scroll_up(self, animate=True):
	return self.key_scroll_y(-60, animate)

    """
    def on_touch_down(self, touch):
	super(WMCardScrollView, self).on_touch_down(touch)

    def on_touch_up(self, touch):
	super(WMCardScrollView, self).on_touch_up(touch)
    """

    def on_touch_move(self, touch):
	super(WMCardScrollView, self).on_touch_move(touch)

class WMActionScreenToggleButton(ActionToggleButton):

    do_down = ObjectProperty(None)
    do_normal = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(WMActionScreenToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, state):
        if self.do_down and state == 'down':
            self.do_down()
        if self.do_normal and state == 'normal':
            self.do_normal()

class WMSortActionToggleButton(ActionToggleButton):

    def __init__(self, **kwargs):
        self.screen = kwargs.get('screen', None)
        self.key = kwargs.get('key', None)
        self.no_trigger = False
        super(WMSortActionToggleButton, self).__init__(**kwargs)

    def on_state(self, widget, state):
        if self.no_trigger:
            self.no_trigger = False
            return
        if hasattr(self, 'screen') and self.screen:
            if state == 'down':
                self.screen.set_sort(self.key)
