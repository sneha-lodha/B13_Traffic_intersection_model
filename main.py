from mesa import *

from car import *
from grid import *

# Main program, determines portrayal of agents and canvas and runs server

# portrayal of agent on the canvas
def agent_portrayal(agent):
	# if the agent is a car
	if agent.getType() == 'car':
		portrayal = {	'Shape': 'circle',
								'Color': agent.getColor(),
								'Filled': 'true',
								'Layer': 1,
								'r': 0.5
								}

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

# how the canvas looks
canvas = CanvasGrid(agent_portrayal, 11, 11, 500, 500) 

# which grid and canvas to run
server = ModularServer(Grid, [canvas], 'Grid'
																			# ,{'x':10, 'y':10}
																			)

server.port = 8523 # 8521 is default
server.launch()

