from mesa import *
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from car import *
from grid import *

# Main program, determines portrayal of agents and canvas and runs server

# Parameters settable by user

# Set direction in which the car(arrow) points


def setArrowDirection(agent, portrayal):
<<<<<<< HEAD
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
=======
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
>>>>>>> 35290d95780010e9b52b2720adfa967e71d51bbf

# set direction of the traffic light


def setRectDirection(agent, portrayal):
<<<<<<< HEAD
    if agent.getDirection() == 'south' or agent.getDirection() == 'north':
        portrayal['w'] = 0.8
        portrayal['h'] = 0.1
    if agent.getDirection() == 'east' or agent.getDirection() == 'west':
        portrayal['w'] = 0.1
        portrayal['h'] = 0.8
=======
 if agent.getDirection() == 'south' or agent.getDirection() == 'north':
  portrayal['w'] = 0.8
  portrayal['h'] = 0.1
 if agent.getDirection() == 'east' or agent.getDirection() == 'west':
  portrayal['w'] = 0.1
  portrayal['h'] = 0.8
>>>>>>> 35290d95780010e9b52b2720adfa967e71d51bbf

# portrayal of agent on the canvas


def agent_portrayal(agent):
<<<<<<< HEAD
    # if the agent is a car
    if agent.getType() == 'car':
        portrayal = {	'Shape': 'arrowHead',
                      'Color': agent.getColor(),
                      'Filled': 'true',
                      'Layer': 1,
                      'scale': 0.5,
                      }
        setArrowDirection(agent, portrayal)
    if agent.getType() == 'light':
        portrayal = {	'Shape': 'rect',
                      'Color': agent.getColor(),
                      'Filled': 'true',
                      'Layer': 2,
                      }
        setRectDirection(agent, portrayal)
    # if the agent is part of the background
    if agent.getType() == 'background':
        portrayal = {	'Shape': 'rect',
                      'Color': agent.getColor(),
                      'Filled': 'true',
                      'Layer': 0,
                      'w': 1,
                      'h': 1
                      }
    return portrayal


east_flow = UserSettableParameter(
    'slider', "% traffic flow from East", 15, 1, 100, 5)
west_flow = UserSettableParameter(
    'slider', "% traffic flow from West", 15, 1, 100, 5)
north_flow = UserSettableParameter(
    'slider', "% traffic flow from North", 15, 1, 100, 5)
south_flow = UserSettableParameter(
    'slider', "% traffic flow from South", 15, 1, 100, 5)
=======
 # if the agent is a car
 if agent.getType() == 'car':
  portrayal = { 'Shape': 'arrowHead', # agent has shape of an arrowhead
        'Color': agent.getColor(),    # color us different for every agent
        'Filled': 'true',
        'Layer': 1,
        'scale': 0.5,
        }
  setArrowDirection(agent, portrayal) # arrow points towards agents direction
 # if the agent is a traffic light
 if agent.getType() == 'light':
  portrayal = { 'Shape': 'rect',      # agent has a rectangle shape
        'Color': agent.getColor(),    # color depends on the agent
        'Filled': 'true',
        'Layer': 2,                   # highest layer, so always visible
        }
  setRectDirection(agent, portrayal)  # set direction of the light
 #if the agent is part of the background
 if agent.getType() == 'background':
  portrayal = { 'Shape': 'rect',      # shape is a square
        'Color': agent.getColor(),
        'Filled': 'true',
        'Layer': 0,                   # is lowest layer, so only background
        'w': 1,                       # fills entire block
        'h': 1                        # fills entire block
        }
 return portrayal

# sliders that give possibility to change the traffic flow from specific direction
east_flow = UserSettableParameter('slider', "% traffic flow from East", 15, 1, 100, 5)
west_flow = UserSettableParameter('slider', "% traffic flow from West", 15, 1, 100, 5)
north_flow = UserSettableParameter('slider', "% traffic flow from North", 15, 1, 100, 5)
south_flow = UserSettableParameter('slider', "% traffic flow from South", 15, 1, 100, 5)

>>>>>>> 35290d95780010e9b52b2720adfa967e71d51bbf
# how the canvas looks
canvas = CanvasGrid(agent_portrayal, 25, 25, 750, 750)

# which grid and canvas to run
<<<<<<< HEAD
server = ModularServer(
    Grid,
    [canvas],
    'Traffic Flow Model',
    model_params={
        "east_flow": east_flow,
        "west_flow": west_flow,
        "south_flow": south_flow,
        "north_flow": north_flow})
=======
server = ModularServer(Grid, [canvas], 'Traffic Flow Model', model_params= {"east_flow": east_flow, 
                   "west_flow": west_flow, 
                   "south_flow": south_flow, 
                   "north_flow": north_flow})
                   
>>>>>>> 35290d95780010e9b52b2720adfa967e71d51bbf


server.port = 8523  # 8521 is default
server.launch()
