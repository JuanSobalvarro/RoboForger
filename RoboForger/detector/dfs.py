"""
In this module we define the DFS class that is used to perform a depth-first search on a graph of figures.

The logic is that:
1. We need to find the leaf nodes, figures that are not connected to any other figures or has the least amount of connections.
** The connections to a figure should be interpreted from the end point of the figure, since we want to draw from the start and then at the end we need to continue drawing
"""
from typing import List, Dict, Tuple

from RoboForger.drawing.figures import Figure
from .enums import ConnectionType

def is_figure_connected(start_figure: Figure, end_figure: Figure) -> ConnectionType:
    start_figure_points = start_figure.get_points()
    end_figure_points = end_figure.get_points()

    if start_figure_points[-1] == end_figure_points[0]:
        return ConnectionType.END2START

    if start_figure_points[0] == end_figure_points[-1]:
        return ConnectionType.START2END

    if start_figure_points[0] == end_figure_points[0]:
        return ConnectionType.START2START

    if start_figure_points[-1] == end_figure_points[-1]:
        return ConnectionType.END2END

    return ConnectionType.DISCONNECTED

def create_graph_from_figures(figures: List[Figure]) -> Dict[Figure, List[Figure]]:
    """
    Given a list of figures, create a graph represented as an adjacency list.
    """
    graph: Dict[Figure, List[Figure]] = {}

    for figure in figures:
        graph[figure] = []

        for other_figure in figures:

            if figure == other_figure:
                continue

            connection_type = is_figure_connected(figure, other_figure)

            # In reality we just care if the next figure is connected at the end or at the start of the current figure
            if connection_type != ConnectionType.DISCONNECTED:
                graph[figure].append(other_figure)

    return graph

def print_graph(graph: Dict[Figure, List[Tuple[Figure, ConnectionType]]]):
    """
    Print the graph in a readable format.
    """
    print("===============Graph Adjacency List================")
    for figure, neighbors in graph.items():
        print(f"Figure {figure.name} has {len(neighbors)} neighbors:")

        for n in neighbors:
            neighbor, conn_type = n
            print(f"  - {neighbor.name} with connection type {conn_type.name}")

    print("====================================================")


def find_traces(graph: Dict[Figure, List[Figure]]) -> List[List[Figure]]:
    """
    Find traces in the graph using depth-first search (DFS).
    """

    visited = set()
    traces = []

    # Sort nodes by the number of connections (ascending order) so that the most likely to be root nodes are the ones with less connections
    nodes_sorted = sorted(graph.keys(), key=lambda x: len(graph[x]))

    for figure in nodes_sorted:
        if figure in visited:
            continue

        trace = []
        stack = [figure]

        while stack:
            current = stack.pop()

            # If the current figure has already been visited, we skip it
            if current in visited:
                continue

            visited.add(current)
            trace.append(current)

            # Sort neighbors by the number of connections (ascending order) so we follow first the neighbors that are
            # most likely to dont have too many connections (traces)
            neighbors = sorted(graph[current], key=lambda x: len(graph[x]))

            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append(neighbor)

        # If we have a trace, we add it to the list of traces
        if trace:
            traces.append(trace)

    return traces