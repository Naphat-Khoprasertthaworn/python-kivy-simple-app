import kivy
from kivy.config import Config
Config.set('graphics', 'resizable', False) # Config.set should be used before importing any other Kivy modules


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import mainthread
from pytube import YouTube
from kivy.uix.button import Button

import threading

Builder.load_file('main.kv')

class MyLayout(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.res = None
        self.yt = None

    def selectRes(self,instance):
        print("Select",instance.text)
        self.res = instance.text

    def findVideo(self):
        url = self.ids.url.text
        try:
            self.yt = YouTube(url)
        except:
            print("link error")
            
        resList = [stream for stream in self.yt.streams.filter(file_extension="mp4",progressive=True)] # progressive=False -> no sound
        for res in resList:
            button = Button(text=res.resolution)
            button.bind(on_press = self.selectRes)
            self.ids.resBox.add_widget( button )


    def downloadThread(self):
        # print("thread working!")
        try:
            # print("start download")
            self.yt.streams.filter(resolution=self.res).first().download()
            self.clearUrl()
        except:
            print("download error")
            return
        print("download success")
        
    def download(self):
        if(self.yt == None):
            print("yt object is None")
            return
        
        if(self.res == None):
            print("res is None")
            return

        t = threading.Thread(target=self.downloadThread)
        t.start()
    
    @mainthread
    def clearUrl(self):
        self.yt = None
        self.res = None
        self.ids.url.text = ""
        
        
        
    

class MyApp(App):
    def build(self):
        Window.size = (700, 800)
        #Window.clearcolor = (1,1,1,1)
        return MyLayout()


if __name__ == "__main__":
    MyApp().run()