from random import random
import random
from typing import List, Set
from agent.agent import Agent
from environment.action import Action
from environment.agent_state import AgentState
from environment.coordinate import Coordinate
from environment.graph import generate_graph
from environment.orientation import Orientation
from environment.percept import Percept
from environment.grid import Grid

import networkx as nx
import copy
class BeelineAgent(Agent):

    def __init__(self, grid_width, grid_height, 
                       agent_state: AgentState, 
                       safe_locations: Set[Coordinate], 
                       beeline_action_list: List[Action]):
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        self.agent_state = agent_state
        self.safe_locations = safe_locations
        self.beeline_action_list = beeline_action_list

    def _construct_beeline(self) -> List[Action]:

        actions = []

        max_x_coordinate = 0
        max_y_coordinate = 0

        for coordinate in self.safe_locations:
            max_x_coordinate = max(max_x_coordinate, coordinate.x)
            max_y_coordinate = max(max_y_coordinate, coordinate.y)
        
        percept_width = max_x_coordinate + 1
        percept_height = max_y_coordinate + 1

        def mark_safe_locations(grid: Grid, safe_locations: List[Coordinate]):
            for coordinate in safe_locations:
                grid.set_one(coordinate.x, coordinate.y)
            
            return grid
        
        safe_locations_grid = Grid(percept_width, percept_height)
        mark_safe_locations(safe_locations_grid, self.safe_locations)

        def number_locations(width, height, grid):
            k = width * height - 1

            grid = Grid(width, height)

            for y in range(height - 1, -1, -1):
                for x in range(width - 1, -1, -1):
                    grid.set_value(x, y, k)
                    k -= 1

            return grid
        
        numbered_locations_grid = Grid(percept_width, percept_height)
        numbered_locations_grid = number_locations(percept_width, percept_height, numbered_locations_grid)

        path_list = generate_graph(numbered_locations_grid, 
                                   safe_locations_grid, 
                                   percept_width, 
                                   percept_height, 
                                   Coordinate(0, 0), 
                                   self.agent_state.location)

        # remove last element in list
        del path_list[-1]
        position = copy.deepcopy(self.agent_state.location)
        orientation = copy.deepcopy(self.agent_state.orientation)

        for i in reversed(path_list):
            if position.x - 1 >= 0 and numbered_locations_grid.get_value(position.x - 1, position.y) == i:
                while orientation != orientation.WEST:
                    orientation = Orientation.turn_left(orientation)
                    actions.append(Action.TURN_LEFT)
                position.x -= 1
            elif position.x + 1 < percept_width and numbered_locations_grid.get_value(position.x + 1, position.y) == i:
                while orientation != orientation.EAST:
                    orientation = Orientation.turn_right(orientation)
                    actions.append(Action.TURN_RIGHT)
                position.x += 1
            elif position.y - 1 >= 0 and numbered_locations_grid.get_value(position.x, position.y - 1) == i:
                while orientation != orientation.SOUTH:
                    orientation = Orientation.turn_right(orientation)
                    actions.append(Action.TURN_RIGHT)
                position.y -= 1
            elif position.y + 1 < percept_height and numbered_locations_grid.get_value(position.x, position.y + 1) == i:
                while orientation != orientation.WEST:
                    orientation = Orientation.turn_left(orientation)
                    actions.append(Action.TURN_LEFT)
                position.y += 1

            actions.append(Action.FORWARD)

        return actions


    def next_action(self, percept: Percept) -> Action:
        
        if self.agent_state.has_gold:
            if self.agent_state.location == Coordinate(0, 0):
                return Action.CLIMB
            else:
                if not self.beeline_action_list:
                    self.beeline_action_list = self._construct_beeline()
 
                action = self.beeline_action_list.pop(0)
                self.agent_state.apply_move_action(action, self.grid_width, self.grid_height)
                return action
        elif percept.glitter:
            self.agent_state.has_gold = True
            return Action.GRAB
        else:
            random_number = random.randint(0, 3)

            if random_number == 0:
                self.agent_state.forward(self.grid_width, self.grid_height)
                new_location = copy.deepcopy(self.agent_state.location)
                self.safe_locations.add(new_location)
                return Action.FORWARD
            elif random_number == 1:
                self.agent_state.turn_left()
                return Action.TURN_LEFT
            elif random_number == 2:
                self.agent_state.turn_right()
                return Action.TURN_RIGHT
            elif random_number == 3:
                self.agent_state.use_arrow()
                return Action.SHOOT