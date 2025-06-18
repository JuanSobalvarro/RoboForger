"""
Detector is a module that given some figures, it simplifies the points of those figures by unifying figures that are close to each other.
And giving a list of figures in an order that the draw can follow, so when drawing the design we ensure that any figure that is
continuous is drawn in one go, without lifting the tool.
"""
from collections import defaultdict
from typing import List, Dict, Any
from RoboForger.drawing.figures import Figure
from enum import Enum


class ConnectionType(Enum):
    END2START = "end2start"
    START2END = "start2end"
    START2START = "start2start"
    END2END = "end2end"
    DISCONNECTED = "disconnected"


class Detector:
    def __init__(self, figures: List[Figure]):
        """
        Initializes the Detector with a list of figures.

        :param figures: List of Figure objects to be processed.
        """
        self.figures = figures
        self.adjacency = self._build_adjacency(figures)
        # self.__print_adj()

    def __print_adj(self):

        print("===============Adjacency List================")
        for key, value in self.adjacency.items():
            print(f"{key.name}: {[v.name for v in value]}")

        print("=============================================")

    def _dfs(self) -> List[List[Figure]]:
        """
        Given the adjacency list of figures, this method will perform a Depth first search to return a list of the longest traces
        that can be drawn in one go. This method is iterative and will return a list of lists of figures that are connected.
        """
        adj_list: Dict[Figure, List[Figure]] = self.adjacency

        visited: set[Figure] = set()
        traces: List[List[Figure]] = []
        stack: List[Figure] = []

        # Iterate for each figure in the adjacency list since those are the root figures
        for figure in adj_list.keys():
            if figure in visited:
                continue

            visited.add(figure)

            stack.append(figure)
            trace: List[Figure] = []

            while stack:
                current_figure = stack.pop()
                trace.append(current_figure)

                for neighbor in adj_list[current_figure]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            if trace:
                traces.append(trace)

        return traces

    def detect(self) -> List[List[Figure]]:
        """
        Detects and simplifies figures based on proximity and continuity.

        :return: List of simplified Figure objects.
        """

        # FIRST: Figures ensure that every single one starts with the pre-down point and ends with the lifted point.
        # So detect the figures that are root figures (the ones that dont have a start point that is connected to the
        # end point of another figure)

        root_figures: List[Figure] = self.get_root_figures()

        print("Root figures detected:", root_figures)

        figures_traces: Dict[Figure, List[Figure]] = self.get_connections(root_figures)

        traces_detected: List[List[Figure]] = []

        for root_figure in root_figures:
            if root_figure not in figures_traces:
                raise ValueError(f"Figure {root_figure.name} has no traces detected.")

            trace = [root_figure]
            connected_figures = figures_traces[root_figure]

            while connected_figures:
                next_figure = connected_figures.pop(0)
                if next_figure not in trace:
                    trace.append(next_figure)
                    connected_figures.extend(figures_traces.get(next_figure, []))

            traces_detected.append(trace)

        return traces_detected

    def __print_traces(self, traces: List[List[Figure]]):
        """
        Prints the detected traces in a readable format.
        """
        print("================Detected traces=================")
        for i, trace in enumerate(traces):
            print(f"Trace {i + 1}: {[figure.name for figure in trace]}")
        print("================================================")

    def detect_and_simplify(self) -> List[Figure]:
        """
        This method detects the traces and then simplifies them into a list of figures that can be drawn in one go.
        Here we use the flags skip_pre_down and skip_end_lifting to determine if the figure should start with a pre-down point
        and end with a lifted point.
        """

        detected_traces = self._dfs()

        simplified_figures: List[Figure] = []

        self.__print_traces(detected_traces)

        for trace in detected_traces:
            if not trace:
                continue

            if len(trace) == 1:
                # If the trace has only one figure, we can add it directly to the simplified figures
                simplified_figures.append(trace[0])
                continue

            # root figure only needs to skip the end lifted point
            root_figure = trace[0]
            root_figure.set_skip_end_lifted(True)

            # end figure only needs to skip the pre down point
            end_figure = trace[-1]
            end_figure.set_skip_pre_down(True)

            for fig in trace[1:-1]:
                fig.set_skip_pre_down(True)
                fig.set_skip_end_lifted(True)

            simplified_figures.extend(trace)

        return simplified_figures

    def _build_adjacency(self, figures: List[Figure]) -> Dict[Figure, List[Figure]]:
        """
        Builds an adjacency list for the figures based on their connections.
        """
        adjacency: Dict[Figure, List[Figure]] = {}

        for i, figure in enumerate(figures):
            adjacency[figure] = []
            for j, other_figure in enumerate(figures):
                if i != j:
                    connection_type = self.is_connected(figure, other_figure)

                    # A figure 2 is considered a trace of figure 1 if it is connected to it from figure1 end to figure2 start
                    if connection_type == ConnectionType.END2START:
                        adjacency[figure].append(other_figure)

        return adjacency

    def _continuous_figures(self, figure: Figure) -> List[Figure]:
        """
        Finds all figures that are connected to the given figure.

        :param figure: The Figure object to check for connections.
        :return: List of connected Figure objects.
        """
        connected = []
        for fig in self.figures:
            if fig != figure and Detector.is_connected(figure, fig) == ConnectionType.END2START:
                connected.append(fig)
        return connected

    @staticmethod
    def is_connected(start_figure: Figure, end_figure: Figure) -> ConnectionType:

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
