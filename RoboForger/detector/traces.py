"""
In this module we define the DFS class that is used to perform a breadth first search on a graph of figures.

The logic is that:
1. We need to find the leaf nodes, figures that are not connected to any other figures or has the least amount of connections.
** The connections to a figure should be interpreted from the end point of the figure, since we want to draw from the start and then at the end we need to continue drawing
"""
from typing import List, Dict, Tuple, Set

from RoboForger.drawing.figures import Figure
from .enums import ConnectionType


def is_figure_connected(start_figure: Figure, end_figure: Figure) -> ConnectionType:

    if start_figure.end_point == end_figure.start_point:
        return ConnectionType.END2START

    if start_figure.start_point == end_figure.end_point:
        return ConnectionType.START2END

    if start_figure.start_point == end_figure.start_point:
        return ConnectionType.START2START

    if start_figure.end_point == end_figure.end_point:
        return ConnectionType.END2END

    # print(f"Figure {start_figure.name} with points: {start_figure.start_point}|{start_figure.end_point} is not connected "
    #       f"to figure {end_figure.name} with points: {end_figure.start_point}|{end_figure.end_point}.")
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
            # if connection_type != ConnectionType.DISCONNECTED:
            #     graph[figure].append(other_figure)

            if connection_type == ConnectionType.START2END or connection_type == ConnectionType.END2START:
                graph[figure].append(other_figure)


        # print(f"Figure {figure.name} has {len(graph[figure])} connections.")

    return graph

def print_graph(graph: Dict[Figure, List[Figure]]) -> None:
    """
    Print the graph in a readable format.
    """
    print("===============Graph Adjacency List================")
    for figure, neighbors in graph.items():
        print(f"Figure {figure.name} has {len(neighbors)} neighbors:")

        for n in neighbors:
            neighbor = n
            print(f"  - {neighbor.name} with connection type {is_figure_connected(figure, neighbor).name}")

    print("====================================================")

def trace_for_figure(
    figure: Figure,
    graph: Dict[Figure, List[Figure]],
    globally_visited: Set[Figure]
) -> List[Figure]:
    """
    Perform DFS with backtracking to find the longest trace starting from `figure`,
    avoiding already globally visited nodes.
    """
    longest_trace: List[Figure] = [figure]

    # Path is a list of tuples that contains a figure and its possible next figuresm (adjacency)
    path: List[Tuple[Figure, List[Figure]]] = [(figure, [n for n in graph[figure] if n not in globally_visited])]

    while path:
        # Check if the current path is longer than the longest trace found so far
        if len(path) > len(longest_trace):
            longest_trace = [p[0] for p in path]

        if not path[-1][1]:
            path.pop()
            continue

        # If everything is right just add the next step in path
        next_node = path[-1][1].pop()
        next_adj = [adj for adj in graph[next_node] if adj not in globally_visited and adj not in [p[0] for p in path]]

        next_step = (next_node, next_adj)

        path.append(next_step)

    return longest_trace

def find_traces(graph: Dict[Figure, List[Figure]]) -> List[List[Figure]]:
    """
    Find all longest non-overlapping traces in the graph.
    Each trace is a sequence of figures that can be drawn sequentially.
    """
    traces: List[List[Figure]] = []
    visited: Set[Figure] = set()

    # Optional: sort to start from nodes with few connections (leaf-first)
    figures = sorted(graph.keys(), key=lambda fig: len(graph[fig]))

    for figure in figures:
        if figure in visited:
            continue

        trace = trace_for_figure(figure, graph, visited)
        if trace:
            traces.append(trace)
            visited.update(trace)

    return traces