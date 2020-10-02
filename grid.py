from mesa import *
from mesa.space import *
from mesa.time import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from car import *
from background import *
from trafficlight import *


class Grid(Model):
	
	def __init__(self, east_flow, west_flow, north_flow, south_flow):
		self.grid = MultiGrid(25, 25, False)	# grid can contain multiple agents per square
		self.schedule = BaseScheduler(self) 	# steps are in order of addition to grid
		self.running = True										# required to use start/stop function
		self.id = 0														# to make sure all agents have individual id's
		self.traffic_lights = []								# list of all traffic lights on the grid
		self.east_flow = east_flow
		self.west_flow = west_flow
		self.north_flow = north_flow
		self.south_flow = south_flow					
		self.counter = 0
		self.choice = 0

		self.add_roads()											# add roads to the grid
		self.add_barriers()										# add 'barriers' in between the roads to the grid
		self.finish_background()							# fill all unused space in the grid
		self.add_traffic_lights()							# add traffic lights to the grid

	def count(self):
		self.counter += \
		len(self.grid.get_cell_list_contents((10, 8)))  + \
		len(self.grid.get_cell_list_contents((16, 10))) + \
		len(self.grid.get_cell_list_contents((14, 16))) + \
		len(self.grid.get_cell_list_contents((8, 14)))  - 4

		print ("COUNT", self.counter)

	# all the roads added to the grid
	def add_roads(self):
		self.add_road('east', 9, 0, 10)
		self.add_road('east', 10, 0, self.grid.width)
		self.add_road('east', 11, 0, 15)
		
		self.add_road('east', 13, 10, self.grid.width)
		self.add_road('east', 14, 0, self.grid.width)
		self.add_road('east', 15, 15, self.grid.width)

		self.add_road('north', 13, 0, 15)
		self.add_road('north', 14, 0, self.grid.height)
		self.add_road('north', 15, 0, 10)

		self.add_road('north', 9, 15, self.grid.height)
		self.add_road('north', 10, 0, self.grid.height)
		self.add_road('north', 11, 10, self.grid.height)

	# add a road to the grid
	def add_road(self, direction, position, begin, end):
		for i in range(begin, end):
			if direction == 'east':
				if self.grid.is_cell_empty([i,position]):
					self.add_background_agent('grey', i, position)
			if direction == 'north':
				if self.grid.is_cell_empty([position, i]):
					self.add_background_agent('grey', position, i)

	# all the 'barriers' added to the grid
	def add_barriers(self):
		self.add_barrier('east', 11, self.grid.width)
		self.add_barrier('east', 12, self.grid.width)
		self.add_barrier('east', 13, self.grid.width)
		
		self.add_barrier('north', 11, self.grid.height)
		self.add_barrier('north', 12, self.grid.height)
		self.add_barrier('north', 13, self.grid.height)

	# add a 'barrier' to the grid
	def add_barrier(self, direction, position, length):
		for i in range(0, length):
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

  # all the traffic lights added to the grid
	def add_traffic_lights(self):
		self.add_traffic_light(9, 9, self.east_flow, 'east', 'right')
		self.add_traffic_light(9, 10, self.east_flow, 'east')
		self.add_traffic_light(9, 11, self.east_flow, 'east', 'left')

		self.add_traffic_light(15, 13, self.west_flow, 'west', 'left')
		self.add_traffic_light(15, 14, self.west_flow, 'west')
		self.add_traffic_light(15, 15, self.west_flow, 'west', 'right')

		self.add_traffic_light(13, 9, self.north_flow, 'north', 'left')
		self.add_traffic_light(14, 9, self.north_flow, 'north')
		self.add_traffic_light(15, 9, self.north_flow, 'north', 'right')

		self.add_traffic_light(9, 15, self.south_flow, 'south', 'right')
		self.add_traffic_light(10, 15, self.south_flow, 'south')
		self.add_traffic_light(11, 15, self.south_flow, 'south', 'left')

	# add traffic light to the grid and schedule
	# x,y are coordinates of traffic light, direction which way its traffic goes
	def add_traffic_light(self, x, y, flow, direction, turn = ''):
		traffic_light = Traffic_light(self.id, self, flow, direction, turn)
		self.grid.place_agent(traffic_light, (x, y))
		self.schedule.add(traffic_light)    					
		self.id+=1
		self.traffic_lights.append(traffic_light)

	# add car to the grid and schedule
	def addCar(self, direction, x, y, flow):
		rand = random.randint(1,100)
		if flow > rand:  # atm 11% chance a car is added at a certain location
			if (len(list(self.grid.iter_cell_list_contents((x,y)))) < 2):
				car = Car(self.id, self, direction)				# create new car
				self.grid.place_agent(car, (x, y))	
				self.schedule.add(car)    				
				self.id += 1

	def choose_light(self, light, time):
		print(light.time)	
		if self.choice in range(0,3) and light.getDirection() == 'east' and light.round == False:
			print("Choice: " + str(self.choice) + ", direction: " + light.getDirection() +", time: " + str(time) + ", on time: " + str(light.getOnTime()))
			self.choose_light_helper(light, time)
		elif self.choice in range(3,6) and light.getDirection() == 'west' and light.round == True:
			print("Choice: " + str(self.choice) + ", direction: " + light.getDirection() +", time: " + str(time) + ", on time: " + str(light.getOnTime()))
			self.choose_light_helper(light, time)
		elif self.choice in range(6,9) and light.getDirection() == 'north' and light.round == False:
			print("Choice: " + str(self.choice) + ", direction: " + light.getDirection() +", time: " + str(time) + ", on time: " + str(light.getOnTime()))
			self.choose_light_helper(light, time)
		elif self.choice in range(9,12) and light.getDirection() == 'south' and light.round == True:
			print("Choice: " + str(self.choice) + ", direction: " + light.getDirection() +", time: " + str(time) + ", on time: " + str(light.getOnTime()))
			self.choose_light_helper(light, time)
		if self.choice == 12:
			self.choice = 0

	def choose_light_helper(self, light, time):
		if (time + 3) < light.getOnTime():
			light.turnOn()
		elif time < light.getOnTime() - 1:
			light.turnOff()
		else:
			self.choice += 1
		
  # at every step, cars may be added to the grid
	def step(self):
		self.schedule.step()
		self.addCar('east', 0, 9, self.east_flow)
		self.addCar('east', 0, 10, self.east_flow)
		self.addCar('east', 0, 11, self.east_flow)

		self.addCar('west', 24, 13, self.west_flow)
		self.addCar('west', 24, 14, self.west_flow)
		self.addCar('west', 24, 15, self.west_flow)
		
		self.addCar('north', 13, 0, self.north_flow)
		self.addCar('north', 14, 0, self.north_flow)
		self.addCar('north', 15, 0, self.north_flow)
		
		self.addCar('south', 9, 24, self.south_flow)
		self.addCar('south', 10, 24, self.south_flow)
		self.addCar('south', 11, 24, self.south_flow)
		self.count()
