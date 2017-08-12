#! /usr/bin/python3

from kivy.app    import App
from kivy.lang   import Builder
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '1011')

from kivy.core.window import Window

from kivy.clock import Clock

from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.floatlayout   import FloatLayout
from kivy.uix.widget        import Widget
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import Screen

from kivy.properties import ObjectProperty

from lib.uix.thumb             import Thumbnail
from lib.uix.postGrid          import PostGrid
from lib.uix.screencoordinator import ScreenCoordinator
from lib.uix.postView          import PostViewScreen

# Window size should be 800x1011
Window.clearcolor = (0.1059, 0.1059, 0.2667, 1)
Window.minimum_width = 530
Window.minimum_height = 530

class PostSelectionScreen(Screen):
	pass

class K621Ui(FloatLayout):
	pass

class K621App(App):
	def __init__(self, **kwargs):
		super(K621App, self).__init__(**kwargs)
		
	def build(self):
		return K621Ui()
	
if __name__ == "__main__":
	K621App().run()