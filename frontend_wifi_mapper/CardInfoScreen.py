from __future__ import print_function
""" Kivy """
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
""" Our stuff """
import WMScreen

class CardInfoScreen(WMScreen.WMScreen):

    scroll_view = ObjectProperty(None)
    main_layout = ObjectProperty(None)
    btn_layout = ObjectProperty(None)
    some_static_button = ObjectProperty(None)

    def __init__(self, **kwargs):
	super(CardInfoScreen, self).__init__(**kwargs)
