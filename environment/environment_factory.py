import random
from environment.agent import Agent
from environment.coordinates import Coordinate
from environment.environment import Environment
from environment.percept import Percept


class EnvironmentFactory:
    def __init__(self):
        pass
    
    def _generate_random_location(self, grid_width, grid_length) -> Coordinate:
        x = random.randint(1, grid_width - 1)
        y = random.randint(1, grid_length - 1)

        return Coordinate(x, y)

    def _get_pit_locations(self, grid_width, grid_length, pit_probability):
        grid = []

        for x in range(1, grid_width):
            for y in range(1, grid_length):
                grid.append(Coordinate(x, y))

        return list(filter(lambda c: random.random() < pit_probability, grid))

    def create(self, grid_width: int, grid_length: int, pit_probability: float, allow_climb_without_gold: bool = False):

        pit_locations = self._get_pit_locations(grid_width, grid_length, pit_probability)
        
        environment = Environment(
            grid_width=grid_width,
            grid_height=grid_length,
            allow_climb_without_gold=allow_climb_without_gold,
            agent=Agent(),
            pit_locations=pit_locations,
            is_terminated=False,
            wumpus_location=self._generate_random_location(grid_width, grid_length),
            is_wumpus_alive=True,
            gold_location=self._generate_random_location(grid_width, grid_length)
        )

        percept = Percept(
            environment.is_stench,
            environment.is_breeze,
            False,
            False,
            False,
            False,
            0.0
        )

        return environment, percept
