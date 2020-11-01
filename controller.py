from mesa import Agent


class Controller(Agent):
    """The controller of the demand based system"""

    def __init__(self, id, model):
        super().__init__(id, model)     # required, part of mesa
        self.type = 'controller'
        self.green_lights = 'east'
        self.time = 0
        self.delay_limit = 60   # max amount of time a car should have to wait

    def determine_light(self):
        """Determine which combination of lights has the highest demand.
        The time variable assures 7 second interval between two green lights"""
        self.time += 1
        demands = self.combine_demands()
        highest_demand = max(demands, key=demands.get)
        self.check_delay_limit()
        if not self.car_waiting_long():
            if demands[self.green_lights] < demands[highest_demand] - 6:
                if not self.car_waiting():
                    self.green_lights = highest_demand
                    self.time = 0

    def car_waiting(self):
        """Check whether there is a car waitin for the traffic light"""
        for light in self.model.traffic_lights:
            if light.get_direction() == self.green_lights:
                if not light.get_car_waiting():
                    return False
        return True

    def check_delay_limit(self):
        """Lower the delay limit back to 60 if possible, this is done
        to avoid the delay limit from increasing to much"""
        if self.delay_limit > 60:
            for light in self.model.traffic_lights:
                if light.get_waiting_time() > self.delay_limit - 16:
                    return
            self.delay_limit -= 16

    def car_waiting_long(self):
        """Check if there is a car waiting longer than the delay limit.
        If so, that car's light is prioritized and the delay limit
        is increased, to avoid switching after one second if multiple cars
        have reached the delay limit simultaneously."""
        for light in self.model.traffic_lights:
            if light.get_waiting_time() > self.delay_limit:
                self.green_lights = light.get_direction()
                if self.time > 8:
                    self.time = 0
                    self.delay_limit += 16
                return True
        return False

    def combine_demands(self):
        """Combine the demands of the individual lights
        in the different groups of lights"""
        demands = {'east': 0, 'west': 0, 'north': 0, 'south': 0}
        for light in self.model.traffic_lights:
            demands[light.get_direction()] += light.get_demand()
        return demands

    def get_type(self):
        """Get the type of the agent"""
        return self.type

    def step(self):
        """Called every step"""
        self.determine_light()
