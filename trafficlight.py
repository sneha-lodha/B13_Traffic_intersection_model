import random

from mesa import *

class Traffic_light(Agent):

	def __init__(self, id, model):
		super().__init__(id, model)			# required by mesa
		self.type = 'light'
		self.color = 'red'
		self.time = 0
		

	def setColor(self, color):
		self.color = color

	def getColor(self):
		return self.color

	def getType(self):
		return self.type

	def step(self):
		if self.time == 5:
			self.setColor('blue')
		if self.time == 10: 
			self.setColor('red') 
			self.time = 0
		self.time +=1