from kivy.base import Logger

from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager

# import names reqired for gesture recognition
from kivy.graphics     import Line
from kivy.gesture      import Gesture
from kivy.gesture      import GestureDatabase
from lib.core.gestures import simplegesture, swipe_left, swipe_right

# properties
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import AliasProperty
from kivy.properties import BooleanProperty

# lib imports
from lib.uix.postView import PostView

class QueueViewManager(ScreenManager):
	origin  = ObjectProperty()
	manager = ObjectProperty()
	#screens = ListProperty([])
	index   = NumericProperty()
	loop    = BooleanProperty(False)
	
	def __init__(self, *args, **kwargs):
		super(QueueViewManager, self).__init__()
		#Initial values
		self.index = 0
		#Create gesture database
		self.gdb = GestureDatabase()
		
		#Add gestures
		self.gdb.add_gesture(swipe_left)
		self.gdb.add_gesture(swipe_right)
		self.gesture_tolerence = 0.70 # minimum score that a gesture must reach before actions can be triggered
	
	def getScreenNameByIndex(self, index):
		return str(self.screens[index].name)
		
	'''
	def getNext(self):
		nextIndex = self.index + 1
		if (self.loop == False):
			# if nextIndex would fall outside the scope of the screens list return None
			if nextIndex > (len(self.screens)-1):
				return None
			# otherwise return the widget associated with nextIndex
			else:
				return self.screens[nextIndex]
		else:
			# if loop is True return the widget no matter what
			if nextIndex > (len(self.screens)-1):
				nextIndex = nextIndex - (len(self.screens)-1)
			return self.screens[nextIndex]
	
	def getPrev(self):
		prevIndex = self.index - 1
		if (self.loop == False) and (prevIndex < 0):
			return None
		else:
			return self.screens[prevIndex]
		
	next    = AliasProperty(getNext, bind=['index'])
	prev    = AliasProperty(getPrev, bind=['index'])
	'''
		
	def isGesture(self, question, gesture):
		if question.get_score(gesture) > self.gesture_tolerence:
			return True
		else:
			return False
			
	def on_touch_down(self, touch):
		# create the 'line' key in the touch object, this data is made available
		# to all other functions that recive this touch object
		touch.ud['line'] = Line(points=(touch.x, touch.y))
		super(QueueViewManager, self).on_touch_down(touch)
		
	def on_touch_move(self, touch):
		# append the newist coordinate data to the point list of the line
		try:
			touch.ud['line'].points += (touch.x, touch.y)
			return True
		except KeyError:
			pass
		super(QueueViewManager, self).on_touch_move(touch)
	
	def on_touch_up(self, touch):
		try:
			g = simplegesture('', list(zip(touch.ud['line'].points[::2], touch.ud['line'].points[1::2])))
			Logger.info('Swipe Left: {}'.format(g.get_score(swipe_left)))
			Logger.info('Swipe Right: {}'.format(g.get_score(swipe_right)))
			if self.isGesture(g, swipe_left):
				Logger.info("Gesture: gesture is a left swipe")
				self.gotoScreenRight()
				# A left swipe should goto the right hand
				# screen, because the act of dragging 
				# somthing to the left exposes the right 
				# hand side of the object and vice versa.
			
			if self.isGesture(g, swipe_right):
				Logger.info("Gesture: gesture is a right swipe")
				self.gotoScreenLeft()
		except KeyError:
			pass
			
		super(QueueViewManager, self).on_touch_up(touch)
		
	def on_index(self, widget, index):
		Logger.info('QueueViewManager: next: {}'.format(self.next))
		Logger.info("QueueViewManager: index: {}".format(index))
		Logger.info('QueueViewManager: prev: {}'.format(self.prev))
		self.current = self.getScreenNameByIndex(index)
		
	def gotoScreenLeft(self):
		# only attempt to change the index if self.screens is not empty
		self.transition.direction = 'right'
		'''
		if self.screens != []:
			self.index -= 1
		'''
		self.current = self.previous()
		
	def gotoScreenRight(self):
		# only attempt to change the index if self.screens is not empty
		self.transition.direction = 'left'
		'''
		if self.screens != []:
			self.index += 1
		'''
		self.current = self.next()
		
	def addPostViewScreen(self, post):
		newName = str(post['id'])
		if not newName in self.screen_names:
			Logger.info("QueueViewManager: I added post {id} by {artist}".format(id=post['id'], artist=post['artist']))
			widget = PostView(origin      = self.origin,
							  coordinator = self.manager,
							  name = newName)
			self.add_widget(widget)
			widget.metadata = post
			Logger.info(widget.name)
			#self.screens.append(widget)
			#widget.bind(origin=self.origin)
		else:
			Logger.info("QueueViewManager: I rejected the duplicate entry")
		
class QueueViewScreen(Screen):
	'''
		QueueViewScreen is, in part, used to display QueueViewManager 
		as a sub element; not the other way around.
	'''
	pass




'''
from QueueViewManager for gesture support
	#def __init__():
		#Create gesture database
		self.gdb = GestureDatabase()
		
		#Add gestures
		self.gdb.add_gesture(swipe_left)
		self.gdb.add_gesture(swipe_right)
		self.gesture_tolerence = 0.75 # minimum score that a gesture must reach before actions can be triggered
		
	def isGesture(self, question, gesture):
		if question.get_score(gesture) > self.gesture_tolerence:
			return True
		else:
			return False
		
	def on_touch_down(self, touch):
		# create the 'line' key in the touch object, this data is made available
		# to all other functions that recive this touch object
		touch.ud['line'] = Line(points=(touch.x, touch.y))
		super(QueueViewManager, self).on_touch_down(touch)
		
	def on_touch_move(self, touch):
		# append the newist coordinate data to the point list of the line
		touch.ud['line'].points += (touch.x, touch.y)
		super(QueueViewManager, self).on_touch_move(touch)
	
	def on_touch_up(self, touch):
		g = simplegesture('', list(zip(touch.ud['line'].points[::2],
									   touch.ud['line'].points[1::2])))
		Logger.info('Swipe Left: {}'.format(g.get_score(swipe_left)))
		Logger.info('Swipe Right: {}'.format(g.get_score(swipe_right)))
		if self.isGesture(g, swipe_left) and (self.previous_slide == None):
			Logger.info("Gesture: gesture is a left swipe")
			self.gotoScreenRight('postSelection')
			
		super(QueueViewManager, self).on_touch_up(touch)
		
	'''