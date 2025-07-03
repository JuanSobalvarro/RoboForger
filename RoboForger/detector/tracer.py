from RoboForger.drawing.figures import Figure
from typing import Dict, List, Tuple, Any, Set
from RoboForger.types import Point3D


class Tracer:
    """
    Tracer builds traces
    """
    def __init__(self, figures: List[Figure]):
        self.figures = figures

        print(f"{len(figures)} figures inputted")

        self.graph = self.create_graph_from_figures(figures)
        # print(f"Graph adjacency list: {self.graph}")

        self.vtx_traces = self.find_traces(self.graph)

        amount_figures = 0
        for vtx_trace in self.vtx_traces:
            amount_figures += len(vtx_trace) - 1
        # print(f"In vtx traces detected draw of {amount_figures} figures")

        self.figure_traces = self.vtx_traces2fig_traces(self.vtx_traces, self.figures)

    @staticmethod
    def create_graph_from_figures(figures: List[Figure]):
        """
        Given a list of figures, create a graph represented as an adjacency list. The nodes are the vertices of the figures.
        """
        adjacency_list: Dict[Point3D, List[Point3D]] = {}

        for figure in figures:

            if not adjacency_list.get(figure.start_point):
                adjacency_list[figure.start_point] = []

            if not adjacency_list.get(figure.end_point):
                adjacency_list[figure.end_point] = []

            adjacency_list[figure.start_point].append(figure.end_point)
            adjacency_list[figure.end_point].append(figure.start_point)

        return adjacency_list

    @staticmethod
    def find_vtx_trace(vtx: Point3D, graph: Dict[Point3D, List[Point3D]], globally_visited: List[Point3D]) -> List[Point3D]:
        """
        Find the longest trace for a node (vertex) given a graph and a visited global set
        """
        longest_trace: List[Point3D] = [vtx]

        path: List[Tuple[Point3D, List[Point3D]]] = [(vtx, [n for n in graph[vtx] if n not in globally_visited])]

        while path:
            if len(path) > len(longest_trace):
                longest_trace = [p[0] for p in path]

            if not path[-1][1]:
                path.pop()
                continue

            next_node = path[-1][1].pop()
            next_adj = [adj for adj in graph[next_node] if adj not in globally_visited and adj not in [x[0] for x in path]]

            next_step = (next_node, next_adj)

            path.append(next_step)

        return longest_trace

    @staticmethod
    def find_traces(graph: Dict[Point3D, List[Point3D]]) -> List[List[Point3D]]:
        """
        Given a graph represented as an adjacency list, find the longest traces for each node
        """
        traces: List[List[Point3D]] = []
        visited: Set[Point3D] = set()

        # Optional: sort to start from nodes with few connections (leaf-first)
        figures = sorted(graph.keys(), key=lambda fig: len(graph[fig]))

        while len(visited) != len(figures):
            longest_trace = []

            for figure in figures:
                if figure in visited:
                    continue

                trace = Tracer.find_vtx_trace(figure, graph, visited)

                if len(trace) > len(longest_trace):
                    longest_trace = trace

            if longest_trace:
                traces.append(longest_trace)
                visited.update(longest_trace)

        return traces

    @staticmethod
    def vtx_traces2fig_traces(vtx_traces: List[List[Point3D]], figures: List[Figure]) -> List[List[Figure]]:
        """
        Convert vertex traces to figure traces based on the original figures.
        """
        figure_traces: List[List[Figure]] = []

        # Hash vtx to fig, for each fig hash their vtx to the fig
        vtx_fig_hash: Dict[Tuple[Point3D, Point3D], List[Figure]] = {}
        for fig in figures:
            if not vtx_fig_hash.get((fig.start_point, fig.end_point)):
                vtx_fig_hash[(fig.start_point, fig.end_point)] = []

            if not vtx_fig_hash.get((fig.end_point, fig.start_point)):
                vtx_fig_hash[(fig.end_point, fig.start_point)] = []

            vtx_fig_hash[(fig.start_point, fig.end_point)].append(fig)
            vtx_fig_hash[(fig.end_point, fig.start_point)].append(fig)

        for vtx_trace in vtx_traces:

            fig_trace: List[Figure] = []

            for i in range(len(vtx_trace) - 1):

                # Find the fig and pop it from the list so when access again will be another figure
                fig = vtx_fig_hash.get((vtx_trace[i], vtx_trace[i + 1])).pop()

                fig_trace.append(fig)

            if fig_trace:
                figure_traces.append(fig_trace)

        # TEMPORAL SOLUTION, if figure not in figure traces append it
        for fig in figures:
            in_trace = False
            for fig_trace in figure_traces:
                if fig in fig_trace:
                    in_trace = True
                    break

            if not in_trace:
                figure_traces.append([fig])

        return figure_traces
