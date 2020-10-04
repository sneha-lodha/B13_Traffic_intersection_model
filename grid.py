from mesa import *
from mesa.space import *
from mesa.time import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from car import *
from background import *
from trafficlight import *


class Grid(Model):
<<<<<<< HEAD

    def __init__(self, east_flow, west_flow, north_flow, south_flow):
        """The Grid class deals with the actual model of the whole simulation
        and add all the agents to the grid and initializes the model.

        We use MultiGrid, which means that multiple agents can be added to the
        same cell.

        Four flow parameters are passed to initalize the model. These represent 
        flow of the cars from the 4 different directions in the simulation.
        """
        self.grid = MultiGrid(25, 25, False)
        self.schedule = BaseScheduler(self)
        self.running = True										
        self.id = 0														
        self.traffic_lights = []							
        self.flows = [east_flow, west_flow, north_flow, south_flow]
        self.car_counter = 0

        # Adds all the different agents to the blocks in the model
        self.add_roads()									
        self.add_barriers()								
        self.finish_background()							
        self.add_traffic_lights()				

    def count_cars(self):
        """ Function to count the number of cars that have cleared the model.
        They are counted when they have successfully crossed the intersection
        and left the screen.
        """
        self.car_counter += \
            len(self.grid.get_cell_list_contents((10, 8))) + \
            len(self.grid.get_cell_list_contents((16, 10))) + \
            len(self.grid.get_cell_list_contents((14, 16))) + \
            len(self.grid.get_cell_list_contents((8, 14))) - 4

        print("COUNT", self.car_counter)

    def add_background_agent(self, color, x, y):
        """Function that given a color and a position (x, y) fills
        that position with the background color.
        """
        self.grid.place_agent(Background(self.id, self, color), (x, y))
        self.id += 1

    def add_road(self, direction, position, begin, end):
        """Function that places a background agent with the color gray to
        mimic a road. This take direction as a prameter to determine which
        direction the road takes.
        """
        for i in range(begin, end):
            if direction == 'east':
                if self.grid.is_cell_empty([i, position]):
                    self.add_background_agent('grey', i, position)
            if direction == 'north':
                if self.grid.is_cell_empty([position, i]):
                    self.add_background_agent('grey', position, i)

    def add_roads(self):
        """Function that adds all the different roads to the simualation"""
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

    def add_barrier(self, direction, position, length):
        """Adds the dark gray background agent to the road acting
        as barriers on which cars cannot go on top of.
        """
        for i in range(0, length):
            if direction == 'east':
                if self.grid.is_cell_empty([i, position]):
                    self.add_background_agent('darkslategrey', i, position)
            if direction == 'north':
                if self.grid.is_cell_empty([position, i]):
                    self.add_background_agent('darkslategrey', position, i)

    def add_barriers(self):
        """Function that adds all the barriers to the simulation"""
        self.add_barrier('east', 11, self.grid.width)
        self.add_barrier('east', 12, self.grid.width)
        self.add_barrier('east', 13, self.grid.width)

        self.add_barrier('north', 11, self.grid.height)
        self.add_barrier('north', 12, self.grid.height)
        self.add_barrier('north', 13, self.grid.height)

    def finish_background(self):
        """Fills the rest of the grid where there is no background, with
        a green background.
        """
        for i in range(0, self.grid.width):
            for j in range(0, self.grid.height):
                if self.grid.is_cell_empty([i, j]):
                    self.add_background_agent('green', i, j)

    def add_traffic_light(self, x, y, direction, turn=''):
        """Adds a traffic light to the grid and also the scheduler. 

        (x, y) are the coordinates of the light and direction is the direction
        of flow that the traffic light controls. 
        """
        traffic_light = Traffic_light(self.id, self, direction, turn)
        self.grid.place_agent(traffic_light, (x, y))
        self.schedule.add(traffic_light)
        self.id += 1
        self.traffic_lights.append(traffic_light)

    def add_traffic_lights(self):
        """Function to add all the traffic lights to the grid"""
        self.add_traffic_light(9, 9, 'east', 'right')
        self.add_traffic_light(9, 10, 'east')
        self.add_traffic_light(9, 11, 'east', 'left')

        self.add_traffic_light(15, 13, 'west', 'left')
        self.add_traffic_light(15, 14, 'west')
        self.add_traffic_light(15, 15, 'west', 'right')

        self.add_traffic_light(13, 9, 'north', 'left')
        self.add_traffic_light(14, 9, 'north')
        self.add_traffic_light(15, 9, 'north', 'right')

        self.add_traffic_light(9, 15, 'south', 'right')
        self.add_traffic_light(10, 15, 'south')
        self.add_traffic_light(11, 15, 'south', 'left')

    # add car to the grid and schedule
    def addCar(self, direction, x, y, flow):
        """Function to add a car to grid at position (x, y) going in the 
        given direction. 
        
        The car is added based on the value of the flow. Higher the value of flow,
        the higher the probability of the car being added.
        """
        rand = random.randint(1, 100)
        if flow > rand:  # atm 11% chance a car is added at a certain location
            if (len(list(self.grid.iter_cell_list_contents((x, y)))) < 2):
                car = Car(self.id, self, direction)				# create new car
                self.grid.place_agent(car, (x, y))
                self.schedule.add(car)
                self.id += 1

    def calculate_on_time(self, flow):
        """Function that given the value of the flow in a certain direction, 
        determines how long the light should stay green. 

        If flow higher than 50, light stay green for 16 time steps, otherwise
        only 5 time steps.
        """
        if flow < 50:
            time = 5
        else:
            time = 16
        return time

    def calculate_timer(self):
        """Based on the flow of the cars from different directions, calculates the
        times at which the lights should switch colors. 

        Always a pause of 3 seconds between different green lights to avoid crashes.
        """
        on_times = []
        # Calculates on times for each direction based on flow.
        for flow in self.flows:
            on_times.append(self.calculate_on_time(flow))
        
        # Adding 3 determines the pause of 3 seconds between different green lights.
        first = 3
        second = first + on_times[0]
        third = second + 3
        fourth = third + on_times[1]
        fifth = fourth + 3
        sixth = fifth + on_times[2]
        seventh = sixth + 3
        eighth = seventh + on_times[3]

        return [first, second, third, fourth, fifth, sixth, seventh, eighth]
