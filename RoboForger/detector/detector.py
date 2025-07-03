"""
Detector is a module that given some figures, it simplifies the points of those figures by unifying figures that are close to each other.
And giving a list of figures in an order that the draw can follow, so when drawing the design we ensure that any figure that is
continuous is drawn in one go, without lifting the tool.
"""
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from RoboForger.drawing.figures import Figure
from .enums import ConnectionType
from .traces import is_figure_connected, print_graph, create_graph_from_figures, find_traces
from RoboForger.detector.tracer import Tracer


class Detector:
    def __init__(self, figures: List[Figure]):
        """
        Initializes the Detector with a list of figures.

        :param figures: List of Figure objects to be processed.
        """
        self.figures = figures
        # self.__print_adj()

        # print_graph(create_graph_from_figures(self.figures))

        tracer = Tracer(self.figures)

        self.traces = tracer.figure_traces

    @staticmethod
    def __print_traces(traces: List[List[Figure]]):
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
        and end with a lifted point. *** WORKING FINE DO NOT TOUCH
        """

        # detected_traces = self._dfs()
        detected_traces: List[List[Figure]] = self.traces

        self.__print_traces(detected_traces)

        simplified_figures: List[Figure] = []

        ensured_traces: List[List[Figure]] = []

        for i in range(len(detected_traces)):
            # print(f"Before ensuring continuity, trace: {detected_traces[i]}")
            trace = self.ensure_continuous(detected_traces[i])
            trace = self.ensure_continuity(trace)
            # print(f"Trace {trace}")
            ensured_traces.append(trace)
            # print(f"After ensuring continuity, trace: {trace}")

        for trace in ensured_traces:
            if not trace:
                continue
            # print(f"Trace {trace} has {len(trace)} figures")
            if len(trace) == 1:
                # If the trace has only one figure, we can add it directly to the simplified figures
                simplified_figures.extend(trace)
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

            # print(f"Trace {trace}")

            simplified_figures.extend(trace)
            # print(f"After extend: {simplified_figures} figures")

        # print("Simplified figures:", simplified_figures)

        print(f"Simplified figures detected in total: {len(simplified_figures)}")

        return simplified_figures

    @staticmethod
    def points_have_connection(fig1_points: Tuple, fig2_points: Tuple) -> bool:
        """
        This method checks if two figures have a connection based on their points.
        It returns True if the figures are connected, otherwise False.
        """
        return fig1_points[0] == fig2_points[0] or fig1_points[1] == fig2_points[1] or fig1_points[0] == fig2_points[1] or fig1_points[1] == fig2_points[0]

    @staticmethod
    def ensure_continuous(trace: List[Figure]) -> List[Figure]:
        """
        This method ensures that a given trace is continuous(the figures can be connected in a way that they can be drawn without lifting the tool).
        """

        for i in range(len(trace) - 1):

            if not Detector.points_have_connection(trace[i].get_start_and_end_points(), trace[i + 1].get_start_and_end_points()):
                raise ValueError(f"!!!!!!!!!!!!!{trace[i].name} and {trace[i + 1].name} are not connected")

        return trace

    @staticmethod
    def ensure_continuity(trace: List[Figure]) -> List[Figure]:
        """
        This method ensures that given a trace, it reverse the points of the figures that
        are not aligned with the previous figure. The correct direction should work like:

        - fig n endpoint == fig n+1 start point
        """
        if not trace:
            raise ValueError("The list of figures is empty.")

        if len(trace) == 1:
            # If there is only one figure, we can return it directly
            return trace

        continuous_trace: List[Figure] = trace

        # Ensure that the shared point of first figure's and second figure is at the end and start point respectively.
        if continuous_trace[0].end_point == continuous_trace[1].end_point:
            continuous_trace[1].reverse_points()
        elif continuous_trace[0].start_point == continuous_trace[1].start_point:
            continuous_trace[0].reverse_points()
        elif continuous_trace[0].start_point == continuous_trace[1].end_point:
            continuous_trace[0].reverse_points()
            continuous_trace[1].reverse_points()

        # if continuous_trace[0].end_point != continuous_trace[1].start_point:
        #     print(f"First figure {continuous_trace[0].name} and second figure {continuous_trace[1].name} couldnt be aalign you are trsh")

        for i in range(len(continuous_trace) - 1):

            # if continuous_trace[i].end_point != continuous_trace[i + 1].start_point:
            #     print(f"Figures {continuous_trace[i].name} and {continuous_trace[i + 1].name} are not connected properly before ensuring continuity.")
            #     print(f"{continuous_trace[i].name} with points: {continuous_trace[i].get_start_and_end_points()}")
            #     print(f"{continuous_trace[i + 1].name} with points: {continuous_trace[i + 1].get_start_and_end_points()}")

            if continuous_trace[i].end_point != continuous_trace[i + 1].start_point:
                continuous_trace[i + 1].reverse_points()

            # if continuous_trace[i].end_point != continuous_trace[i + 1].start_point:
            #     print(f"Figures {continuous_trace[i].name} and {continuous_trace[i + 1].name} are not connected properly after ensuring continuity.")
            #     print(f"{continuous_trace[i].name} with points: {continuous_trace[i].get_start_and_end_points()}")
            #     print(f"{continuous_trace[i + 1].name} with points: {continuous_trace[i + 1].get_start_and_end_points()}")


        return continuous_trace

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
