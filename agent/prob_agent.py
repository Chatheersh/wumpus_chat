from argparse import Action
from typing import List, Set
from agent.beeline_agent import BeelineAgent
from environment.agent_state import AgentState
from environment.coordinate import Coordinate
from pomegranate import BayesianNetwork

class ProbAgent(BeelineAgent):
    def __init__(self, grid_width, grid_height, 
                       agent_state: AgentState, 
                       safe_locations: Set[Coordinate], 
                       beeline_action_list: List[Action],
                       stench_locations: Set[Coordinate],
                       breeze_locations: Set[Coordinate],
                       head_scream: bool,
                       wumpus_probability_model: BayesianNetwork,
                       pit_probability_model: BayesianNetwork):
        super().__init__(grid_width, grid_height, agent_state, safe_locations, beeline_action_list)

        self.stench_locations = stench_locations
        self.breeze_locations = breeze_locations
        self.heard_scream = head_scream

        self.wumpus_probability_model = wumpus_probability_model
        self.pit_probability_model = pit_probability_model

    
    
