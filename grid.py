from mesa import *
from mesa.space import *
from mesa.time import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.datacollection import DataCollector

from background import *
from car import *
from controller import *
from trafficlight import *


class Grid(Model):
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
        self.wait_times = []
        self.average_wait_time = 0
        self.dctt = DataCollector(model_reporters={"Avg wait time": lambda model: model.average_wait_time})
        self.dccc = DataCollector(model_reporters={"Car count": lambda model: model.car_counter})

        # Adds all the different agents to the blocks in the model
        self.add_roads()
        self.add_barriers()
        self.finish_background()
        self.add_traffic_lights()
        self.add_controller()

    def count_cars(self):
        """ Function to count the number of cars that have cleared the model.
        They are counted when they have successfully crossed the intersection
        and left the screen.
        """
        self.car_counter += \
            len(self.grid.get_cell_list_contents((0, 14))) + \
            len(self.grid.get_cell_list_contents((10, 0))) + \
            len(self.grid.get_cell_list_contents((24, 10))) + \
            len(self.grid.get_cell_list_contents((14, 24))) - 4

        print("COUNT", self.car_counter)

    def calculate_average_wait_time(self):
        all_agents = []
        all_agents += self.grid.get_cell_list_contents((0,14))
        all_agents += self.grid.get_cell_list_contents((10,0))
        all_agents += self.grid.get_cell_list_contents((24,10))
        all_agents += self.grid.get_cell_list_contents((14,24))
        for agent in all_agents:
            if (agent.type == "car"):
                self.wait_times.append(agent.wait_time)
        if len(self.wait_times) != 0:
            self.average_wait_time = sum(self.wait_times)/len(self.wait_times)
            print ("Average travel time of cars is:", self.average_wait_time)
        else:
            print ("No cars have passed yet")
            return 0
    
    def add_controller(self):
        controller = Controller(self.id, self)
        self.schedule.add(controller)
        self.grid.place_agent(controller, (0, 0))
        self.id += 1

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
        """ Adds a large background agent with the same size of the grid """
        self.add_background_agent('green', 12, 12)

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
    def add_car(self, direction, x, y, flow):
        """Function to add a car to grid at position (x, y) going in the
        given direction.

        The car is added based on the value of the flow. Higher the value of flow,
        the higher the probability of the car being added.
        """
        rand = random.randint(1, 100)
        if flow > rand:  # atm 11% chance a car is added at a certain location
            cell = list(self.grid.iter_cell_list_contents((x, y)))
            for agent in cell:
                if (agent.type == 'car'):
                    return
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

        # Adding 3 determines the pause of 3 seconds between different green
        # lights.
        first = 3
        second = first + on_times[0]
        third = second + 3
        fourth = third + on_times[1]
        fifth = fourth + 3
        sixth = fifth + on_times[2]
        seventh = sixth + 3
        eighth = seventh + on_times[3]

        return [first, second, third, fourth, fifth, sixth, seventh, eighth]


  # at every step, cars may be added to the grid
    def step(self):
        """Step function that is automatically called at each time step of
        the model.

        Attempt to add cars in all directions based on the flow value. And
        also count the amount of cars passed at each time step.
        """
        # self.determine_light()
        self.schedule.step()
        self.add_car('east', 0, 9, self.flows[0])
        self.add_car('east', 0, 10, self.flows[0])
        self.add_car('east', 0, 11, self.flows[0])

        self.add_car('west', 24, 13, self.flows[1])
        self.add_car('west', 24, 14, self.flows[1])
        self.add_car('west', 24, 15, self.flows[1])

        self.add_car('north', 13, 0, self.flows[2])
        self.add_car('north', 14, 0, self.flows[2])
        self.add_car('north', 15, 0, self.flows[2])

        self.add_car('south', 9, 24, self.flows[3])
        self.add_car('south', 10, 24, self.flows[3])
        self.add_car('south', 11, 24, self.flows[3])
        self.count_cars()
        self.calculate_average_wait_time()
        self.dctt.collect(self)
        self.dccc.collect(self)
