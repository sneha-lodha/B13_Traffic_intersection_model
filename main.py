from mesa.visualization.modules import ChartModule, CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.ModularVisualization import ModularServer

from grid import Grid

""" Main loop of the program. The code is related to the canvas, so the
way the grid is displayed. Also, it sets and launches the local server"""


def setArrowDirection(agent, portrayal):
    """Set direction in which the car(arrow) points"""
    if agent.get_direction() == 'north':
        portrayal['heading_x'] = 0
        portrayal['heading_y'] = 1
    if agent.get_direction() == 'south':
        portrayal['heading_x'] = 0
        portrayal['heading_y'] = -1
    if agent.get_direction() == 'west':
        portrayal['heading_x'] = -1
        portrayal['heading_y'] = 0
    if agent.get_direction() == 'east':
        portrayal['heading_x'] = 1
        portrayal['heading_y'] = 0


def setRectDirection(agent, portrayal):
    """Set direction of the traffic light"""
    if agent.get_direction() == 'south' or agent.get_direction() == 'north':
        portrayal['w'] = 0.8
        portrayal['h'] = 0.1
    if agent.get_direction() == 'east' or agent.get_direction() == 'west':
        portrayal['w'] = 0.1
        portrayal['h'] = 0.8


def agent_portrayal(agent):
    """Portrayal of agent on the canvas"""
    if agent.get_type() == 'car':
        portrayal = {'Shape': 'arrowHead',
                     'Color': agent.get_color(),
                     'Filled': 'true',
                     'Layer': 2,
                     'scale': 0.5,
                     }
        # arrow points towards agents direction
        setArrowDirection(agent, portrayal)
        return portrayal

    if agent.get_type() == 'light':
        portrayal = {'Shape': 'rect',
                     'Color': agent.get_color(),
                     'Filled': 'true',
                     'Layer': 3,    # highest layer, so always visible
                     }
        setRectDirection(agent, portrayal)
        return portrayal

    if agent.get_type() == 'background':
        if agent.get_color() == 'green':
            portrayal = {'Shape': 'rect',
                         'Color': agent.get_color(), 'Filled': 'true',
                         'Layer': 0,   # lowest layer, so only background
                         'w': 25,
                         'h': 25
                         }
            return portrayal
        portrayal = {'Shape': 'rect',
                     'Color': agent.get_color(),
                     'Filled': 'true',
                     'Layer': 1,
                     'w': 1,
                     'h': 1
                     }
        return portrayal


# sliders that give the possibility to change the traffic flow
light_system = UserSettableParameter(
    'choice', 'Traffic system', value='Fixed time',
    choices=['Fixed time', 'Flow based', 'Demand based'])
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
chartTT = ChartModule([{"Label": "Avg wait time", "Color": "Black"}],
                      data_collector_name='dctt')
chartCC = ChartModule([{"Label": "Car count", "Color": "Blue"}],
                      data_collector_name='dccc')
# which grid and canvas to run
server = ModularServer(
    Grid,
    [canvas, chartTT, chartCC],
    'Traffic Flow Model',
    model_params={
        "east_flow": east_flow,
        "west_flow": west_flow,
        "south_flow": south_flow,
        "north_flow": north_flow,
        "system": light_system})

server.port = 8523  # 8521 is default
server.launch()
