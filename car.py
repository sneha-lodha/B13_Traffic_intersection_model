import random

from mesa import Agent


class Car(Agent):
    """The car class manages all the decision made by the individual cars.
    Most of the code of this class is related to the move function, which
    determines whether the car can move."""

    def __init__(self, id, model, direction):
        super().__init__(id, model)     # required by mesa
        self.type = 'car'
        self.color = self.set_color()
        self.direction = direction      # direction the car is travelling
        self.distance = 0               # distance the car has travelled
        self.wait_time = 0

    def remove_agent(self):
        """Remove agent from the grid if it reached the end"""
        self.model.schedule.remove(self)
        self.model.grid.remove_agent(self)

    def can_move(self, edge, x):
        """Check if a car can/is allowed to move"""
        light = self.get_traffic_light()  # determine relevant traffic light
        if self.pos[x] == edge:        # if agent has reached end of the grid
            self.remove_agent()
            return False                  # car cannot move, as it is gone
        if light.color == 'red' and (
                self.car_ahead() or self.pos[x] == light.pos[x]):
            return False                  # car cannot move forward
        return True                    # car can move forward

    def move_forward(self, x, y):
        """Move agent 1 cell forward and increase travelled distance by one"""
        self.model.grid.move_agent(self, (self.pos[0] + x, self.pos[1] + y))
        self.distance += 1

    def move(self):
        """ Main move loop, determines if and where the car moves """
        if self.direction == 'east':
            if self.can_move(self.model.grid.width - 1, 0):
                if self.turn_ahead():            # if car has to turn
                    if self.distance < self.model.grid.width / 2:
                        # car has to turn right
                        self.turn('south', 0, -1)
                    else:
                        # car has to turn left
                        self.turn('north', 0, 1)
                else:
                    self.move_forward(1, 0)
            else:
                self.wait_time += 1

        # all the other 3 parts work the same, just with different variables
        elif self.direction == 'west':
            if self.can_move(0, 0):
                if self.turn_ahead():
                    if self.distance < self.model.grid.width / 2:
                        self.turn('north', 0, 1)
                    else:
                        self.turn('south', 0, -1)
                else:
                    self.move_forward(-1, 0)
            else:
                self.wait_time += 1

        elif self.direction == 'north':
            if self.can_move(self.model.grid.width - 1, 1):
                if self.turn_ahead():
                    if self.distance < self.model.grid.width / 2:
                        self.turn('east', 1, 0)
                    else:
                        self.turn('west', -1, 0)
                else:
                    self.move_forward(0, 1)
            else:
                self.wait_time += 1

        elif self.direction == 'south':
            if self.can_move(0, 1):
                if self.turn_ahead():
                    if self.distance < self.model.grid.width / 2:
                        self.turn('west', -1, 0)
                    else:
                        self.turn('east', 1, 0)
                else:
                    self.move_forward(0, -1)
            else:
                self.wait_time += 1

    def get_traffic_light(self):
        """Get the correct traffic light"""
        for light in self.model.traffic_lights:  # loop over all lights
            # if light has same direction as car
            if light.direction == self.direction:
                if self.direction == 'east' or self.direction == 'west':
                    # light has to be in same lane as car
                    if light.pos[1] == self.pos[1]:
                        return light
                if self.direction == 'north' or self.direction == 'south':
                    # light has to be in same lane as car
                    if light.pos[0] == self.pos[0]:
                        return light

    def look_ahead(self):
        """Look at the contents of the cell 1 position ahead"""
        if(self.direction == 'east'):
            cellContents = list(
                self.model.grid.iter_cell_list_contents(
                    (self.pos[0] + 1, self.pos[1])))
        elif(self.direction == 'west'):
            cellContents = list(
                self.model.grid.iter_cell_list_contents(
                    (self.pos[0] - 1, self.pos[1])))
        elif(self.direction == 'south'):
            cellContents = list(
                self.model.grid.iter_cell_list_contents(
                    (self.pos[0], self.pos[1] - 1)))
        elif(self.direction == 'north'):
            cellContents = list(
                self.model.grid.iter_cell_list_contents(
                    (self.pos[0], self.pos[1] + 1)))
        return cellContents

    def turn_ahead(self):
        """Check whether the car has to make a turn"""
        cellAhead = self.look_ahead()
        for agent in cellAhead:
            # if next cell is a barrier
            if(agent.type == 'background' and agent.color == 'darkslategrey'):
                return True              # car has to make a turn
        return False               # car does not have to make a turn

    def car_ahead(self):
        """Check whether there is a car in the cell ahead"""
        cellAhead = self.look_ahead()   # get content from cell ahead
        for agent in cellAhead:
            if(agent.type == 'car'):
                return True                  # there is a car ahead
        return False                   # there is no car ahead

    def step(self):
        """Called every step for every individual car"""
        self.move()

    def turn(self, direction, x, y):
        """General turn function"""
        self.direction = direction    # change direction the car is moving in
        # move one cell forward in new direction
        self.move_forward(x, y)

    def set_color(self):
        """Selects a color for the car"""
        colors = ['black', 'yellow', 'blue', 'brown', 'white']
        x = random.randint(0, 3)
        return colors[x - 1]

    def get_color(self):
        """Get the color of the car"""
        return self.color

    def get_type(self):
        """Get the type of the car"""
        return self.type

    def get_direction(self):
        """Get the direction of the car"""
        return self.direction
