import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image


Builder.load_file('main.kv')

class MyLayout(Widget):
    pass



class MyApp(App):
    def build(self):
        Window.clearcolor = (1,1,1,1)
        return MyLayout()


if __name__ == "__main__":
    MyApp().run()