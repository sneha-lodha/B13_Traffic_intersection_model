from mesa import *
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from car import *
from grid import *

""" Main loop of the program. The code is related to the canvas, so the
way the grid is displayed. Also, it sets and launches the local server"""


def setArrowDirection(agent, portrayal):
    """Set direction in which the car(arrow) points"""
    if agent.getDirection() == 'north':
        portrayal['heading_x'] = 0
        portrayal['heading_y'] = 1
    if agent.getDirection() == 'south':
        portrayal['heading_x'] = 0
        portrayal['heading_y'] = -1
    if agent.getDirection() == 'west':
        portrayal['heading_x'] = -1
        portrayal['heading_y'] = 0
    if agent.getDirection() == 'east':
        portrayal['heading_x'] = 1
        portrayal['heading_y'] = 0


def setRectDirection(agent, portrayal):
    """Set direction of the traffic light"""
    if agent.getDirection() == 'south' or agent.getDirection() == 'north':
        portrayal['w'] = 0.8
        portrayal['h'] = 0.1
    if agent.getDirection() == 'east' or agent.getDirection() == 'west':
        portrayal['w'] = 0.1
        portrayal['h'] = 0.8


def agent_portrayal(agent):
    """Portrayal of agent on the canvas"""
    if agent.getType() == 'car':
        portrayal = {'Shape': 'arrowHead',
                     'Color': agent.getColor(),
                     'Filled': 'true',
                     'Layer': 2,
                     'scale': 0.5,
                     }
        # arrow points towards agents direction
        setArrowDirection(agent, portrayal)
        return portrayal

    if agent.getType() == 'light':
        portrayal = {'Shape': 'rect',
                     'Color': agent.getColor(),
                     'Filled': 'true',
                     'Layer': 3,                   # highest layer, so always visible
                     }
        setRectDirection(agent, portrayal)
        return portrayal

    if agent.getType() == 'background':
        if agent.getColor() == 'green':
            portrayal = { 'Shape': 'rect',      
            'Color': agent.getColor(),'Filled': 'true',
            'Layer': 0,                   # lowest layer, so only background
            'w': 25,                       
            'h': 25                        
            }
            return portrayal
        portrayal = {'Shape': 'rect',
                     'Color': agent.getColor(),
                     'Filled': 'true',
                     'Layer': 1,                   # lowest layer, so only background
                     'w': 1,
                     'h': 1
                     }
        return portrayal


# sliders that give possibility to change the traffic flow from specific
# direction
east_flow = UserSettableParameter(
    'slider', "% traffic flow from East", 15, 1, 100, 5)
west_flow = UserSettableParameter(
    'slider', "% traffic flow from West", 15, 1, 100, 5)
north_flow = UserSettableParameter(
    'slider', "% traffic flow from North", 15, 1, 100, 5)
south_flow = UserSettableParameter(
    'slider', "% traffic flow from South", 15, 1, 100, 5)

# how the canvas looks
canvas = CanvasGrid(agent_portrayal, 25, 25, 750, 750)

# which grid and canvas to run
server = ModularServer(
    Grid,
    [canvas],
    'Traffic Flow Model',
    model_params={
        "east_flow": east_flow,
        "west_flow": west_flow,
        "south_flow": south_flow,
        "north_flow": north_flow})

server.port = 8523  # 8521 is default
server.launch()
