import re, json, sys

import concurrent.futures

from threading import Thread

from kivy.app import App

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.logger import Logger

from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.widget     import Widget
from kivy.uix.label      import Label
from kivy.uix.image      import AsyncImage
from kivy.uix.button     import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput  import TextInput

from kivy.graphics import Line, Rectangle, Color

from kivy.properties import DictProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty

from kivy.clock import Clock
from kivy.base  import Logger

try:
	from lib.core.scrapper import Scrapper
except:
	sys.path.append('/home/fisk/Projects/k621/lib/core/')
	from scrapper import Scrapper
	
class CommentSubmitter(BoxLayout):
	manager = ObjectProperty()

class CommentBodyQuote(Label):
	pass

class CommentBodyLine(Label):
	pass

class CommentBody(BoxLayout):
	text = StringProperty()
	parsed_text = ListProperty()
	
	def on_size(self, *args):
		Clock.schedule_once(self.calcHeight)
	
	def on_text(self, *args):
		self.parseText()
		self.populate()
		Clock.schedule_once(self.calcHeight, 1)	
		
	def calcHeight(self, *args):
		# recalculate the total height of all the labels when the window is resized
		totalHeight = 0
		for widget in self.parsed_text:
			widget._label.refresh()
			totalHeight += widget.texture_size[1]
		#print(self.height, totalHeight)
		self.height = totalHeight
		
	def populate(self):
		for i in self.parsed_text:
			self.add_widget(i)
		self.add_widget(Widget())
			
	def extractQuotes(self, text):
		search = r"\[quote\](.*?)\[/quote\]"
		match = re.findall(search, text, re.DOTALL)
		return match
	
	def cleanQuote(self, quote):
		refParam  = r"(\:.*?\d+)"
		# Exctract Refrence url
		refrences = re.findall(refParam, quote)
		for refrence in refrences:
			clean = quote.replace(refrence, "")
			
		return clean
		
	def parseText(self):
		####### Using lots of labels dosent seem to be working look into kivy's builtin block text widget ############
		
		# Text parser assembled a list of Labels and Widgets to be displayed in the body of a comment
		# Make quotes look as good as posible by removing the user refrence and the tags
		workingText = self.text
		raw_quotes = self.extractQuotes(workingText)
		qList = []
		# cleanQuote(quote)
		try:
			for quote in raw_quotes:
				qList.append(CommentBodyQuote(text=self.cleanQuote(quote)))
				workingText = workingText.replace(quote, "")
		except Exception as e:
			Logger.critical(e)
		
		#workingText = workingText.replace("[quote]", "").replace("[/quote]", "") ## Use this artifact to place a properly formated quote instead of removing it in the future
		# Assemble labels
		try:
			lines = workingText.split('\n')
			qCounter = 0
			for line in lines:
				if "[quote][/quote]" in line:
					self.parsed_text.append(qList[qCounter])
					self.parsed_text.append(CommentBodyLine(text=line.replace("[quote][/quote]", "")))
				else:
					self.parsed_text.append(CommentBodyLine(text=line))
		except Exception as e:
			Logger.critical(e)
				
		self.calcHeight()
			

