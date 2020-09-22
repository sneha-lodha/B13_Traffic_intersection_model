import random

from mesa import *

class Car(Agent):

	def __init__(self, id, model, direction):
		super().__init__(id, model)			# required by mesa
		self.type = 'car'
		self.color = self.randomColor()
		self.direction = direction   		# direction the car is travelling
		self.distance = 0								# distance the car has travelled
		
	# remove agent from the grid if it reached the end
	def removeAgent(self):
		self.model.schedule.remove(self)
		self.model.grid.remove_agent(self)

	# check if car can/is allowed to move
	def can_move(self, edge, x):
		light = self.getTrafficLight()
		if self.pos[x] == edge:
			self.removeAgent()
			return False
		if light.color == 'red' and (self.carAhead() or self.pos[x] == light.pos[x]):
			return False
		return True
	
	# move agent 1 cell forward and increase travelled distance by one
	def moveForward(self, x, y):
		self.model.grid.move_agent(self, (self.pos[0] + x, self.pos[1] + y)) #move in x direction, keep y direction
		self.distance += 1


	# main move loop, determines if and where the car moves
	def move(self):
		if self.direction == 'east':
			if self.can_move(self.model.grid.width - 1, 0):		# if the car can/is allowed to move
				if self.turnAhead():														# if car has to turn
					if self.distance < self.model.grid.width / 2:	# if the car has to turn right of left
						self.turnSouth()														# the car has to turn right
					else:
					 self.turnNorth()															# the  car has to turn left
				else:
					self.moveForward(1, 0);												# the car moves 1 cell forward
		# all the other 3 parts work the same, just with different variables
		elif self.direction == 'west':
			if self.can_move(0, 0):
				if self.turnAhead():
					if self.distance < self.model.grid.width / 2:	
						self.turnNorth()
					else:
					 self.turnSouth()
				else:
					self.moveForward(-1, 0);
		
		elif self.direction == 'north':
			if self.can_move(self.model.grid.width - 1, 1):
				if self.turnAhead():
					if self.distance < self.model.grid.width / 2:
						self.turnEast()
					else:
					 self.turnWest()
				else:
					self.moveForward(0, 1);
		
		elif self.direction == 'south':
			if self.can_move(0, 1):
				if self.turnAhead():
					if self.distance < self.model.grid.width / 2:
						self.turnWest()
					else:
					 self.turnEast()
				else:
					self.moveForward(0, -1);

	# get the correct traffic light 
	def getTrafficLight(self):
		for light in self.model.traffic_lights:
			if light.direction == self.direction:			# light has to be in same direction as car
				if self.direction == 'east' or self.direction == 'west':
					if light.pos[1] == self.pos[1]:				# light has to be in same lane as car
						return light
				if self.direction == 'north' or self.direction == 'south':
					if light.pos[0] == self.pos[0]:				# light has to be in same lane as car
						return light

	# look at the contents of the cell 1 position ahead
	def lookAhead(self):
		if(self.direction == 'east'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0]+1,self.pos[1])))
		elif(self.direction == 'west'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0]-1,self.pos[1])))
		elif(self.direction == 'south'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0],self.pos[1]-1)))
		elif(self.direction == 'north'):
			cellContents = list(self.model.grid.iter_cell_list_contents((self.pos[0],self.pos[1]+1)))
		return cellContents

	# check whether the car has to make a turn
	def turnAhead(self):
		cellAhead = self.lookAhead()
		for agent in cellAhead:
			if(agent.type == 'background' and agent.color == 'darkslategrey'):	# next cell is a barrier
				return True 							# car has to make a turn
		return False

	# check whether there is a car in the cell ahead
	def carAhead(self):
		cellAhead = self.lookAhead()
		for agent in cellAhead:
			if(agent.type == 'car'): 				# next cell contains a car
				return True
		return False

	# called every step
	def step(self):
		self.move()
	
	# turn the car east
	def turnEast(self):
		self.direction = 'east'
		self.moveForward(1, 0)

	# turn the car west
	def turnWest(self):
		self.direction = 'west'
		self.moveForward(-1, 0)

	# turn the car north
	def turnNorth(self):
		self.direction = 'north'
		self.moveForward(0, 1)

	# turn the car south
	def turnSouth(self):
		self.direction = 'south'
		self.moveForward(0, -1)

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