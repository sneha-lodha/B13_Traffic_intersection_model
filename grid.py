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
		self.running = True
		self.id = 0													 # to make sure all agents have individual id's
		self.traffic_lights = []

		self.add_road('east', 5, 0, self.grid.width)
		self.add_road('east', 7, 0, self.grid.width)
		self.add_road('north', 5, 0, self.grid.height)
		self.add_road('north', 7, 0, self.grid.height)
		
		self.add_barrier('east', 6, 0, self.grid.width)
		self.add_barrier('north', 6, 0, self.grid.height)

		self.finish_background()
		
		self.add_traffic_light(5, 5, 'east', 'red')
		self.add_traffic_light(7, 7, 'west', 'red')
		self.add_traffic_light(7, 5, 'north', 'green')
		self.add_traffic_light(5, 7, 'south', 'green')

	# add a road to the grid
	def add_road(self, direction, position, begin, end=0):
		for i in range(begin, end):
			if direction == 'east':
				if self.grid.is_cell_empty([i,position]):
					self.add_background_agent('grey', i, position)
			if direction == 'north':
				if self.grid.is_cell_empty([position, i]):
					self.add_background_agent('grey', position, i)

	# add a 'barrier' to the grid
	def add_barrier(self, direction, position, begin, end=0):
		for i in range(begin, end):
			if direction == 'east':
				if self.grid.is_cell_empty([i,position]):
					self.add_background_agent('darkslategrey', i, position)
			if direction == 'north':
				if self.grid.is_cell_empty([position, i]):
					self.add_background_agent('darkslategrey', position, i)

	# fill the rest of the grid with a green background
	def finish_background(self):
		for i in range(0, self.grid.width):
			for j in range(0, self.grid.height):
				if self.grid.is_cell_empty([i,j]):
					self.add_background_agent('green', i, j)

	# add background agent to grid
	def add_background_agent(self, color, x, y):
		self.grid.place_agent(Background(self.id, self, color), (x, y))
		self.id += 1

	# add traffic light to the grid and schedule
	# x,y are coordinates of traffic light, direction which way its traffic goes
	def add_traffic_light(self, x, y, direction, color):
		traffic_light = Traffic_light(self.id, self, direction, color)
		self.grid.place_agent(traffic_light, (x, y))
		self.schedule.add(traffic_light)    					
		self.id+=1
		self.traffic_lights.append(traffic_light)

	# add car to the grid and schedule
	def addCar(self, direction, x, y):
		if (bool(random.getrandbits(1))):
			if (len(list(self.grid.iter_cell_list_contents((x,y)))) < 2):
				car = Car(self.id, self, direction)				# create new car
				self.grid.place_agent(car, (x, y))	
				self.schedule.add(car)    				
				self.id += 1


	def step(self):
		self.schedule.step()
		self.addCar('east', 0, 5)
		self.addCar('west', 12, 7)
		self.addCar('north', 7, 0)
		self.addCar('south', 5, 12)
