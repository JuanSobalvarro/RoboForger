"""
Detector is a module that given some figures, it simplifies the points of those figures by unifying figures that are close to each other.
And giving a list of figures in an order that the draw can follow, so when drawing the design we ensure that any figure that is
continuous is drawn in one go, without lifting the tool.
"""
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from RoboForger.drawing.figures import Figure
from .enums import ConnectionType
from .dfs import is_figure_connected, print_graph, create_graph_from_figures, find_traces


class Detector:
    def __init__(self, figures: List[Figure]):
        """
        Initializes the Detector with a list of figures.

        :param figures: List of Figure objects to be processed.
        """
        self.figures = figures
        # self.__print_adj()

        # print_graph(create_graph_from_figures(self.figures))

        self.traces = find_traces(create_graph_from_figures(self.figures))

    def __print_adj(self):

        print("===============Adjacency List================")
        for key, value in self.adjacency.items():
            print(f"{key.name}: {[v.name for v in value]}")

        print("=============================================")

    @staticmethod
    def __print_traces(traces: List[List[Figure]]):
        """
        Prints the detected traces in a readable format.
        """
        print("================Detected traces=================")
        for i, trace in enumerate(traces):
            print(f"Trace {i + 1}: {[figure.name for figure in trace]}")
        print("================================================")

    def find_traces(self, graph: Dict[Figure, List[Tuple[Figure, ConnectionType]]]) -> List[List[Tuple[Figure, bool]]]:
        visited = set()
        traces = []

        for figure in graph.keys():
            if figure in visited:
                continue
            trace = []
            stack = [(figure, None, False)]  # (current, parent, reversed_flag)
            visited.add(figure)

            while stack:
                current, parent, reversed_flag = stack.pop()
                trace.append((current, reversed_flag))

                for neighbor, conn_type in graph[current]:
                    if neighbor in visited:
                        continue

                    # Determine if reversal is needed
                    should_reverse = conn_type in {
                        ConnectionType.START2END,
                        ConnectionType.END2END,
                        ConnectionType.START2START
                    }
                    stack.append((neighbor, current, should_reverse))
                    visited.add(neighbor)

            traces.append(trace)

        return traces

    @staticmethod
    def check_aligned_end2start(figures: List[Figure]) -> bool:
        """
        Checks if all figures are aligned in the same direction.
        This is useful to ensure that the figures can be drawn in one go without lifting the tool.
        """
        if not figures:
            return True

        last_figure = figures[0]

        for next_figure in figures[1:]:
            if last_figure.end_point != next_figure.start_point:
                print(f"Figures {last_figure.name} and {next_figure.name} are not aligned end to start.")
                return False
            last_figure = next_figure

        return True

    @staticmethod
    def check_aligned_start2end(figures: List[Figure]) -> bool:
        """
        Checks if all figures are aligned in the same direction.
        This is useful to ensure that the figures can be drawn in one go without lifting the tool.
        """
        if not figures:
            return True

        first_figure = figures[0]

        for next_figure in figures[1:]:
            if first_figure._points[0] != next_figure._points[-1]:
                return False
            first_figure = next_figure

        return True

    def _dfs(self) -> List[List[Figure]]:
        """
        Given the adjacency list of figures, this method will perform a Depth first search to return a list of the longest traces
        that can be drawn in one go. This method is iterative and will return a list of lists of figures that are connected. WORKING FINE DO NOT TOUCH
        """
        adj_list: Dict[Figure, List[Figure]] = self._build_adjacency(self.figures)

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

    def detect_and_simplify(self) -> List[Figure]:
        """
        This method detects the traces and then simplifies them into a list of figures that can be drawn in one go.
        Here we use the flags skip_pre_down and skip_end_lifting to determine if the figure should start with a pre-down point
        and end with a lifted point. *** WORKING FINE DO NOT TOUCH
        """

        # detected_traces = self._dfs()
        detected_traces: List[List[Figure]] = self.traces

        # self.__print_traces(detected_traces)

        simplified_figures: List[Figure] = []

        checked_traces = []
        for trace in detected_traces:
            # print("Ensuring continuity for trace", i + 1)
            # print(f"{detected_traces[i]}")
            continuous_traces = self.ensure_continuity(trace)
            checked_traces.extend(continuous_traces)

        for trace in checked_traces:
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

    @staticmethod
    def ensure_continuity(trace: List[Figure]) -> List[List[Figure]]:
        """
        This method ensures that given a trace, it reverse the points of the figures that
        are not aligned with the previous figure or SPLITS the trace if the figures are not continuous.
        """
        if not trace:
            raise ValueError("The list of figures is empty.")

        # print("Pre ensuring continuity of figures:")
        # for fig in figures:
        #     print(f"{fig.name}: {fig.get_start_and_end_points()}")

        if len(trace) == 1:
            # If there is only one figure, we can return it directly
            return [trace]

        continuous_traces: List[List[Figure]] = []
        current_trace: List[Figure] = [trace[0]]

        # Adjust first figure if necessary based on the second
        first_fig = trace[0]
        second_fig = trace[1]
        first_start, first_end = first_fig.get_start_and_end_points()
        second_start, second_end = second_fig.get_start_and_end_points()

        # If the *end* of the first doesnt connect to the *start* of the second, reverse it
        if first_end != second_start and first_end != second_end:
            if first_start == second_start or first_start == second_end:
                first_fig.reverse_points()

        last_fig = first_fig

        for next_fig in trace[1:]:
            next_start, next_end = next_fig.get_start_and_end_points()
            last_end = last_fig.get_start_and_end_points()[1]

            # Reverse next figure if needed
            if last_end == next_end:
                next_fig.reverse_points()
                next_start, next_end = next_fig.get_start_and_end_points()

            # If *still* not continuous start a new trace
            if last_end != next_start:
                continuous_traces.append(current_trace)
                current_trace = [next_fig]
            else:
                current_trace.append(next_fig)

            last_fig = next_fig

            # Append the last trace
        if current_trace:
            continuous_traces.append(current_trace)

        return continuous_traces

    def _build_adjacency(self, figures: List[Figure]) -> Dict[Figure, List[Figure]]:
        """
        Builds an adjacency list for the figures based on their connections.
        """
        adjacency: Dict[Figure, List[Figure]] = {}

        for i, figure in enumerate(figures):
            adjacency[figure] = []
            for j, other_figure in enumerate(figures):
                if i != j:
                    if self.__is_trace(figure, other_figure):
                        adjacency[figure].append(other_figure)

        return adjacency

    def __is_trace(self, figure1, figure2):
        """
        This method defines if figure2 is a trace of figure1. This will define how we interpret the figures when drawing them.
        """
        connection_type = is_figure_connected(figure1, figure2)

        is_trace = connection_type == ConnectionType.END2START or connection_type == ConnectionType.END2END

        return is_trace

    def _continuous_figures(self, figure: Figure) -> List[Figure]:
        """
        Finds all figures that are connected to the given figure.

        :param figure: The Figure object to check for connections.
        :return: List of connected Figure objects.
        """
        connected = []
        for fig in self.figures:
            if fig != figure and is_figure_connected(figure, fig) == ConnectionType.END2START:
                connected.append(fig)
        return connected
