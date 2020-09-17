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
		self.grid = MultiGrid(13, 13, False) # grid can contain multiple agents per square
		self.schedule = BaseScheduler(self)  # steps are in order of addition to grid
		self.size = 13
		self.running = True
		self.id = 0													 # to make sure all agents have individual id's

		# create background
		for i in range(0, self.size):
			for j in range(0, self.size):
				if (i==5 or j ==5 or i==7 or j == 7): # if center row/column of grid, it a road
					self.grid.place_agent(Background(self.id, self, 'grey'), (i, j))
				else:
					if (i == 6 or j == 6):
						self.grid.place_agent(Background(self.id, self, 'darkslategrey'), (i, j))
					else: # if not center row/column, its grass
				 		self.grid.place_agent(Background(self.id, self, 'green'), (i, j))
				self.id+=1
		
		self.add_traffic_light(5, 5, 'east', 'red')
		self.add_traffic_light(7, 7, 'west', 'red')
		self.add_traffic_light(7, 5, 'north', 'blue')
		self.add_traffic_light(5, 7, 'south', 'blue')

	def add_traffic_light(self, x, y, direction, color):
		traffic_light = Traffic_light(self.id, self, direction, color)
		self.grid.place_agent(traffic_light, (x, y))
		self.schedule.add(traffic_light)    					# add traffic light to schedule
		self.id+=1

	def addCar(self, direction, x, y):
			if (len(list(self.grid.iter_cell_list_contents((x,y)))) < 2):
				car = Car(self.id, self, direction)						# create new car
				self.grid.place_agent(car, (x, y))	# add car to left side of grid
				self.schedule.add(car)    					# add car to schedule
				self.id += 1


	def step(self):
		# if (len(list(self.grid.iter_cell_list_contents((0,5)))) < 2):
		self.schedule.step()
		self.addCar('east', 0, 5)
		self.addCar('west', 12, 7)
		self.addCar('north', 7, 0)
		self.addCar('south', 5, 12)
			# car = Car(self.id, self, 'north')						# create new car
			# self.id+=1
			# self.grid.place_agent(car, (5, 0	))	# add car to left side of grid
			# self.schedule.add(car)    					# add car to schedule
			# car = Car(self.id, self, 'east')						# create new car
			# self.id+=1
			# self.grid.place_agent(car, (0, 5))	# add car to left side of grid
			# self.schedule.add(car)    					# add car to schedule
			# car = Car(self.id, self, 'north')						# create new car
			# self.id+=1
			# self.grid.place_agent(car, (5, 0	))	# add car to left side of grid
			# self.schedule.add(car)    					# add car to schedule
