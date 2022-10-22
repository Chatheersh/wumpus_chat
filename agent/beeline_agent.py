from random import random
import random
from agent.agent import Agent
from environment.action import Action
from environment.agent_state import AgentState
from environment.coordinates import Coordinate
from environment.percept import Percept


class BeelineAgent(Agent):

    def __init__(self, agent_state: AgentState):
        self.agent_state = agent_state
    
    def next_action(self, percept: Percept) -> Action:

        if self.agent_state.has_gold and self.agent_state.location.is_equal(Coordinate(0, 0)):
            return Action.CLIMB
        elif percept.glitter:
            self.agent_state.has_gold = True
            return Action.GRAB
        else:
            return random.choice([Action.FORWARD, Action.TURN_LEFT, Action.TURN_RIGHT, Action.SHOOT])