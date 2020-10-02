import random

from mesa import *

class Traffic_light(Agent):

	def __init__(self, id, model, flow, direction, turn = 'no turn'):
		super().__init__(id, model)			# required by mesa
		self.type = 'light'
		self.color = 'red'
		self.time = 0										# timer counting when to go green/red
		self.direction = direction 			# direction of the cars passing the light
		self.turn = turn								# whether light 'indicates' a turn
		self.flow = flow

	def step(self):
		times = self.model.calculate_timer()
		print(times)
		self.timer2(times)

# determines how long the light is red vs green.
# ATM they switch per direction, so the variable turn is not yet used
	def timer1(self):
		if self.time == 5:
			if self.direction == 'north':
				self.setColor('red')
		if self.time == 8:
			if self.direction == 'east':
				self.setColor('green')
		if self.time == 13:
			if self.direction == 'east': 
				self.setColor('red') 
		if self.time == 16:
			if self.direction == 'south':
				self.setColor('green')
		if self.time == 21:
			if self.direction == 'south':
				self.setColor('red')
		if self.time == 24:
			if self.direction == 'west':
				self.setColor('green')
		if self.time == 29:
			if self.direction == 'west':
				self.setColor('red')
		if self.time == 32:	
			if self.direction == 'north':
				self.setColor('green')
			self.time = 0
		self.time+=1

	def timer2(self, times):
		print(self.time)
		if self.time == times[0]:
			if self.direction == 'east':
				self.setColor('green')
		if self.time == times[1]:
			if self.direction == 'east':
				self.setColor('red')
		if self.time == times[2]:
			if self.direction == 'west':
				self.setColor('green')	
		if self.time == times[3]:
			if self.direction == 'west':
				self.setColor('red')
		if self.time == times[4]:
			if self.direction == 'north':
				self.setColor('green')	
		if self.time == times[5]:
			if self.direction == 'north':
				self.setColor('red')
		if self.time == times[6]:
			if self.direction == 'south':
				self.setColor('green')
		if self.time == times[7]:
			if self.direction == 'south':
				self.setColor('red')
			self.time = 0
		self.time += 1 

	def setColor(self, color):
		self.color = color

	def getColor(self):
		return self.color

	def getType(self):
		return self.type

	def getDirection(self):
		return self.direction

