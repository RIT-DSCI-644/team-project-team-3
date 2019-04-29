#import kivy
#kivy.require('1.9.0')
import pandas as pd
import numpy as np
import matplotlib as plt
import wx
import dfgui # can install this via pip: https://github.com/bluenote10/PandasDataFrameGUI

from kivy.app import App
from functools import partial
#from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout # use this to position/organize widgets
#from kivy.uix.recycleview.views import RecycleDataViewBehavior
#from kivy.uix.recyclegridlayout import RecycleGridLayout
#from kivy.uix.popup import Popup
#from helper_functions import *

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: "[b]Generate Report[b]"
            markup: True
            font_size: 30 
            size_hint_x: 0.25
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.manager.current = 'report'
        Button:
            text: "[b]View Data[/b]"
            markup: True
            font_size: 30 
            size_hint_x: 0.25
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.manager.current = 'viewData'
        Button:
            text: "[b]View Raw Data[/b]"
            markup: True
            font_size: 30 
            size_hint_x: 0.25
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}     
            #background_color: (155,0,51,53) # comment
            on_press: root.manager.current = 'rawData'
<ReportScreen>:
    BoxLayout:
        Button:
            text: "Generate Report"
        Button:
            text: "main menu"
            on_press: root.manager.current = 'menu'
<ViewDataScreen>:
    BoxLayout:
        Button:
            text: "view data"
        Button:
            text: "main menu"
            on_press: root.manager.current = 'menu'
<RawDataScreen>:
    BoxLayout:
        Button:
            text: "view raw data"
            on_press: root.manager.current = "rawDataFrame"
        Button:
            text: "main menu"
            on_press: root.manager.current = 'menu'
<RawDataFrameScreen>:
    BoxLayout:
        Button:
            text: "raw clinton data"
            on_press: root.clintonRawFrame()
        Button:
            text: "raw trump data"
            on_press: root.trumpRawFrame()
        Button:
            text: "filter congress data"
        Button:
            text: "main menu"
            on_press: root.manager.current = 'menu'

        
""")

# data
clintonRaw = pd.read_csv('clinton_raw.csv')

# Screens
class MenuScreen(Screen):
    pass

class ReportScreen(Screen):
    pass

class ViewDataScreen(Screen):
    pass

class RawDataScreen(Screen):
    pass

class RawDataFrameScreen(Screen):
    
    def clintonRawFrame(self):
        clintonRaw = pd.read_csv('clinton_raw.csv')
        dfgui.show(clintonRaw)
    
    def trumpRawFrame(self):
        trumpRaw = pd.read_csv('trump_raw.csv')
        dfgui.show(trumpRaw)

# Screen Manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ReportScreen(name='report'))
sm.add_widget(ViewDataScreen(name='viewData'))
sm.add_widget(RawDataScreen(name='rawData'))
sm.add_widget(RawDataFrameScreen(name='rawDataFrame'))



class Gui2App(App):

    # disable the button when pressed
    #def disable(self, instance, *args):
    #    instance.disabled = True

    # change the text of  the button when pressed
    #def update(self, instance, *args):
    #    instance.text = "Disabled Button!"

    #def get_data(self):
    #    df = pd.read_excel("clinton_raw.csv")    
    def build(self):
        # mybtn = Button(text="Click me to disable", background_color = (155,0,51,53), pos = (300, 500), size_hint = (.25, .18))
        # mybtn.bind(on_press=partial(self.disable, mybtn))
        # mybtn.bind(on_press=partial(self.update, mybtn))
        #return Label(text = "[color=99ffcc][u][b]this[/b] label[/u][/color] is the [i]best[/i] label [color=f50000][b]known to man[/b][/color]", markup = True, font_size = '30')
        #self.add_widget(ReportButton())
        #self.add_widget(ViewDataButton())
        #self.add_widget(FilterDataButton())
        return sm

if __name__ == '__main__':
    Gui2App().run()
