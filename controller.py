from mesa import *

class Controller(Agent):

    def __init__(self, id, model):
        super().__init__(id, model)		# required, part of mesa
        self.type = 'controller'
        self.green_lights = 'east'
        self.time = 0

    def determine_light(self):
        self.time += 1
        demands = self.combine_demands()
        highest_demand = max(demands, key=demands.get)
        print(demands[self.green_lights], demands[highest_demand])
        if demands[self.green_lights] < demands[highest_demand] - 6 :
            self.green_lights = highest_demand
            self.time = 0


    def combine_demands(self):
        demands = {'east': 0, 'west': 0, 'north': 0, 'south': 0}
        for light in self.model.traffic_lights:
            if light.direction == 'east':
                demands['east'] += light.demand
            if light.direction == 'west':
                demands['west'] += light.demand
            if light.direction == 'north':
                demands['north'] += light.demand
            if light.direction == 'south':
                demands['south'] += light.demand
        return demands



    def getType(self):
        """Get the type of the agent"""
        return self.type

    def step(self):
        """Called every step for every individual car"""
        self.determine_light()
