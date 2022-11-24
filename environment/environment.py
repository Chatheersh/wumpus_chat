import copy

from environment.action import Action
from typing import List
from environment.agent import Agent
from environment.coordinate import Coordinate
from environment.orientation import Orientation
from environment.percept import Percept


class Environment:
    def __init__(self, grid_width: int, 
                       grid_height: int, 
                       allow_climb_without_gold: bool, 
                       agent: Agent, 
                       pit_locations: List[Coordinate], 
                       is_terminated: bool, 
                       wumpus_location: Coordinate, 
                       is_wumpus_alive: bool, 
                       gold_location: Coordinate):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.allow_climb_without_gold = allow_climb_without_gold
        self.agent = agent
        self.pit_locations = pit_locations
        self.is_terminated = is_terminated
        self.wumpus_location = wumpus_location
        self.is_wumpus_alive = is_wumpus_alive
        self.gold_location = gold_location

    def is_pit_at(self, coordinate: Coordinate) -> bool: 
        return any(coordinate.x == l.x and coordinate.y == l.y for l in self.pit_locations)

    def is_wumpus_at(self, coordinate: Coordinate) -> bool:
        return coordinate == self.wumpus_location

    def is_agent_at(self, coordinate: Coordinate) -> bool:
        return coordinate == self.agent.location
    
    def is_glitter(self):
        return self.agent.location == self.gold_location
    
    def is_gold_at(self, coordindate: Coordinate):
        return coordindate == self.gold_location
    
    def kill_attempt_is_successful(self):

        def wumpus_in_line_of_fire():
            orientation = self.agent.orientation

            if orientation == Orientation.WEST:
                return self.agent.location.x > self.wumpus_location.x and self.agent.location.y == self.wumpus_location.y
            elif orientation == Orientation.EAST:
                return self.agent.location.x < self.wumpus_location.x and self.agent.location.y == self.wumpus_location.y
            elif orientation == Orientation.SOUTH:
                return self.agent.location.x == self.wumpus_location.x and self.agent.location.y > self.wumpus_location.y
            elif orientation == Orientation.NORTH:
                return self.agent.location.x == self.wumpus_location.x and self.agent.location.y < self.wumpus_location.y
    
        return self.agent.has_arrow and self.is_wumpus_alive and wumpus_in_line_of_fire()
    
    def adjacent_cells(self, coordinate: Coordinate) -> List[Coordinate]:

        left_coordinates = [Coordinate(coordinate.x - 1, coordinate.y)] if coordinate.x > 0 else [None]

        right_coordinates = [Coordinate(coordinate.x + 1, coordinate.y)] if coordinate.x < self.grid_width - 1 else [None]

        bottom_coordinates = [Coordinate(coordinate.x, coordinate.y - 1)] if coordinate.y > 0 else [None]

        top_coorindates = [Coordinate(coordinate.x, coordinate.y + 1)] if coordinate.y < self.grid_height - 1 else [None]

        return  left_coordinates + right_coordinates + bottom_coordinates + top_coorindates

    def is_pit_adjacent(self, coordinate: Coordinate) -> bool:
        
        for a in self.adjacent_cells(coordinate):
            if a:
                for p in self.pit_locations:
                    if a.x == p.x and a.y == p.y:
                        return True
        
        return False

    def is_wumpus_adjacent(self, coordinate: Coordinate) -> bool:
        return any(a.x == self.wumpus_location.x and a.y == self.wumpus_location.y for a in self.adjacent_cells(coordinate) if a)

    def is_breeze(self) -> bool:
        return self.is_pit_adjacent(self.agent.location)
    
    def is_stench(self) -> bool:
        return self.is_wumpus_adjacent(self.agent.location) or self.is_wumpus_at(self.agent.location)

    def apply_action(self, action: Action):

        environment = None
        percept = None

        if self.is_terminated:
            return (self, Percept(False, False, False, False, False, True, 0))
        else:
            if action == Action.FORWARD:
                old_location = copy.deepcopy(self.agent.location)
                self.agent.forward(self.grid_width, self.grid_height)
                death = (self.is_wumpus_at(self.agent.location) and self.is_wumpus_alive) or \
                    (self.is_pit_at(self.agent.location))
                self.agent.is_alive = not death
                environment = Environment(
                    grid_height=self.grid_height,
                    grid_width=self.grid_width,
                    allow_climb_without_gold=self.allow_climb_without_gold,
                    agent=self.agent,
                    pit_locations=self.pit_locations,
                    is_terminated=death,
                    wumpus_location=self.wumpus_location,
                    is_wumpus_alive=self.is_wumpus_alive,
                    gold_location= self.agent.location if self.agent.has_gold else self.gold_location
                )
                percept = Percept(environment.is_stench(), 
                                  environment.is_breeze(), 
                                  environment.is_glitter(), 
                                  old_location == self.agent.location, 
                                  False, 
                                  not self.agent.is_alive, 
                                  -1 if self.agent.is_alive else -1001)
            elif action == Action.TURN_LEFT:
                self.agent.turn_left()
                environment = Environment(
                    grid_height=self.grid_height,
                    grid_width=self.grid_width,
                    allow_climb_without_gold=self.allow_climb_without_gold,
                    agent=self.agent,
                    pit_locations=self.pit_locations,
                    is_terminated=self.is_terminated,
                    wumpus_location=self.wumpus_location,
                    is_wumpus_alive=self.is_wumpus_alive,
                    gold_location=self.gold_location
                )
                percept = Percept(environment.is_stench(), 
                                  environment.is_breeze(), 
                                  environment.is_glitter(), 
                                  False, 
                                  False, 
                                  False, 
                                  -1)
            elif action == Action.TURN_RIGHT:
                self.agent.turn_right()
                environment = Environment(
                    grid_height=self.grid_height,
                    grid_width=self.grid_width,
                    allow_climb_without_gold=self.allow_climb_without_gold,
                    agent=self.agent,
                    pit_locations=self.pit_locations,
                    is_terminated=self.is_terminated,
                    wumpus_location=self.wumpus_location,
                    is_wumpus_alive=self.is_wumpus_alive,
                    gold_location=self.gold_location
                )
                percept = Percept(environment.is_stench(), 
                                  environment.is_breeze(), 
                                  environment.is_glitter(), 
                                  False, 
                                  False, 
                                  False, 
                                  -1)
            elif action == Action.GRAB:
                self.agent.has_gold = self.is_glitter()
                environment = Environment(
                    grid_height=self.grid_height,
                    grid_width=self.grid_width,
                    allow_climb_without_gold=self.allow_climb_without_gold,
                    agent=self.agent,
                    pit_locations=self.pit_locations,
                    is_terminated=self.is_terminated,
                    wumpus_location=self.wumpus_location,
                    is_wumpus_alive=self.is_wumpus_alive,
                    gold_location=self.agent.location if self.agent.has_gold else self.gold_location
                )
                percept = Percept(environment.is_stench(), 
                                  environment.is_breeze(), 
                                  environment.is_glitter(), 
                                  False, 
                                  False, 
                                  False, 
                                  -1)
            elif action == Action.CLIMB:
                in_start_location = self.agent.location == Coordinate(0, 0)
                success = self.agent.has_gold and in_start_location
                is_terminated = success or (self.allow_climb_without_gold and in_start_location)
                environment = Environment(
                    grid_height=self.grid_height,
                    grid_width=self.grid_width,
                    allow_climb_without_gold=self.allow_climb_without_gold,
                    agent=self.agent,
                    pit_locations=self.pit_locations,
                    is_terminated=self.is_terminated,
                    wumpus_location=self.wumpus_location,
                    is_wumpus_alive=self.is_wumpus_alive,
                    gold_location=self.gold_location
                )
                percept = Percept(False, 
                                  False, 
                                  environment.is_glitter(), 
                                  False, 
                                  False, 
                                  is_terminated, 
                                  999 if success else -1)
            elif action == Action.SHOOT:
                had_arrow = self.agent.has_arrow
                wumpus_killed = self.kill_attempt_is_successful()
                self.agent.has_arrow = False
                environment = Environment(
                    grid_height=self.grid_height,
                    grid_width=self.grid_width,
                    allow_climb_without_gold=self.allow_climb_without_gold,
                    agent=self.agent,
                    pit_locations=self.pit_locations,
                    is_terminated=self.is_terminated,
                    wumpus_location=self.wumpus_location,
                    is_wumpus_alive=self.is_wumpus_alive and not wumpus_killed,
                    gold_location=self.gold_location
                )
                percept = Percept(self.is_stench(), 
                                  self.is_breeze(), 
                                  environment.is_glitter(), 
                                  False, 
                                  wumpus_killed, 
                                  False, 
                                  -11 if had_arrow else -1)
            
            return environment, percept
    
    def visualize(self):
        grid_str = ""

        wumpus_symbol = "W" if self.is_wumpus_alive else "w"

        for y in range(self.grid_height - 1, -1, -1):
            cells = []
            for x in range(0, self.grid_width):
                cell = ""
                coordinate = Coordinate(x, y)

                if self.is_agent_at(coordinate):
                    cell += "A"
                else:
                    cell += " "
                
                if self.is_pit_at(coordinate):
                    cell += "P"
                else:
                    cell += " "

                if self.is_gold_at(coordinate):
                    cell += "G"
                else:
                    cell += " "
                
                if self.is_wumpus_at(coordinate):
                    cell += wumpus_symbol
                else:
                    cell += " "
                
                cells.append(cell)
            
            row = "|".join(cells)

            grid_str += f"{row}\n"
        
        return grid_str
                

    