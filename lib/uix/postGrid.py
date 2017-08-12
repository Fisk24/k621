from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties     import ObjectProperty
from kivy.properties     import ListProperty
from kivy.properties     import NumericProperty
from kivy.properties     import BoundedNumericProperty

from kivy.clock import Clock

from math import floor, ceil

from lib.uix.thumb import Thumbnail
from lib.core.scrapper import Scrapper

class PostGrid(GridLayout):
	
	thumbNailSize = ListProperty()
	gridMembers   = ListProperty()
	metadata      = ListProperty()
	postCount     = NumericProperty(0)
	scrapper      = ObjectProperty()
	currentPage   = BoundedNumericProperty(1, min=1, max=750, errorvalue=1)
	origin        = ObjectProperty
	
	def __init__(self, **kwargs):
		super(PostGrid, self).__init__(**kwargs)
		
		self.cols = 1
		self.height = 300
		self.postCount = 0
		
		self.scrapper = Scrapper()
		
		Clock.schedule_once(self.populateGrid, 1)
		
	def on_currentPage(self, obj, page):
		self.postCount = 0
		self.clear_widgets()
		self.populateGrid()
		self.origin.ids.gridScroll.scroll_y = 1
		
	def generateMetadata(self):
		postList = self.scrapper.fetchPostsByPage(self.currentPage)
		self.metadata = postList
		
	def populateGrid(self, t=1):
		self.generateMetadata()
		self.addThumbnails(self.metadata, root=self.origin)	
			
	def addThumbnail(self, metadata, root=None):
		tn = Thumbnail(metadata, root)
		self.add_widget(tn)
		self.gridMembers.append(tn)
		self.postCount += 1
		self.calcArangmentValues(None, self.size)
		
	def addThumbnails(self, plist, root=None):
		for i in plist:
			self.addThumbnail(i, root=root)
			
	def clearThumbnails(self):
		self.clear_widgets()
		self.gridMembers = []
		self.postCount = 0
		self.calcArangmentValues(None, self.size)	
			
	def on_size(self, obj, size):
		self.calcArangmentValues(obj, size)
				
	def calcArangmentValues(self, obj, size):
		# First calculate potential spacing
		width   = size[0]
		height  = size[1]
		self.cols       = self.calcPostsPerRow(width, 200)
		self.height     = self.calcHeight()
		self.padding[1] = 16
		self.padding[0] = self.spacing[0]
		self.spacing    = self.calcHorizontalSpacing(width, 200), 16 # spacing is a tuple # find a way to get this 200 from the thumbnail class

	def calcHeight(self):
		# Determine Number of Rows
		rows   = ceil(self.postCount/self.cols)
		height = (275+self.spacing[1])*rows
		return height
	
	def calcPostsPerRow(self, containerWidth, postWidth):
		nPPR = floor(containerWidth/postWidth)
		if nPPR <= 0:
			nPPR = 1
		return nPPR
		
	def calcHorizontalSpacing(self, containerWidth, postWidth):
		#[padding_left, padding_top, padding_right, padding_bottom]
		return floor(((containerWidth-self.padding[0])/self.cols)-postWidth)
		#return (containerWidth*0.01) 