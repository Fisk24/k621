import sys

from kivy.uix.screenmanager import Screen
from kivy.uix.image         import AsyncImage
from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.button        import Button
from kivy.uix.label         import Label
from kivy.uix.widget        import Widget

from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import DictProperty

from kivy.clock import Clock
from kivy.base  import Logger

try:
	from lib.core.scrapper import Scrapper
except:
	sys.path.append('/home/fisk/Projects/k621/lib/core/')
	from scrapper import Scrapper
#from lib.uix.comments import Comment

from multiprocessing.pool import ThreadPool

'''
<DevLabel@Label>:
	size_hint_y: None
	text_size: self.size
	height: 17
	markup: True
	halign: 'left'
	valign: 'bottom'
'''
'''
	PostViewScreen should not be a screen it should be a BoxLayout (or a ScrollView)
	create a new class in a new module for the screen
	rename PostViewScreen to PostViewWidget and fix all accosiations
	the new screen should have access to all the current metadata
	and pass only one post at a time to PostViewWidget
	
	PostViewScreen will control the CommentManager class via the target
	and the main focus of the page which can be an AsyncImage, AsyncVideoPlayer 
	(which i may have to make, nvm VideoPlayer app is capable of streaming so urls can be passed to it)
	and calculate total height for all its children
'''
class PostView(BoxLayout, Screen):
	origin      = ObjectProperty()
	coordinator = ObjectProperty()
	metadata    = DictProperty()
	#target      = NumericProperty()
	scrapper    = ObjectProperty()
	comments    = ListProperty(['loading'])
	
	threadPool = ObjectProperty(ThreadPool(processes=1))
	commentWorker = ObjectProperty()
	
	def on_metadata(self, widget, md):
		#self.assemblePostInfo() # Dev
		self.resetComments()
		Logger.info('PostView: {}'.format(md))
		self.preLoadComments(md['id'])
		self.updateMainPostImage()
	
	def on_comments(self, widget, comments):
		pass
		#self.updateComments(comments)
		
	def resetComments(self):
		self.comments = ['loading']
		
	def preLoadComments(self, target):
		self.commentWorker = self.threadPool.apply_async(self.loadComments, (target,))
		Logger.info("Started loading comments for post: {}".format(self.metadata['id']))
		Clock.schedule_once(self.applyComments, 2)
		
	def applyComments(self, *args):
		self.comments = self.commentWorker.get()
	
	def loadComments(self, target, *args):
		self.scrapper = Scrapper()
		responce = self.scrapper.fetchCommentsById(target)
		return responce
		print("Comments loaded")
		
	def updateComments(self, comments):
		if (len(comments) > 0) and (comments[0] != 'loading'):
			self.ids.comments.comments = comments
		
	def updateMainPostImage(self, *args, **kwargs):
		self.ids.mainPostImage.source = self.metadata['file_url']
		
	def makeLabel(self, text):
		label = Label(text=str(text), size_hint_y=None, halign="left", valign="bottom", markup=True, height=17)
		label.bind(size=label.setter('text_size'))
		return label
		
	def assemblePostInfo(self):
		data = self.getPostById(self.target)
		self.origin.ids.dev_target_info.clear_widgets()
		self.origin.ids.dev_target_info.add_widget(self.makeLabel("[b]Post Info:[/b]"))
		self.origin.ids.dev_target_info.add_widget(self.makeLabel("Targeting: {}".format(self.target)))
		for key in data:
			l = self.makeLabel("{}: {}".format(key, data[key]))
			self.origin.ids.dev_target_info.add_widget(l)
		self.origin.ids.dev_target_info.add_widget(Widget())
		
	def getPostById(self, id):
		# Itterate through metadata, and if the itteration finds the requested id; return that metadata item.
		for post in self.metadata:
			if post['id'] == id:
				return post
			
	
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			