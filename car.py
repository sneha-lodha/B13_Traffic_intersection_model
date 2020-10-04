import random

from mesa import *

class Car(Agent):

	def __init__(self, id, model, direction):
		super().__init__(id, model)     # required by mesa
		self.type = 'car'
		self.color = self.randomColor() # every car is a random color
		self.direction = direction      # direction the car is travelling
		self.distance = 0               # distance the car has travelled
		
	# remove agent from the grid if it  reached the end
	def removeAgent(self):
		self.model.schedule.remove(self)   # remove agent from schedule
		self.model.grid.remove_agent(self) # remove agent from grid

	# check if car can/is allowed to move
	def can_move(self, edge, x):
		light = self.getTrafficLight() # determine relevant traffic light
		if self.pos[x] == edge:        # if agent has reached end of the grid
			self.removeAgent()
			return False                 # car cannot move, as it is gone
		if light.color == 'red' and (self.carAhead() or self.pos[x] == light.pos[x]):
			return False                 # car cannot move forward    
		return True                    # car can move forward
	
	# move agent 1 cell forward and increase travelled distance by one
	def moveForward(self, x, y):
		self.model.grid.move_agent(self, (self.pos[0] + x, self.pos[1] + y))
		self.distance += 1 # increase travelled distance


	# main move loop, determines if and where the car moves
	def move(self):
		if self.direction == 'east':                        # if car is moving east
			if self.can_move(self.model.grid.width - 1, 0):   # if the car can move
				if self.turnAhead():                            # if car has to turn
					if self.distance < self.model.grid.width / 2: 
						self.turn('south', 0, -1)                   # car has to turn right
					else:
					 self.turn('north', 0, 1)                     # car has to turn left
				else:
					self.moveForward(1, 0)                        # the car moves forward
		
		# all the other 3 parts work the same, just with different variables
		elif self.direction == 'west':
			if self.can_move(0, 0):
				if self.turnAhead():
					if self.distance < self.model.grid.width / 2:	
						self.turn('north', 0, 1)
					else:
					 self.turn('south', 0, -1)
				else:
					self.moveForward(-1, 0);
		
		elif self.direction == 'north':
			if self.can_move(self.model.grid.width - 1, 1):
				if self.turnAhead():
					if self.distance < self.model.grid.width / 2:
						self.turn('east', 1, 0)
					else:
					 self.turn('west', -1, 0)
				else:
					self.moveForward(0, 1);
		
		elif self.direction == 'south':
			if self.can_move(0, 1):
				if self.turnAhead():
					if self.distance < self.model.grid.width / 2:
						self.turn('west', -1, 0)
					else:
					 self.turn('east', 1, 0)
				else:
					self.moveForward(0, -1);

	# get the correct traffic light 
	def getTrafficLight(self):
		for light in self.model.traffic_lights: # loop over all lights
			if light.direction == self.direction: # light has to have same direction as car
				if self.direction == 'east' or self.direction == 'west':
					if light.pos[1] == self.pos[1]:   # light has to be in same lane as car
						return light
				if self.direction == 'north' or self.direction == 'south':
					if light.pos[0] == self.pos[0]:   # light has to be in same lane as car
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
			# if next cell is a barrier
			if(agent.type == 'background' and agent.color == 'darkslategrey'):	
				return True            # car has to make a turn
		return False               # car does not have to make a turn

	# check whether there is a car in the cell ahead
	def carAhead(self):
		cellAhead = self.lookAhead()   # get content from cell ahead
		for agent in cellAhead:        # loop over all agents in cell ahead
			if(agent.type == 'car'):     # the agent is a car
				return True                # there is a car ahead
		return False                   # there is no car ahead

	# called every step
	def step(self):
		self.move()
	
	# general turn function
	def turn(self, direction, x, y):
		self.direction = direction    # change direction the car is moving in
		self.moveForward(x,y)         # move one cell forward in new direction

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