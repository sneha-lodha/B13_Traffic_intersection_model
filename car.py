import random

from mesa import *

class Car(Agent):

	def __init__(self, id, model):
		super().__init__(id, model)			# required by mesa
		self.type = 'car'
		self.color = self.randomColor()
		
	# car moves by one grid forward per step
	def move(self):
		self.model.grid.move_agent(self, (self.pos[0]+1, self.pos[1]))

	# called every step
	def step(self):
		self.move()

	# selects random color, to make it easy to see different between cars
	def randomColor(self):
		r = random.randint(0,255)
		g = random.randint(0,255)
		b = random.randint(0,255)
		return '#{:02x}{:02x}{:02x}'.format(r,g,b) # transform to HTML color code

	def getColor(self):
		return self.color

	def getType(self):
		return self.type