"""
This module creates a Draw class that is used to generate the Rapid Code given a CAD file.
"""
from typing import Tuple
from RoboForger.types import Point3D, RawLine, RawArc, RawCircle, RawSpline
from RoboForger.drawing.figures import PolyLine, Arc, Circle, BSpline
from RoboForger.preprocessing.cad_parser import CADParser
from RoboForger.preprocessing.converter import Converter
from RoboForger.drawing.draw import Draw


class Forger:
    """
    The forger class generalize the utilization of roboforger in 4 steps:
    - File Parsing: Takes a DXF file and parses the figures it founds
    - Convertion: Converts the parsed figures into the figures forger understand (python objects)
    - Drawing detection: Logic for drawing, order of figures and maybe intelligent tracing
    - Code Generation: Translate traces and points into RAPID code
    """
    def __init__(self, 
        origin: Point3D = (450.0, 0, 450.0),
        zero: Point3D = (0.0, 0.0, 0.0),
        pre_scale: float = 1.0,
        float_precision: int = 4,
        lifting: float = 50.0,
        tool_name: str = "tool0",
        global_velocity: int = 1000,
        polyline_velocity: int = 1000,
        arc_velocity: int = 1000,
        circle_velocity: int = 1000,
        spline_velocity: int = 1000,
        workspace_limits: Tuple[Point3D, Point3D] = ((-100, -700, -100), (800, 700, 800)),
        use_intelligent_traces: bool = True,
        use_offset_programming: bool = True
        ):

        self._origin = origin
        self._zero = zero
        self._pre_scale = pre_scale
        self._float_precision = float_precision
        self._lifting = lifting
        self._tool_name = tool_name
        self._global_velocity = global_velocity
        self._polyline_velocity = polyline_velocity
        self._arc_velocity = arc_velocity
        self._circle_velocity = circle_velocity
        self._spline_velocity = spline_velocity
        self._workspace_limits = workspace_limits
        self._use_intelligent_traces = use_intelligent_traces
        self._use_offset_programming = use_offset_programming

        self._raw_lines: list[RawLine] = []
        self._raw_arcs: list[RawArc] = []
        self._raw_circles: list[RawCircle] = []
        self._raw_splines: list[RawSpline] = []

        self._polylines: list[PolyLine] = []
        self._arcs: list[Arc] = []
        self._circles: list[Circle] = []
        self._splines: list[BSpline] = []

        self._rapid_code: str = ""


    def get_origin(self) -> Point3D:
        return self._origin

    def get_zero(self) -> Point3D:
        return self._zero

    def get_scale(self) -> float:
        return self._pre_scale

    def get_float_precision(self) -> int:
        return self._float_precision

    def get_lifting(self) -> float:
        return self._lifting

    def get_tool_name(self) -> str:
        return self._tool_name

    def get_global_velocity(self) -> float:
        return self._global_velocity

    def get_workspace_limits(self) -> Tuple[Point3D, Point3D]:
        return self._workspace_limits

    def get_use_intelligent_traces(self) -> bool:
        return self._use_intelligent_traces

    def get_use_offset_programming(self) -> bool:
        return self._use_offset_programming

    def set_origin(self, origin: Point3D) -> None:
        self._origin = origin

    def set_zero(self, zero: Point3D) -> None:
        self._zero = zero

    def set_scale(self, scale: float) -> None:
        self._pre_scale = scale

    def set_float_precision(self, float_precision: int) -> None:
        self._float_precision = float_precision

    def set_lifting(self, lifting: float) -> None:
        self._lifting = lifting

    def set_tool_name(self, tool_name: str) -> None:
        self._tool_name = tool_name

    def set_global_velocity(self, global_velocity: float) -> None:
        self._global_velocity = global_velocity

    def set_workspace_limits(self, workspace_limits: Tuple[Point3D, Point3D]) -> None:
        self._workspace_limits = workspace_limits

    def set_use_intelligent_traces(self, use_intelligent_traces: bool) -> None:
        self._use_intelligent_traces = use_intelligent_traces

    def set_use_offset_programming(self, use_offset_programming: bool) -> None:
        self._use_offset_programming = use_offset_programming

    def reset_default(self):
        self._origin = (450.0, 0, 450.0)
        self._zero = (0.0, 0.0, 0.0)
        self._pre_scale = 1.0
        self._float_precision = 4
        self._lifting = 50.0
        self._tool_name = "tool0"
        self._global_velocity = 1000.0
        self._workspace_limits = ((-810, -810, 0), (810, 810, 800))
        self._use_intelligent_traces = True
        self._use_offset_programming = True

    def get_raw_lines(self) -> list[RawLine]:
        return self._raw_lines

    def get_raw_arcs(self) -> list[RawArc]:
        return self._raw_arcs

    def get_raw_circles(self) -> list[RawCircle]:
        return self._raw_circles

    def get_raw_splines(self) -> list[RawSpline]:
        return self._raw_splines

    def get_polylines(self) -> list[PolyLine]:
        return self._polylines

    def get_arcs(self) -> list[Arc]:
        return self._arcs

    def get_circles(self) -> list[Circle]:
        return self._circles

    def get_splines(self) -> list[BSpline]:
        return self._splines

    def parse_figures(self, dxf_file: str):
        parser = CADParser(filepath=dxf_file)
        figures = parser.get_figures_parsed()
        self._raw_lines = figures.get("lines", [])
        self._raw_arcs = figures.get("arcs", [])
        self._raw_circles = figures.get("circles", [])
        self._raw_splines = figures.get("splines", [])

    def convert_figures(self):
        converter = Converter(float_precision=self._float_precision, pre_scale=self._pre_scale, lifting=self._lifting, origin=self._origin)
        figures = converter.convert_figures(lines=self._raw_lines,
                                            arcs=self._raw_arcs,
                                            circles=self._raw_circles,
                                            splines=self._raw_splines)
        self._polylines = figures.get("lines", [])
        self._arcs = figures.get("arcs", [])
        self._circles = figures.get("circles", [])
        self._splines = figures.get("splines", [])

        for line in self._polylines:
            line.set_velocity(self._polyline_velocity)

        for arc in self._arcs:
            arc.set_velocity(self._arc_velocity)

        for circle in self._circles:
            circle.set_velocity(self._circle_velocity)

    def get_raw_figures(self) -> dict:
        return {
            "lines": self._raw_lines,
            "arcs": self._raw_arcs,
            "circles": self._raw_circles,
            "splines": self._raw_splines
        }
    
    def get_figures(self) -> dict:
        return {
            "polylines": self._polylines,
            "arcs": self._arcs,
            "circles": self._circles,
            "splines": self._splines
        }

    def generate_rapid_code(self):
        draw = Draw(tool_name=self._tool_name,
                    velocity=self._global_velocity,
                    workspace_limits=self._workspace_limits,
                    origin=self._origin,
                    zero=self._zero,
                    use_detector=self._use_intelligent_traces)

        draw.add_figures(self._polylines)
        draw.add_figures(self._arcs)
        draw.add_figures(self._circles)
        draw.add_figures(self._splines)

        self._rapid_code = draw.generate_rapid_code(use_offset=self._use_offset_programming)

    def get_rapid_code(self) -> str:
        return self._rapid_code
    
    def export_rapid_to_txt(self, save_path: str):
        if not self._rapid_code or self._rapid_code == "":
            raise ValueError("No RAPID code generated. Please run generate_rapid_code() first.")
        
        with open(save_path, 'w') as file:
            file.write(self._rapid_code)
        print(f"RAPID code exported to {save_path}")