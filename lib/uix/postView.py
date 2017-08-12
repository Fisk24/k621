from kivy.uix.screenmanager import Screen
from kivy.uix.image         import AsyncImage
from kivy.uix.carousel      import Carousel
from kivy.uix.button        import Button
from kivy.uix.label         import Label
from kivy.uix.widget        import Widget

from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

from lib.core.scrapper import Scrapper

from threading import Thread

'''
<DevLabel@Label>:
	size_hint_y: None
	text_size: self.size
	height: 17
	markup: True
	halign: 'left'
	valign: 'bottom'
'''

class PostViewScreen(Screen):
	origin   = ObjectProperty()
	metadata = ListProperty()
	target   = NumericProperty()
	scrapper = ObjectProperty()
	comments = ListProperty(['...'])
	
	def on_target(self, widget, n):
		self.assemblePostInfo()
		self.updateMainPostImage(n)
		self.resetComments()
		self.preLoadComments(n)
	
	def on_comments(self, widget, comments):
		self.updateComments(comments)
		
	def resetComments(self):
		self.comments = ['...']
		
	def preLoadComments(self, target):
		thread = Thread(name='Comment Loader', target=self.loadComments, args=[target])
		thread.start()
		self.origin.ids.comments.text = "Loading Comments"
	
	def loadComments(self, target):
		self.scrapper = Scrapper()
		self.comments = self.scrapper.fetchCommentsById(target)
		
	def updateComments(self, comments):
		text = ""
		if (len(comments) > 0) and (comments[0] != '...'):
			for comment in comments:
				text += "{} said: {}\n\n".format(comment['creator'], comment['body'])
				
			self.origin.ids.comments.text = text
		else:
			self.origin.ids.comments.text = "No comments for this post :'C"
		
	def updateMainPostImage(self, target):
		file_url = self.getPostById(self.target)['file_url']
		self.origin.ids.mainPostImage.source = file_url
		
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
			
			
			
			
class SmartCarousel(Carousel):
	origin   = ObjectProperty()
	metadata = ListProperty()
	target   = NumericProperty()
	
	def on_metadata(self, obj, data):
		self.populate(obj, data)
		print(self.slides)
		
	def on_index(self, obj, n):
		pass
	
	def on_target(self, obl, n):
		self.gotoSlideById(n)
		
	def populate(self, obj, data):
		for i in self.metadata:
			obj.add_widget(AsyncImage(source=i['file_url'], allow_stretch=True))
			
	def gotoSlideById(self, id):
		# Itterate through metadata, and if the itteration finds the requested id; navigate to the INDEX of that metadata item.
		for post in self.metadata:
			if post['id'] == id:
				self.index = self.metadata.index(post)+1
	