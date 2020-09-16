import random

from mesa import *


#Background blocks used in the grid
class Background(Agent):

	def __init__(self, id, model, color):
		super().__init__(id, model)		# required, part of mesa
		self.type = 'background'	
		self.color = color

	def getColor(self):
		return self.color

	def getType(self):
		return self.type
