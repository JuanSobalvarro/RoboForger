"""
This module creates a Draw class that is used to generate the Rapid Code given a CAD file.
"""
import os
from typing import Tuple, Sequence
from RoboForger.drawing.figures.figure import Figure
from RoboForger.fig_types import Point3D, RawLine, RawArc, RawCircle, RawSpline
from RoboForger.drawing.figures import PolyLine, Arc, Circle, BSpline
from RoboForger.preprocessing.cad_parser import CADParser
from RoboForger.preprocessing.converter import Converter
from RoboForger.drawing.draw import Draw
from RoboForger.utils import get_resource_path


class ForgerParameters:
    """
    Remember to always keep this class picklable since we need to send it to the processing function in a separate process.
    """
    __slots__ = (
        "origin",
        "zero",
        "pre_scale",
        "float_precision",
        "lifting",
        "tool_name",
        "global_velocity",
        "polyline_velocity",
        "arc_velocity",
        "circle_velocity",
        "spline_velocity",
        "workspace_limits",
        "use_intelligent_traces",
        "use_offset_programming",
    )

    def __init__(self):
        self.origin: Point3D = (450.0, 0.0, 450.0)
        self.zero: Point3D = (0.0, 0.0, 0.0)
        self.pre_scale: float = 1.0
        self.float_precision: int = 4
        self.lifting: float = 50.0
        self.tool_name: str = "tool0"

        self.global_velocity = 1000
        self.polyline_velocity = 1000
        self.arc_velocity = 1000
        self.circle_velocity = 1000
        self.spline_velocity = 1000

        self.workspace_limits = ((-100, -700, -100), (800, 700, 800))
        self.use_intelligent_traces = True
        self.use_offset_programming = True

    def to_dict(self) -> dict:
        return {
            "origin": self.origin,
            "zero": self.zero,
            "pre_scale": self.pre_scale,
            "float_precision": self.float_precision,
            "lifting": self.lifting,
            "tool_name": self.tool_name,
            "global_velocity": self.global_velocity,
            "polyline_velocity": self.polyline_velocity,
            "arc_velocity": self.arc_velocity,
            "circle_velocity": self.circle_velocity,
            "spline_velocity": self.spline_velocity,
            "workspace_limits": self.workspace_limits,
            "use_intelligent_traces": self.use_intelligent_traces,
            "use_offset_programming": self.use_offset_programming,
        }

    def apply(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Forger:
    """
    The forger class generalize the utilization of roboforger in 4 steps:
    - File Parsing: Takes a DXF file and parses the figures it founds
    - Convertion: Converts the parsed figures into the figures forger understand (python objects)
    - Drawing detection: Logic for drawing, order of figures and maybe intelligent tracing
    - Code Generation: Translate traces and points into RAPID code
    """
    def __init__(
            self,
            parameters: ForgerParameters,
        ):

        self._params = parameters

        self._raw_lines: list[RawLine] = []
        self._raw_arcs: list[RawArc] = []
        self._raw_circles: list[RawCircle] = []
        self._raw_splines: list[RawSpline] = []

        self._polylines: list[PolyLine] = []
        self._arcs: list[Arc] = []
        self._circles: list[Circle] = []
        self._splines: list[BSpline] = []

        self._parsed: bool = False # flag to know if figures have been parsed
        self._converted: bool = False # flag to know if figures have been converted
        self._rapid_code: str = "" # generated RAPID code after processing

    def parse_figures(self, cad_file: str):
        if not os.path.exists(cad_file):
            raise FileNotFoundError(f"CAD file not found at {cad_file}")
        
        if self._parsed:
            self._parsed = False  # reset parsed flag if new parsing is done

        try:
            parser = CADParser(filepath=cad_file, binary_dwg2dxf_path=get_resource_path("bin/dwg2dxf"))
        except Exception as e:
            raise RuntimeError(f"Failed to initialize CAD parser: {e}")
        
        figures = parser.get_figures_parsed()
        self._raw_lines = figures.get("lines", [])
        self._raw_arcs = figures.get("arcs", [])
        self._raw_circles = figures.get("circles", [])
        self._raw_splines = figures.get("splines", [])

        self._parsed = True

        if self._converted:
            self._converted = False  # reset converted flag if new parsing is done

    def convert_figures(self):
        converter = Converter(float_precision=self._params.float_precision, pre_scale=self._params.pre_scale, lifting=self._params.lifting, origin=self._params.origin)
        figures: dict[str, list[PolyLine | Arc | Circle | BSpline]] = converter.convert_figures(lines=self._raw_lines,
                                                                                                arcs=self._raw_arcs,
                                                                                                circles=self._raw_circles,
                                                                                                splines=self._raw_splines)
        self._polylines = figures.get("lines", []) # type: ignore
        self._arcs = figures.get("arcs", []) # type: ignore
        self._circles = figures.get("circles", [])  # type: ignore
        self._splines = figures.get("splines", []) # type: ignore

        for line in self._polylines:
            line.set_velocity(self._params.polyline_velocity)

        for arc in self._arcs:
            arc.set_velocity(self._params.arc_velocity)

        for circle in self._circles:
            circle.set_velocity(self._params.circle_velocity)

        # for spline in self._splines:
        #     spline.set_velocity(self._params.spline_velocity)

        self._converted = True

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
        draw = Draw(tool_name=self._params.tool_name,
                    velocity=self._params.global_velocity,
                    workspace_limits=self._params.workspace_limits,
                    origin=self._params.origin,
                    zero=self._params.zero,
                    use_detector=self._params.use_intelligent_traces)

        draw.add_figures(self._polylines) # type: ignore
        draw.add_figures(self._arcs) # type: ignore
        draw.add_figures(self._circles) # type: ignore
        draw.add_figures(self._splines) # type: ignore

        self._rapid_code = draw.generate_rapid_code(use_offset=self._params.use_offset_programming)

    def get_rapid_code(self) -> str:
        return self._rapid_code
    
    def export_rapid_to_txt(self, save_path: str):
        if not self._rapid_code or self._rapid_code == "":
            raise ValueError("No RAPID code generated. Please run generate_rapid_code() first.")
        
        with open(save_path, 'w') as file:
            file.write(self._rapid_code)
        print(f"RAPID code exported to {save_path}")
