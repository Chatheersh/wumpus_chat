import networkx as nx
from environment.coordinate import Coordinate

from environment.grid import Grid

def generate_graph(all_locations: Grid, safe_locations: Grid, width: int, height: int, start_location: Coordinate, final_location: Coordinate):
    
    graph = nx.Graph()

    for i in range(0, width):
        for j in range(0, height):
            if safe_locations.get_value(i, j) == 1:
                graph.add_node(all_locations.get_value(i, j))

                if i - 1 >= 0:
                    if safe_locations.get_value(i - 1, j) == 1:
                        graph.add_edge(all_locations.get_value(i, j), all_locations.get_value(i - 1, j))
                
                if i + 1 < width:
                    if safe_locations.get_value(i + 1, j) == 1:
                        graph.add_edge(all_locations.get_value(i, j), all_locations.get_value(i + 1, j))
                
                if j - 1 >= 0:
                    if safe_locations.get_value(i, j - 1) == 1:
                        graph.add_edge(all_locations.get_value(i, j), all_locations.get_value(i, j - 1))
                
                if j + 1 < height:
                    if safe_locations.get_value(i, j + 1) == 1:
                        graph.add_edge(all_locations.get_value(i, j), all_locations.get_value(i, j + 1))

    return nx.astar_path(graph, all_locations.get_value(start_location.x,start_location.y), all_locations.get_value(final_location.x,final_location.y))