=======
	
	def __init__(self, east_flow, west_flow, north_flow, south_flow):
		self.grid = MultiGrid(25, 25, False)	# grid can contain multiple agents per square
		self.schedule = BaseScheduler(self) 	# steps are in order of addition to grid
		self.running = True										# required to use start/stop function
		self.id = 0														# to make sure all agents have individual id's
		self.traffic_lights = []								# list of all traffic lights on the grid
		self.flows = [east_flow, west_flow, north_flow, south_flow]					
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
		self.add_traffic_light(9, 9, self.flows[0], 'east', 'right')
		self.add_traffic_light(9, 10, self.flows[0], 'east')
		self.add_traffic_light(9, 11, self.flows[0], 'east', 'left')

		self.add_traffic_light(15, 13, self.flows[1], 'west', 'left')
		self.add_traffic_light(15, 14, self.flows[1], 'west')
		self.add_traffic_light(15, 15, self.flows[1], 'west', 'right')

		self.add_traffic_light(13, 9, self.flows[2], 'north', 'left')
		self.add_traffic_light(14, 9, self.flows[2], 'north')
		self.add_traffic_light(15, 9, self.flows[2], 'north', 'right')

		self.add_traffic_light(9, 15, self.flows[3], 'south', 'right')
		self.add_traffic_light(10, 15, self.flows[3], 'south')
		self.add_traffic_light(11, 15, self.flows[3], 'south', 'left')

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

	def calculate_timer(self):
		on_times = []
		for flow in self.flows:
			on_times.append(self.calculate_on_time(flow))
		first = 3
		second = first + on_times[0]
		third = second + 3
		fourth = third + on_times[1]
		fifth = fourth + 3
		sixth = fifth + on_times[2]
		seventh = sixth + 3
		eighth = seventh + on_times[3] 

		return [first, second, third, fourth, fifth, sixth, seventh, eighth]
	
	def calculate_on_time(self, flow):
		if flow < 10:
			time = 0
		else:
			time = 16
		return time
>>>>>>> 35290d95780010e9b52b2720adfa967e71d51bbf

  # at every step, cars may be added to the grid
    def step(self):
        """Step function that is automatically called at each time step of 
        the model. 

        Attempt to add cars in all directions based on the flow value. And
        also count the amount of cars passed at each time step.
        """
        self.schedule.step()
        self.addCar('east', 0, 9, self.flows[0])
        self.addCar('east', 0, 10, self.flows[0])
        self.addCar('east', 0, 11, self.flows[0])

        self.addCar('west', 24, 13, self.flows[1])
        self.addCar('west', 24, 14, self.flows[1])
        self.addCar('west', 24, 15, self.flows[1])

        self.addCar('north', 13, 0, self.flows[2])
        self.addCar('north', 14, 0, self.flows[2])
        self.addCar('north', 15, 0, self.flows[2])

        self.addCar('south', 9, 24, self.flows[3])
        self.addCar('south', 10, 24, self.flows[3])
        self.addCar('south', 11, 24, self.flows[3])
        self.count_cars()
