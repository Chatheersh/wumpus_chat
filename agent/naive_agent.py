from random import random
import random
from agent.agent import Agent
from environment.action import Action
from environment.percept import Percept


class NaiveAgent(Agent):
    def next_action(self, percept: Percept) -> Action:
        return random.choice(list(Action))

