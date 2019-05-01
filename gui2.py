#import kivy
#kivy.require('1.9.0')
import collections
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import wx
import dfgui # can install this via pip: https://github.com/bluenote10/PandasDataFrameGUI

from kivy.app import App
from kivy.core.window import Window
from functools import partial
#from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout # use this to position/organize widgets
#from kivy.uix.recycleview.views import RecycleDataViewBehavior
#from kivy.uix.recyclegridlayout import RecycleGridLayout
#from kivy.uix.popup import Popup
from helper_functions import get_average_sentiment, get_top_retweeted, get_most_conservative, get_most_liberal, get_sentiment_frequency, get_most_positive, get_most_negative

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: "[b]Generate Word Clouds[b]"
            markup: True
            font_size: 30 
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.manager.current = 'report'
        Button:
            text: "[b]View Sentiment Data[/b]"
            markup: True
            font_size: 30 
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.manager.current = 'sentimentData'
        Button:
            text: "[b]View Raw Data[/b]"
            markup: True
            font_size: 30 
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}     
            #background_color: (155,0,51,53) # comment
            on_press: root.manager.current = 'rawData'
<ReportScreen>:
    BoxLayout:
        Button:
            text: "[b]Word Clouds[b]"
            markup: True
            font_size: 20
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_x': .5, 'center_y':.5}
            on_press: root.manager.current = 'wordCloud'
        Button:
            text: "[b]main menu[b]"
            markup: True
            font_size: 15
            size_hint: (.1, .1)
            pos_hint: {'center_x': 0, 'y':0}
            on_press: root.manager.current = 'menu'
<SentimentDataScreen>:
    BoxLayout:
        Button:
            text: "[b]View Sentiment Data[b]"
            markup: True
            font_size: 20
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_x': .5, 'center_y':.5}
            on_press: root.manager.current = "sentimentDataFrame"
        Button:
            text: "[b]main menu[b]"
            markup: True
            font_size: 15
            size_hint: (.1, .1)
            pos_hint: {'center_x': 0, 'y':0}
            on_press: root.manager.current = 'menu'
<RawDataScreen>:
    BoxLayout:
        Button:
            text: "[b]View Raw Data[b]"
            markup: True
            font_size: 20
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_x': .5, 'center_y':.5}
            on_press: root.manager.current = "rawDataFrame"
        Button:
            text: "[b]main menu[b]"
            markup: True
            font_size: 15
            size_hint: (.1, .1)
            pos_hint: {'center_x': 0, 'y':0}
            on_press: root.manager.current = 'menu'
<RawDataFrameScreen>:
    BoxLayout:
        Button:
            text: "[b]Raw Clinton Data[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.clintonRawFrame()
        Button:
            text: "[b]Raw Trump Data[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.trumpRawFrame()
        Button:
            text: "[b]Raw Congress Data[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.congressRawFrame()
        Button:
            text: "[b]main menu[b]"
            markup: True
            font_size: 15
            size_hint: (.1, .1)
            pos_hint: {'center_x': 0, 'y':0}
            on_press: root.manager.current = 'menu'
<SentimentDataFrameScreen>:
    BoxLayout:
        Button:
            text: "[b]Sentiment Clinton Data[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.clintonSentiment()
        Button:
            text: "[b]Sentiment Trump Data[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.trumpSentiment()
        Button:
            text: "[b]Sentiment Congress Data[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.congressSentiment()
        Button:
            text: "[b]main menu[b]"
            markup: True
            font_size: 15
            size_hint: (.1, .1)
            pos_hint: {'center_x': 0, 'y':0}
            on_press: root.manager.current = 'menu'
<WordCloudScreen>:
    BoxLayout:
        Button:
            text: "[b]Clinton Word Cloud[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.clintonCloud()
        Button:
            text: "[b]Trump Word Cloud[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.trumpCloud()
        Button:
            text: "[b]Congress Word Cloud[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.congressCloud()
        Button:
            text: "[b]Clinton Sentiment[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.clintonSentCloud()
        Button:
            text: "[b]Trump Sentiment[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.trumpSentCloud()
        Button:
            text: "[b]Congress Sentiment[b]"
            markup: True
            font_size: 15
            size_hint_x: 0.5
            size_hint_y: 0.25
            pos_hint: {'center_y': 0.5}
            on_press: root.congressSentCloud()
        Button:
            text: "[b]main menu[b]"
            markup: True
            font_size: 15
            size_hint: (.25, .25)
            pos_hint: {'center_x': 0, 'y':0}
            on_press: root.manager.current = 'menu'
        
