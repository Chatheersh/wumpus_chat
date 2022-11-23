
from agent.agent import Agent
from agent.beeline_agent import BeelineAgent
from agent.naive_agent import NaiveAgent
from agent.prob_agent import ProbAgent
from environment.action import get_str_rpr
from environment.agent_state import AgentState
from environment.coordinate import Coordinate
from environment.environment import Environment
from environment.environment_factory import EnvironmentFactory
from environment.percept import Percept
from environment.pit_model_factory import PitModelFactory
from environment.wumpus_model_factory import WumpusModelFactory


def run_episode(environment: Environment, agent: Agent, percept: Percept) -> float:
    next_action = agent.next_action(percept)
    print(f"Action: {get_str_rpr(next_action)}")

    next_environment, next_percept = environment.apply_action(next_action)

    print(next_environment.visualize())
    print(next_percept.show())

    return next_percept.reward + (run_episode(next_environment, agent, next_percept) if not next_percept.is_terminated else 0.0)

def main():
    width = 4
    height = 4
    environment, percept = EnvironmentFactory().create(width, height, 0.2, False)

    safe_locations = set()
    safe_locations.add(Coordinate(0, 0))

    w_model = WumpusModelFactory().create_model(width, height)
    p_model = PitModelFactory().generate_model(width, height)

    agent = ProbAgent(4, 4, AgentState(), safe_locations, [], [], [], False, w_model, p_model)
    total_reward = run_episode(environment, agent, percept)
    print(f"Total reward {total_reward}")

if __name__ == "__main__":
    main()

