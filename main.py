from mesa import *
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer
from car import *
from grid import *

# Main program, determines portrayal of agents and canvas and runs server

#Parameters settable by user

# Set direction in which the car(arrow) points
def setArrowDirection(agent, portrayal):
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

# set direction of the traffic light
def setRectDirection(agent, portrayal):
	if agent.getDirection() == 'south' or agent.getDirection() == 'north':
		portrayal['w'] = 0.8
		portrayal['h'] = 0.1
	if agent.getDirection() == 'east' or agent.getDirection() == 'west':
		portrayal['w'] = 0.1
		portrayal['h'] = 0.8

# portrayal of agent on the canvas
def agent_portrayal(agent):
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
	#if the agent is part of the background
	if agent.getType() == 'background':
		portrayal = {	'Shape': 'rect',
								'Color': agent.getColor(),
								'Filled': 'true',
								'Layer': 0,
								'w': 1,
								'h': 1	
								}
	return portrayal

flow_slider = UserSettableParameter('slider', "% traffic flow", 15, 1, 100, 5) 

# how the canvas looks
canvas = CanvasGrid(agent_portrayal, 25, 25, 750, 750) 

# which grid and canvas to run
server = ModularServer(Grid, [canvas], 'Traffic Flow Model', model_params= {"flow_percentage":flow_slider})			# ,{'x':10, 'y':10}
																			

server.port = 8523 # 8521 is default
server.launch()

