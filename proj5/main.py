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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar

import shutil
import os

import threading

Builder.load_file('main.kv')

class MyLayout(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.res = None
        self.yt = None
        self.resList = None
        self.mapDownloadingProgress = {}

    def selectRes(self,instance):
        print("Select",instance.text)
        self.res = instance.text

    def findVideo(self):
        t = threading.Thread(target=self.findVideoThread)
        t.start()
        return

    def findVideoThread(self):
        url = self.ids.url.text
        try:
            self.yt = YouTube(url)
            self.resList = [stream for stream in self.yt.streams.filter(progressive=True)] # progressive=False -> no sound
            self.addResButton()
        except:
            self.clearResButton()
            print("link error")
            
    def progressFunction(self,stream, chunk, bytes_remaining): #PyTube Download Progress
        size = stream.filesize
        progress = int((float(abs(bytes_remaining-size)/size))*float(100))
        self.addDownloadProgress( stream,progress )
        print(progress)

    @mainthread
    def clearResButton(self):
        self.ids.resBox.clear_widgets()

    @mainthread
    def addResButton(self):
        if(self.resList == None):
            print("resList is None")
            return
        for res in self.resList:
            button = Button(text=res.resolution)
            button.bind(on_press = self.selectRes)
            self.ids.resBox.add_widget( button )


    def downloadThread(self):
        # self.yt.register_on_progress_callback(self.progressFunction)
        # directoryPath = f"{ os.environ['HOME'] }/Downloads"
        # self.yt.streams.filter(resolution=self.res).first().download(output_path=directoryPath)
        #self.clearUrl()
        try:
            self.yt.register_on_progress_callback(self.progressFunction)
            directoryPath = f"{ os.environ['HOME'] }/Downloads" #download to every OS Downloads folder
            self.yt.streams.filter(resolution=self.res).first().download(output_path=directoryPath)
            pass
        except:
            print("download error")
            self.popUpError("download error")
            return
        self.clearUrl()
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
        self.resList = None
        self.ids.url.text = ""
        self.clearResButton()

    @mainthread
    def popUpError(self,text):
        popup = Popup(
            title='Error!',
            content=Label(text=text),
            size_hint=(None, None), size=(400, 400),
        )
        popup.open()
    
    @mainthread
    def addDownloadProgress(self,stream,progress):
        if stream not in self.mapDownloadingProgress:
            self.mapDownloadingProgress[stream] = ProgressBar(max=100)
            self.ids.downloadingBox.add_widget( self.mapDownloadingProgress[stream] )
        
        self.mapDownloadingProgress[stream].value = progress

        if progress == 100:
            self.ids.downloadingBox.remove_widget( self.mapDownloadingProgress[stream] )
            del self.mapDownloadingProgress[stream]
        return

class MyApp(App):
    def build(self):
        Window.size = (700, 800)
        return MyLayout()


if __name__ == "__main__":
    MyApp().run()