from pomegranate import *

class WumpusModelFactory:

    def __init__(self):
        pass

    def _create_wumpus_dict(self, width, height):

        wumpus_prob_dict = {}

        for i in range(0, width):
            for j in range(0, height):
                wumpus_prob_dict[f"{i},{j}"] = 1./15

        return wumpus_prob_dict

    def _is_adjacent(self, x_1, y_1, x_2, y_2):
        if x_1 == x_2 and abs(y_1 - y_2) == 1:
            return True
        elif y_1 == y_2 and abs(x_1 - x_2) == 1:
            return True
        else:
            return False

    def _create_stench_list(self, x, y, width, height):
        stench_list = []
        for i in range(0, width):
            for j in range(0, height):
                if i == 0 and j == 0:
                    continue
                elif self._is_adjacent(i, j, x, y):
                    stench_list.append([f"{i},{j}", True, 1.0])
                    stench_list.append([f"{i},{j}", False, 0.0])
                else:
                    stench_list.append([f"{i},{j}", True, 0.0])
                    stench_list.append([f"{i},{j}", False, 1.0])
        return stench_list

    def create_model(self, width, height):

        wumpus_prob_dict = self._create_wumpus_dict(width, height)

        # no wumpus at 1,1
        wumpus_prob_dict.pop("0,0")

        wumpus = DiscreteDistribution(wumpus_prob_dict)

        nodes = {}
        for i in range(0, width):
            for j in range(0, height):
                nodes[f"{i},{j}"] = Node(ConditionalProbabilityTable(
                    self._create_stench_list(i, j, width, height), [wumpus]), name=f"{i},{j}")

        wumpus_node = Node(wumpus, name="wumpus")

        model = BayesianNetwork("Wumpus")

        model.add_state(wumpus_node)

        for i in range(0, width):
            for j in range(0, height):
                model.add_state(nodes[f"{i},{j}"])
                model.add_edge(wumpus_node, nodes[f"{i},{j}"])

        model.bake()

        return model
