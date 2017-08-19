from kivy.lang.builder import Builder

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget    import Widget
from kivy.uix.image     import AsyncImage
from kivy.uix.behaviors import ButtonBehavior

from kivy.graphics import Rectangle, Color

class Thumbnail(ButtonBehavior, Widget):
	def __init__(self, metadata, root=None, **kwargs):
		super(Thumbnail, self).__init__(**kwargs)
		
		self.root = root
		self.metadata = metadata
		#self.id = "p{id}".format(id=self.metadata['id'])
		
		self.ids.preview.source = self.metadata['preview_url']
		self.ids.score.text = "s"+str(self.metadata['score'])
		self.ids.fav_count.text = "f"+str(self.metadata['fav_count'])
		self.setRating(self.metadata['rating'])
		self.setBgColor()
		
	def on_release(self):
		#self.root.ids.screenCoord.transition.direction = 'left'
		#self.root.ids.screenCoord.current = 'queueView'
		#self.root.ids.screenCoord.new_target = self.metadata['id']
		self.root.ids.queueManager.addPostViewScreen(self.metadata)
		
		
	def setRating(self, rating):
		if rating.upper() == 'S':
			self.ids.rating.text = "[b][color=#0f9b00]S[/color][/b]"
		elif rating.upper() == 'Q':
			self.ids.rating.text = "[b][color=#e9ff00]Q[/color][/b]"
		elif rating.upper() == 'E':
			self.ids.rating.text = "[b][color=#ff3535]E[/color][/b]"
			
	def setBgColor(self):
		with self.canvas.before:
			Color(0.2, 0.3451, 0.5098, 1)  # set the color to light blue
			if self.metadata['has_children'] == True:
				Color(0, 255, 0, 1)  # set the color to green
			if self.metadata['parent_id'] != None:
				Color(93, 255, 0, 1)  # set the color to yellow
			if self.metadata['status'] == 'pending':
				Color(0, 0, 255, 1)  # set the color to blue
			if self.metadata['status'] == 'flagged':
				Color(255, 0, 0, 1)  # set the color to red
				
			self.rect = Rectangle(pos=self.pos, size=self.size)
		self.bind(pos=self.update_rect, size=self.update_rect)
			
	def update_rect(self, *args):
		self.rect.pos = self.pos
		self.rect.size = self.size
	
			