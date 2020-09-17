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
		trafficLights = self.identifyTrafficLights()
		eastLight = self.getDirectionalLight(trafficLights, 'east')

		if self.direction == 'east':
			if self.pos[0] == self.model.grid.width - 1:
				self.removeAgent()
			else:
				if(eastLight.color == 'red' and self.pos[0] == 4):
					pass
				elif(eastLight.color == 'red'):
					print("RED")
					if(not self.carAhead(self.pos[0],self.pos[1])):
						self.model.grid.move_agent(self, (self.pos[0]+1, self.pos[1])) #move in x direction, keep y direction
				elif(eastLight.color == 'blue'):
					self.model.grid.move_agent(self, (self.pos[0]+1, self.pos[1]))
		
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

	def getDirectionalLight(self, lights, direction):
		for e in lights:
			if e.direction == direction:
				return e

	def carAhead(self, x, y):
		cellContents = list(self.model.grid.iter_cell_list_contents((x+1,y)))
		print(cellContents)
		for e in cellContents:
			if(e.type == 'car'):
				return True
		return False

	def identifyTrafficLights(self):
		trafficLights = []
		lightCells = list(self.model.grid.iter_cell_list_contents([(5,5),(5,7),(7,5),(7,7)]))
		for e in lightCells:
			if(e.type == 'light'):
				trafficLights.append(e)
		return trafficLights
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