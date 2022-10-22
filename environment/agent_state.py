from environment.action import Action
from environment.coordinates import Coordinate
from environment.orientation import Orientation


class AgentState:
    def __init__(self, location: Coordinate = Coordinate(0, 0), orientation: Orientation = Orientation.EAST, has_gold : bool = False, has_arrow: bool = True, is_alive: bool = True):
        self.location = location
        self.orientation = orientation
        self.has_gold = has_gold
        self.has_arrow = has_arrow
        self.is_alive = is_alive

    def turn_left(self):
        if self.orientation == Orientation.EAST:
            self.orientation = Orientation.NORTH
        elif self.orientation == Orientation.NORTH:
            self.orientation = Orientation.WEST
        elif self.orientation == Orientation.WEST:
            self.orientation = Orientation.SOUTH
        elif self.orientation == Orientation.SOUTH:
            self.orientation = Orientation.EAST

    def turn_right(self):
        if self.orientation == Orientation.EAST:
            self.orientation = Orientation.SOUTH
        elif self.orientation == Orientation.SOUTH:
            self.orientation = Orientation.WEST
        elif self.orientation == Orientation.WEST:
            self.orientation = Orientation.NORTH
        elif self.orientation == Orientation.NORTH:
            self.orientation = Orientation.EAST

    def forward(self, grid_width: int, grid_height: int):
        if self.orientation == Orientation.WEST:
            self.location = Coordinate(max(0, self.location.x - 1), self.location.y)
        if self.orientation == Orientation.EAST:
            self.location = Coordinate(min(grid_width - 1, self.location.x + 1), self.location.y)
        elif self.orientation == Orientation.SOUTH:
            self.location = Coordinate(self.location.x, max(0, self.location.y - 1))
        elif self.orientation == Orientation.NORTH:
            self.location = Coordinate(self.location.x, min(grid_height - 1, self.location.y + 1))
    
    def use_arrow(self):
        self.has_arrow = False

    def apply_move_action(self, action: Action, grid_width: int, grid_height: int):

        if action == Action.TURN_LEFT:
            self.turn_left()
        elif action == Action.TURN_RIGHT:
            self.turn_right()
        elif action == Action.FORWARD:
            self.forward(grid_width, grid_height)
    
    def show(self):
        return f"location: {self.location} orientation: {self.orientation} has_gold: {self.orientation} has_arrow: {self.has_arrow} is_alive: {self.is_alive}"