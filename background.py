from mesa import Agent


class Background(Agent):
    """Simple class responsible for the background agents. These agents do
    not have much functionality except setting the background color of
    a certain cell in the multi-grid.
    """

    def __init__(self, id, model, color):
        super().__init__(id, model)		# required, part of mesa
        self.type = 'background'
        self.color = color

    def get_color(self):
        """Return the color of the current background agent in the cell."""
        return self.color

    def get_type(self):
        """Return the type background as the type of agent."""
        return self.type