""")


# functions from helper functions
def grab_text(df):
    cw =[]
    df = df["text"]   #Grab just the fourth column
        
    for x in df.index:    #Iterate over the valid indicies. Need this since congresslib/con are partials. 
        temp=str(df[x])
        temp.strip()                  ##Cleans up the text of junk characters
        temp=temp.replace('.','')  #stripping out common punctuation so words ending with commas and periods don't count as two different words.
        temp=temp.replace(',','')
        temp=temp.replace('“','')
        temp=temp.replace('”','')
        temp=temp.replace('&amp','')
        temp=temp.replace(';','')
        temp=temp.replace('-',' ')
        temp=temp.lower()
        cw.append(temp)
    return cw

stopword = pd.read_csv('stopwords.csv')
stopword = stopword['a']
stopword = set(stopword) # needs to be set for wordcloud

# Screens
class MenuScreen(Screen):
    pass

class ReportScreen(Screen):
    pass

class SentimentDataScreen(Screen):
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

    def congressRawFrame(self):
        congressRaw = pd.read_csv('congress_raw.csv')
        dfgui.show(congressRaw)

class SentimentDataFrameScreen(Screen):

    def clintonSentiment(self):
        clintonSent = pd.read_csv('clinton_sentiment.csv')
        dfgui.show(clintonSent)
    
    def trumpSentiment(self):
        trumpSent = pd.read_csv('trump_sentiment.csv')
        dfgui.show(trumpSent)

    def congressSentiment(self):
        congressSent = pd.read_csv('congress_sentiment.csv')
        dfgui.show(congressSent)

class WordCloudScreen(Screen):
    
    def clintonCloud(self):
        clintonRaw = pd.read_csv('clinton_raw.csv')
        clintonRawText = str(grab_text(clintonRaw))
        wc = WordCloud(max_words=10, stopwords=stopword).generate(clintonRawText)
        default_colors = wc.to_array()
        plt.imshow(wc.recolor(color_func=None, random_state=3), interpolation="bilinear")
        plt.axis("off")
        #plt.figure()
        plt.imshow(default_colors, interpolation="bilinear")
        plt.show()

    def clintonSentCloud(self):
        clintonSent = pd.read_csv('clinton_sentiment.csv')
        clintonSentText = str(grab_text(clintonSent))
        wc = WordCloud(max_words=10, stopwords=stopword).generate(clintonSentText)
        default_colors = wc.to_array()
        plt.imshow(wc.recolor(color_func=None, random_state=3), interpolation="bilinear")
        plt.axis("off")
        #plt.figure()
        plt.imshow(default_colors, interpolation="bilinear")
        plt.show()

    def trumpCloud(self):
        trumpRaw = pd.read_csv('trump_raw.csv')
        trumpRawText = str(grab_text(trumpRaw))
        wc = WordCloud(max_words=10, stopwords=stopword).generate(trumpRawText)
        default_colors = wc.to_array()
        plt.imshow(wc.recolor(color_func=None, random_state=3), interpolation="bilinear")
        plt.axis("off")
        #plt.figure()
        plt.imshow(default_colors, interpolation="bilinear")
        plt.show()

    def trumpSentCloud(self):
        trumpSent = pd.read_csv('trump_sentiment.csv')
        trumpSentText = str(grab_text(trumpSent))
        wc = WordCloud(max_words=10, stopwords=stopword).generate(trumpSentText)
        default_colors = wc.to_array()
        plt.imshow(wc.recolor(color_func=None, random_state=3), interpolation="bilinear")
        plt.axis("off")
        #plt.figure()
        plt.imshow(default_colors, interpolation="bilinear")
        plt.show()

    def congressCloud(self):
        congressRaw = pd.read_csv('congress_raw.csv')
        congressRawText = str(grab_text(congressRaw))
        wc = WordCloud(max_words=10, stopwords=stopword).generate(congressRawText)
        default_colors = wc.to_array()
        plt.imshow(wc.recolor(color_func=None, random_state=3), interpolation="bilinear")
        plt.axis("off")
        #plt.figure()
        plt.imshow(default_colors, interpolation="bilinear")
        plt.show()

    def congressSentCloud(self):
        congressSent = pd.read_csv('congress_raw.csv')
        congressSentText = str(grab_text(congressSent))
        wc = WordCloud(max_words=10, stopwords=stopword).generate(congressSentText)
        default_colors = wc.to_array()
        plt.imshow(wc.recolor(color_func=None, random_state=3), interpolation="bilinear")
        plt.axis("off")
        #plt.figure()
        plt.imshow(default_colors, interpolation="bilinear")
        plt.show()
    

# Screen Manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ReportScreen(name='report'))
sm.add_widget(SentimentDataScreen(name='sentimentData'))
sm.add_widget(RawDataScreen(name='rawData'))
sm.add_widget(RawDataFrameScreen(name='rawDataFrame'))
sm.add_widget(SentimentDataFrameScreen(name='sentimentDataFrame'))
sm.add_widget(WordCloudScreen(name='wordCloud'))


Window.size = (1200, 700)

class Gui2App(App):

    # disable the button when pressed
    #def disable(self, instance, *args):
    #    instance.disabled = True

    # change the text of  the button when pressed
    #def update(self, instance, *args):
    #    instance.text = "Disabled!"

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
