from kivy.app import App
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import threading 
import time
import sys
from scapy.all import *

#Builder.load_file("test.kv")

class Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)  
        self.counter = 0
        self.stop = False

    def callback_stop(self, i):
        return self.stop

    def callback(self, pkt):
        if self.app and self.app.layout:
            self.app.layout.new_pkt(pkt)

    def run(self):
        sniff("wlp59s0", prn=self.callback, stop_filter=self.callback_stop)

    def add_app(self, app):
        self.app = app

class LoginScreen(StackLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.btn_lst = []

    def new_pkt(self, pkt):
        btn = Button(text=pkt[Ether].src, width=15, size_hint=(0.15, 0.15))
        self.btn_lst.append(btn)
        self.add_widget(btn)
	#Clock.schedule_interval(self.update, 1)

    def update(self, *args):	
	btn = Button(text="prout", width=5, size_hint=(0.15, 0.15))
        self.add_widget(btn)

class MyApp(App):

    def __init__(self, thread):
        App.__init__(self)
        self.thread = thread
        self.layout = None

    def build(self):
        self.layout = LoginScreen()
        return self.layout

if __name__ == '__main__':
    thread = Thread()
    app = MyApp(thread)
    thread.add_app(app)
    thread.start()
    app.run()
    thread.stop = True
    thread.join()
