import random

from mesa import *


# Background blocks used in the grid
class Background(Agent):
    """Simple class responsible for the background agents. These agents do
    not have much functionality except setting the background color of
    a certain cell in the multi-grid.
    """

    def __init__(self, id, model, color):
        super().__init__(id, model)		# required, part of mesa
        self.type = 'background'
        self.color = color

    def getColor(self):
        """Return the color of the current background agent in the cell."""
        return self.color

    def getType(self):
        """Return the type background as the type of agent."""
        return self.type
