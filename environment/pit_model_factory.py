from pomegranate import *

class PitModelFactory:

    def __init__(self):
        self._table_2 = self.generate_table_with_two_pits()
        self._table_3 = self.generate_table_with_three_pits()
        self._table_4 = self.generate_table_with_four_pits()

    def generate_table_with_two_pits(self):
        table = []
        for a in [True, False]:
            for b in [True, False]:
                table.append([a, b, a or b, 1.0])
                table.append([a, b, not (a or b), 0.0])
        return table

    def generate_table_with_three_pits(self):
        table = []
        for a in [True, False]:
            for b in [True, False]:
                for c in [True, False]:
                    table.append([a, b, c, a or b or c, 1.0])
                    table.append([a, b, c, not (a or b or c), 0.0])
        return table

    def generate_table_with_four_pits(self):
        table = []
        for a in [True, False]:
            for b in [True, False]:
                for c in [True, False]:
                    for d in [True, False]:
                        table.append([a, b, c, d, a or b or c or d, 1.0])
                        table.append([a, b, c, d, not (a or b or c or d), 0.0])
        return table

    def find_neighbours(self, x, y, width, height):

        neighbours = []
        
        if x - 1 >= 0:
            neighbours.append(f"{x-1},{y}")
        
        if x + 1 < width:
            neighbours.append(f"{x+1},{y}")

        if y - 1 >= 0:
            neighbours.append(f"{x},{y-1}")

        if y + 1 < height:
            neighbours.append(f"{x},{y+1}")

        # a pit cannot exist in origin
        if "0,0" in neighbours:
            neighbours.remove("0,0")

        return neighbours
    
    def generate_model(self, width, height):
        pits_dd_dict = {}
        pits_nodes_dict = {}
        pit_indexes = {}

        model = BayesianNetwork("Pit")

        index = 0

        for i in range(0, width):
            for j in range(0, height):
                if i == 0 and j == 0:
                    continue
                else:
                    d = DiscreteDistribution({True: 0.2, False: 0.8})
                    s = Node(d, name=f"pit_{i}_{j}")
                    model.add_state(s)
                    pits_dd_dict[f"{i},{j}"] = d
                    pits_nodes_dict[f"{i},{j}"] = s
                    pit_indexes[f"{i},{j}"] = index
                    index += 1

        for i in range(0, width):
            for j in range(0, height):
                neighbours_list = self.find_neighbours(i, j, width, height)
                
                table = []
                if len(neighbours_list) == 2:
                    table = self._table_2
                elif len(neighbours_list) == 3:
                    table = self._table_3
                elif len(neighbours_list) == 4:
                    table = self._table_4

                neighbour_pits = [value for key, value in pits_dd_dict.items() if key in neighbours_list]
                c = ConditionalProbabilityTable(table, neighbour_pits)
                s = Node(c, name=f"breeze_{i}_{j}")
                model.add_state(s)

                for neighbour in neighbours_list:
                    model.add_edge(pits_nodes_dict[neighbour], s)

        model.bake()
        return pit_indexes, model
    