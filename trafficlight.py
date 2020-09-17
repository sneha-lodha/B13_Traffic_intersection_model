import random

from mesa import *

class Traffic_light(Agent):

	def __init__(self, id, model, direction, color):
		super().__init__(id, model)			# required by mesa
		self.type = 'light'
		self.color = color
		self.time = 0
		self.direction = direction
		

	def setColor(self, color):
		self.color = color

	def getColor(self):
		return self.color

	def getType(self):
		return self.type

	def getDirection(self):
		return self.direction

	def step(self):
		self.timer()

	def timer(self):
		if self.time == 5:
			if self.direction == 'north' or self.direction == 'south':
				self.setColor('red')
		if self.time == 6:
			if self.direction == 'east' or self.direction == 'west':
				self.setColor('blue')
		if self.time == 11:
			if self.direction == 'east' or self.direction == 'west': 
				self.setColor('red') 
		if self.time == 12:
			if self.direction == 'north' or self.direction == 'south':
				self.setColor('blue')
			self.time = 0
		self.time+=1

