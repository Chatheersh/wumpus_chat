from environment.coordinates import Coordinate
from environment.orientation import Orientation


class Agent:
    def __init__(self, location: Coordinate = Coordinate(0, 0),
                       orientation: Orientation = Orientation.EAST, 
                       has_gold: bool = False,
                       has_arrow: bool = False,
                       is_alive: bool = False):
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