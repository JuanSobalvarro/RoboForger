"""
Detector is a module that given some figures, it simplifies the points of those figures by unifying figures that are close to each other.
And giving a list of figures in an order that the draw can follow, so when drawing the design we ensure that any figure that is
continuous is drawn in one go, without lifting the tool.
"""
from typing import List, Dict, Any, Tuple
from RoboForger.drawing.figures import Figure
from RoboForger.detector.tracer import Tracer


class Detector:
    def __init__(self, figures: List[Figure]):
        """
        Initializes the Detector with a list of figures.

        :param figures: List of Figure objects to be processed.
        """
        self.figures = figures

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

        detected_traces: List[List[Figure]] = self.traces

        self.__print_traces(detected_traces)

        simplified_figures: List[Figure] = []

        ensured_traces: List[List[Figure]] = []

        for i in range(len(detected_traces)):
            trace = self.ensure_continuity(detected_traces[i])
            ensured_traces.append(trace)

        for trace in ensured_traces:
            if not trace:
                continue

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

            simplified_figures.extend(trace)

        print(f"Simplified figures detected in total: {len(simplified_figures)}")

        return simplified_figures

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

        for i in range(len(continuous_trace) - 1):

            if continuous_trace[i].end_point != continuous_trace[i + 1].start_point:
                continuous_trace[i + 1].reverse_points()


        return continuous_trace
