from mesa import *
from mesa.space import *
from mesa.time import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from car import *
from background import *
from trafficlight import *


class Grid(Model):
	
	def __init__(self):
		self.grid = MultiGrid(11, 11, False) # grid can contain multiple agents per square
		self.schedule = BaseScheduler(self)  # steps are in order of addition to grid
		self.size = 11
		self.running = True
		self.id = 0													 # to make sure all agents have individual id's

		# create background
		for i in range(0, self.size):
			for j in range(0, self.size):
				if (i==5 or j ==5): # if center row/column of grid, it a road
					self.grid.place_agent(Background(self.id, self, 'grey'), (i, j))
				else: # if not center row/column, its grass
					self.grid.place_agent(Background(self.id, self, 'green'), (i, j))
				self.id+=1
		light = Traffic_light(self.id, self)
		self.grid.place_agent(light, (4,4))
		self.schedule.add(light)    					# add car to schedule
		self.id+=1

  
	def step(self):
		car = Car(self.id, self)						# create new car
		self.id+=1
		self.grid.place_agent(car, (-1, 5))	# add car to left side of grid
		self.schedule.add(car)    					# add car to schedule
		self.schedule.step()
