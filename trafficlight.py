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
		self.on = False
		self.count = 0
		self.on_time = 0
		self.flow = flow
		self.round = False

	def step(self):
		self.timer2()

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

	def timer2(self):
		if self.count < 6:
			self.count += 1
		else: 
			self.on_time = self.decide_on_time(self.flow)
			
			if self.time == self.on_time:
				if self.round == True:
					self.round = False
				else:
					self.round = True
				self.time = 0

			self.model.choose_light(self, self.time)
			if self.on == True:
				self.setColor('green')
			elif self.on == False:
				self.setColor('red')
			self.time += 1


	def decide_on_time(self, flow):
		if flow < 50:
			time = 10
		else:
			time = 15
		return time

	def setColor(self, color):
		self.color = color

	def getOnTime(self):
		return self.on_time

	def getColor(self):
		return self.color

	def getType(self):
		return self.type

	def getDirection(self):
		return self.direction

	def turnOn(self):
		self.on = True
	
	def turnOff(self):
		self.on = False
