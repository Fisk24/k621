#! /usr/bin/python3

import sys

from kivy.app    import App
from kivy.lang   import Builder
from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '1011')

from kivy.core.window import Window

from kivy.clock import Clock

from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.floatlayout   import FloatLayout
from kivy.uix.widget        import Widget
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import SlideTransition
from kivy.uix.screenmanager import Screen
from kivy.uix.actionbar     import ActionBar
from kivy.uix.settings      import SettingsWithSidebar

from kivy.properties import ObjectProperty

from lib.uix.thumb             import Thumbnail
from lib.uix.postgrid          import PostGrid
from lib.uix.screencoordinator import ScreenCoordinator
from lib.uix.queueviewscreen   import QueueViewScreen
from lib.uix.postView          import PostView
from lib.uix.comments          import CommentManager

# Window size should be 800x1011
Window.clearcolor = (0, 0, 0.2, 0)
Window.minimum_width = 530
Window.minimum_height = 530

class PostSelectionScreen(Screen):
	'''
		Move me to gridView.py
		Change gridView class name to postSelector or similar
		Fix all references broken by this change
	'''
	pass

class K621ActionBar(ActionBar):
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
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	