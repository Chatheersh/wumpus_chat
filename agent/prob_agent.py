from environment.action import Action
import copy
import random
from typing import List, Set
from agent.beeline_agent import BeelineAgent
from environment.agent_state import AgentState
from environment.coordinate import Coordinate
from pomegranate import BayesianNetwork
from environment.grid import Grid

from environment.percept import Percept
from environment.pit_model import PitModel
from environment.prob_grid import ProbGrid

class ProbAgent(BeelineAgent):
    def __init__(self, grid_width: int, 
                       grid_height: int, 
                       agent_state: AgentState, 
                       visited_locations: Set[Coordinate], 
                       beeline_action_list: List[Action],
                       stench_locations: dict,
                       breeze_locations: dict,
                       heard_scream: bool,
                       wumpus_probability_model: BayesianNetwork,
                       pit_probability_model: PitModel):
        
        self.grid_width = grid_width
        self.grid_height = grid_height
        
        self.agent_state = agent_state
        self.visited_locations = visited_locations
        self.beeline_action_list = beeline_action_list

        self.stench_locations = stench_locations
        self.breeze_locations = breeze_locations
        self.heard_scream = heard_scream

        self.wumpus_probability_model = wumpus_probability_model
        self.pit_probability_model = pit_probability_model

        self.visited_locations_grid = Grid(self.grid_width, self.grid_height)
        self.visited_locations_grid.set_one(0, 0)

        self.is_retracing_steps = False

    def _get_wumpus_probability_grid(self): 
        response = self.wumpus_probability_model.predict_proba(self.stench_locations)
        w_probability_grid = ProbGrid(self.grid_width, self.grid_height)

        # update wumpus probability grid
        for str_coord, probability in response[0].parameters[0].items():
            x = int(str_coord.split(',')[0])
            y = int(str_coord.split(',')[1])

            w_probability_grid.set_value(x, y, probability)

        return w_probability_grid

    def _get_pit_probability_grid(self):
        response = self.pit_probability_model.predict_proba(self.breeze_locations)
        p_probability_grid = ProbGrid(self.grid_width, self.grid_height)

        # update pit probability grid
        for i in range(0, self.grid_width):
            for j in range(0, self.grid_height):

                if i == 0 and j == 0:
                    continue

                index = f"{i},{j}"
                probability = self.pit_probability_model.fetch_response(index, response).parameters[0][True]
                p_probability_grid.set_value(i, j, probability)

        return p_probability_grid

    def _get_unsafe_locations_grid(self, width: int, height: int):
        unsafe_locations_grid = Grid(width, height)

        w_probability_grid = self._get_wumpus_probability_grid()
        p_probability_grid = self._get_pit_probability_grid()

        for i in range(0, width):
            for j in range(0, height):
                if round(w_probability_grid.get_value(i, j), 1) >= 0.5 or round(p_probability_grid.get_value(i, j), 1) >= 0.5:
                    unsafe_locations_grid.set_value(i, j, 1)

        return unsafe_locations_grid

    def _move_forward(self):
        self.agent_state.forward(self.grid_width, self.grid_height)
        new_location = copy.deepcopy(self.agent_state.location)
        self.visited_locations.add(new_location)
        self.visited_locations_grid.set_one(self.agent_state.location.x, self.agent_state.location.y)

    def _beeline(self):

        self.is_retracing_steps = True

        if not self.beeline_action_list:
            self.beeline_action_list = self._construct_beeline()
 
        action = self.beeline_action_list.pop(0)
        self.agent_state.apply_move_action(action, self.grid_width, self.grid_height)
        return action

    def _clear_beeline(self):
        if self.beeline_action_list:
            self.is_retracing_steps = False
            self.beeline_action_list = None

    def _get_adjacent_safe_coordinates(self, unsafe_locations_grid: Grid, visited_locations: Grid):

        adjacent_coordinates = []
        
        x = self.agent_state.location.x
        y = self.agent_state.location.y

        def is_visitable(x, y):
            return x >= 0 and x < self.grid_width and y >= 0 and y <= self.grid_height \
                and unsafe_locations_grid.get_value(x, y) != 1 and visited_locations.get_value(x,y) != 1

        if is_visitable(x - 1, y):
            adjacent_coordinates.append(Coordinate(x - 1, y))
        
        if is_visitable(x + 1, y):
            adjacent_coordinates.append(Coordinate(x + 1, y))

        if is_visitable(x, y - 1):
            adjacent_coordinates.append(Coordinate(x, y - 1))

        if is_visitable(x, y + 1):
            adjacent_coordinates.append(Coordinate(x, y + 1))

        return adjacent_coordinates

    def next_action(self, percept: Percept) -> Action:

        # check if heard scream
        if percept.scream is True:
            self.heard_scream = True

        # fetch current location
        current_location = self.agent_state.location

        # if there is a stench in current location, add to list
        if percept.stench is True:
            self.stench_locations[f"{current_location.x},{current_location.y}"] = True

        # if there is a breeze at current location, add to list
        if percept.breeze is True:
            self.breeze_locations[f"breeze_{current_location.x}_{current_location.y}"] = True
        
        # get the wumpus and pit probability grids
        unsafe_locations_grid = self._get_unsafe_locations_grid(self.grid_width, self.grid_height)

        if self.agent_state.location == Coordinate(0, 0) and self.is_retracing_steps:
            return Action.CLIMB

        if self.agent_state.has_gold:
            if self.agent_state.location == Coordinate(0, 0):
                return Action.CLIMB
            else:
                return self._beeline()
        elif percept.glitter:
            self.agent_state.has_gold = True
            return Action.GRAB
        elif percept.stench and self.agent_state.has_arrow:
            self.agent_state.use_arrow()
            return Action.SHOOT
        else:
            adjacent_coords = self._get_adjacent_safe_coordinates(unsafe_locations_grid, self.visited_locations_grid)

            if not adjacent_coords:
                return self._beeline()
            else:
                # if a beeline was constructed in the past, but we still have viable options
                # lets not give up just yet
                self._clear_beeline()

            if self.agent_state.get_forward_coordinate(self.grid_width, self.grid_height) not in adjacent_coords:
                self.agent_state.turn_right()
                return Action.TURN_RIGHT
            else:
                random_number = random.randint(0, 2)

                if random_number == 0:
                    self._move_forward()
                    return Action.FORWARD
                elif random_number == 1:
                    self.agent_state.turn_left()
                    return Action.TURN_LEFT
                elif random_number == 2:
                    self.agent_state.turn_right()
                    return Action.TURN_RIGHT
    
