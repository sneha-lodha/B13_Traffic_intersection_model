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
		trafficLights = self.model.traffic_lights

		if self.direction == 'east':
			eastLight = self.getDirectionalLight(trafficLights, 'east')
			if self.pos[0] == self.model.grid.width - 1:
				self.removeAgent()
			else:
				if(eastLight.color == 'red' and self.pos[0] == 4):
					pass
				elif(eastLight.color == 'red' and not self.carAhead()):
					self.model.grid.move_agent(self, (self.pos[0]+1, self.pos[1])) #move in x direction, keep y direction
				elif(eastLight.color == 'green'):
					self.model.grid.move_agent(self, (self.pos[0]+1, self.pos[1]))
		
		if self.direction == 'west':
			westLight = self.getDirectionalLight(trafficLights, 'west')
			if self.pos[0] == 0:
				self.removeAgent()
			else:
				if(westLight.color == 'red' and self.pos[0] == 8):
					pass
				elif(westLight.color == 'red' and not self.carAhead()):
					self.model.grid.move_agent(self, (self.pos[0]-1, self.pos[1])) #move in x direction, keep y direction
				elif(westLight.color == 'green'):
					self.model.grid.move_agent(self, (self.pos[0]-1, self.pos[1]))

		if self.direction == 'south':
			southLight = self.getDirectionalLight(trafficLights, 'south')
			if self.pos[1] == 0:
				self.removeAgent()
			else:
				if(southLight.color == 'red' and self.pos[1] == 8):
					pass
				elif(southLight.color == 'red' and not self.carAhead()):
					self.model.grid.move_agent(self, (self.pos[0], self.pos[1]-1)) #move in x direction, keep y direction
				elif(southLight.color == 'green'):
					self.model.grid.move_agent(self, (self.pos[0], self.pos[1]-1))

		if self.direction == 'north':
			northLight = self.getDirectionalLight(trafficLights, 'north')
			if self.pos[1] == self.model.grid.height - 1:
				self.removeAgent()
			else:
				if(northLight.color == 'red' and self.pos[1] == 4):
					pass
				elif(northLight.color == 'red' and not self.carAhead()):
					self.model.grid.move_agent(self, (self.pos[0], self.pos[1]+1)) #move in x direction, keep y direction
				elif(northLight.color == 'green'):
					self.model.grid.move_agent(self, (self.pos[0], self.pos[1]+1))
	
	# called every step
	def step(self):
		self.move()

	def getDirectionalLight(self, lights, direction):
		for e in lights:
			if e.direction == direction:
				return e

	def carAhead(self):
		if(self.direction == 'east'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0]+1,self.pos[1])))
		elif(self.direction == 'west'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0]-1,self.pos[1])))
		elif(self.direction == 'south'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0],self.pos[1]-1)))
		elif(self.direction == 'north'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0],self.pos[1]+1)))
		for e in cellContents:
			if(e.type == 'car'):
				return True
		return False

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

	def getDirection(self):
		return self.direction