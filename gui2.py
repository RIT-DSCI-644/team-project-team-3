import kivy
kivy.require('1.9.0')
import pandas

from kivy.app import App
from functools import partial
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout # use this to position/organize widgets
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.popup import Popup
#from kivy.lang import Builder


class ReportButton(Button):
    pass

class ViewDataButton(Button):
    pass

class FilterDataButton(Button):
    pass   


class Gui2App(BoxLayout, App):

    # disable the button when pressed
    def disable(self, instance, *args):
        instance.disabled = True

    # change the text of  the button when pressed
    def update(self, instance, *args):
        instance.text = "Disabled Button!"

    def get_data(self):
        df = pandas.read_excel("clinton_raw.csv")
        
    def build(self):
        # mybtn = Button(text="Click me to disable", background_color = (155,0,51,53), pos = (300, 500), size_hint = (.25, .18))
        # mybtn.bind(on_press=partial(self.disable, mybtn))
        # mybtn.bind(on_press=partial(self.update, mybtn))
        #return Label(text = "[color=99ffcc][u][b]this[/b] label[/u][/color] is the [i]best[/i] label [color=f50000][b]known to man[/b][/color]", markup = True, font_size = '30')
        self.add_widget(ReportButton())
        self.add_widget(ViewDataButton())
        self.add_widget(FilterDataButton())
        return self


gui2 = Gui2App()

gui2.run()