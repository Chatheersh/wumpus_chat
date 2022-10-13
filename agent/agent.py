from abc import abstractmethod
from environment.action import Action
from environment.percept import Percept


class Agent:
    @abstractmethod
    def next_action(self, percept: Percept) -> Action:
        pass