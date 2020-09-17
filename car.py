import random

from mesa import *

class Car(Agent):

	def __init__(self, id, model, direction):
		super().__init__(id, model)			# required by mesa
		self.type = 'car'
		self.color = self.randomColor()
		self.direction = direction
		
	def removeAgent(self):
		self.model.schedule.remove(self)
		self.model.grid.remove_agent(self)

	# car moves by one grid forward per step
	def move(self):
			if self.direction == 'east':
				if self.pos[0] == self.model.grid.width - 1:
					self.removeAgent()
				else:
					self.model.grid.move_agent(self, (self.pos[0]+1, self.pos[1])) #move in x direction, keep y direction
			if self.direction == 'west':
				if self.pos[0] == 0:
					self.removeAgent()
				else:
					self.model.grid.move_agent(self, (self.pos[0]-1, self.pos[1])) #move in x direction, keep y direction
			if self.direction == 'south':
				if self.pos[1] == 0:
					self.removeAgent()
				else:
					self.model.grid.move_agent(self, (self.pos[0], self.pos[1]-1)) #move in x direction, keep y direction
			if self.direction == 'north':
				if self.pos[1] == self.model.grid.height - 1:
					self.removeAgent()
				else:
					self.model.grid.move_agent(self, (self.pos[0], self.pos[1]+1)) #move in x direction, keep y direction

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