class Comment(BoxLayout):
	# minmum acceptable is 170
	comment = DictProperty()
	avatar_source = StringProperty()
	avatar_metadata = DictProperty()
	min_height = NumericProperty()
	def __init__(self, **kwargs):
		super(Comment, self).__init__(**kwargs)
		self.size_hint_y = None
		self.min_height = 100
		self.padding = (0, 10)
		# bgColor = 0.1490, 0.3019, 0.6078, 1
		# subBgColor = 0.2, 0.3451, 0.5098, 1
		
	def on_size(self, *args):
		self.calcHeight()
		
	def on_comment(self, *args):
		pass
		# see kv file
		#self.setAvatarThumbnail()
		#self.loadAvatarThumbnail()
	
	def calcHeight(self):
		if self.height < self.min_height:
			self.height = self.min_height
		
	def setAvatarThumbnail(self):
		try:
			self.scrapper = Scrapper()
			avatarMetadata = self.scrapper.fetchUserAvatarById(self.comment['creator_id'])
			#Logger.info(self.avatarMetadata)
			if avatarMetadata:
				Logger.info("Non-None type for meta")
				self.avatar_source = avatarMetadata['preview_url']
				Logger.info("Avatar Loaded...")
			else:
				self.avatar_source = "" # Should return a tranparent filler image
		except Exception as e:
			Logger.critical(sys.exec_info())
		
	def drawBackground(self):
		with self.canvas:
			Color(0.2, 0.3451, 0.5098, 1)
			self.rect   = Rectangle(pos=self.pos, size=self.size)
		self.bind(pos=self.update_rect, size=self.update_rect)
		self.bind(pos=self.update_border, size=self.update_border)
		
	def update_border(self, *args):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(0.2, 0.3451, 0.5098, 1)
			self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 10), width=5.0)
		
	def update_rect(self, *args):
		self.rect.pos  = self.pos
		self.rect.size = self.size
			

class CommentManager(BoxLayout):
	origin = ObjectProperty()
	comments = ListProperty(['...'])
	comment_widgets = ListProperty()
	
	def on_size(self, *args):
		if (self.comments) and (self.comments[0] != 'loading'):
			Clock.schedule_once(self.calcHeight, 0.5)
		
	def on_comments(self, *args):
		Logger.info('fired')
		Logger.info(self.comments)
		try:
			noCommentsLabel = Label(text="No one here but us chickens!")
			loadingLabel    = Label(text="Loading comments...")
			if self.comments == []:
				self.clearCommentWidgets()
				self.add_widget(noCommentsLabel)
			if self.comments == ['loading']:
				self.clearCommentWidgets()
				self.add_widget(loadingLabel)
			if (self.comments != []) and (self.comments != ['loading']):
				self.clearCommentWidgets()
				self.size_hint_y = None
				self.doRenderComments()
		except Exception as e:
			Logger.critical(e)
	
	def doRenderComments(self):
		self.generateCommentWidgets()
		Logger.info(self.comment_widgets)
		self.calcHeight()
		
	def calcHeight(self, *args):
		try:
			totalHeight = 0
			if self.height <= self.origin.height:
				pass
			else:
				for widget in self.comment_widgets:
					totalHeight += widget.height+self.spacing
				
				Logger.info("{}, {}".format(self.height, totalHeight))
				self.height = totalHeight
				return totalHeight
		except AttributeError:
			return 0
		
	def clearCommentWidgets(self):
		self.clear_widgets()
		self.comment_widgets = []
		# Respecify the size_hins and other properties to ready it for the loading label
		
	def generateCommentWidgets(self):
		for comment in self.comments:
			self.addCommentWidget(comment)
		self.add_widget(Widget())
		Logger.info("Generator done")
			
	def addCommentWidget(self, comment):
		try:
			widget = Comment(comment=comment)
			self.comment_widgets.append(widget)
			self.add_widget(widget)
		except Exception as e:
			Logger.info(e)
		

class CommentDevUi(BoxLayout):
	pass

class DecoderTextInput(TextInput):
	target = ObjectProperty()
	
	def on_text(self, *args):
		self.target.comments = json.loads(b'[{"id":3422360,"created_at":"2017-08-16 22:36","post_id":1304728,"creator":"Supernova766","creator_id":145649,"body":"[quote]\\"Minkzx\\":/user/show/141501 said:\\r\\nNot usually into macro/micro, but this pic makes me reconsider that.\\r\\n[/quote]\\r\\nI mean, it\'s evalion. The dude knows howto make a sexy dragon.\\r\\n","score":0},{"id":3422341,"created_at":"2017-08-16 22:29","post_id":1304728,"creator":"Minkzx","creator_id":141501,"body":"Not usually into macro/micro, but this pic makes me reconsider that.","score":4}]')
		self.target.doRenderComments()

class CommentApp(App):
	def build(self):
		Builder.load_file('comments.kv')
		return CommentDevUi()
	
if __name__ == "__main__":
	CommentApp().run()
