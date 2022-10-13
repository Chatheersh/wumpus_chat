from enum import Enum


class Action(Enum):
    FORWARD = 0
    TURN_LEFT = 1
    TURN_RIGHT = 2
    SHOOT = 3
    GRAB = 4
    CLIMB = 5 

def get_str_rpr(action: Action):

    if action == Action.FORWARD:
        return "forward"
    elif action == Action.TURN_LEFT:
        return "turn left"
    elif action == Action.TURN_RIGHT:
        return "turn right"
    elif action == Action.SHOOT:
        return "shoot"
    elif action == Action.GRAB:
        return "grab"
    elif action == Action.CLIMB:
        return "climb"