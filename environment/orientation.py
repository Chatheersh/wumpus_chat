from enum import Enum


class Orientation(Enum):
    EAST = 0
    WEST = 1
    SOUTH = 2
    NORTH = 3

    @staticmethod
    def turn_left(orientation):
        if orientation == Orientation.EAST:
            orientation = Orientation.NORTH
        elif orientation == Orientation.NORTH:
            orientation = Orientation.WEST
        elif orientation == Orientation.WEST:
            orientation = Orientation.SOUTH
        elif orientation == Orientation.SOUTH:
            orientation = Orientation.EAST
        
        return orientation

    @staticmethod
    def turn_right(orientation):
        if orientation == Orientation.EAST:
            orientation = Orientation.SOUTH
        elif orientation == Orientation.SOUTH:
            orientation = Orientation.WEST
        elif orientation == Orientation.WEST:
            orientation = Orientation.NORTH
        elif orientation == Orientation.NORTH:
            orientation = Orientation.EAST
        
        return orientation