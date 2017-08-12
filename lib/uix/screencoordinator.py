from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import BoundedNumericProperty

class ScreenCoordinator(ScreenManager):
	metadata = ListProperty()
	new_target = NumericProperty()
	currentPage = BoundedNumericProperty(1, min=1, max=750, errorvalue=1)