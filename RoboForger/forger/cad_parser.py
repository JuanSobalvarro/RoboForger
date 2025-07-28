import ezdxf
import os
from typing import List, Tuple, Dict, Any
from RoboForger.types import Point3D


class CADParser:
    def __init__(self, filepath: str, scale: float = 1.0):
        self.doc = ezdxf.readfile(filepath)
        self._msp = self.doc.modelspace()
        self.scale = scale

    def _scale_point(self, point: Tuple[float, float, float]) -> Point3D:
        return tuple(coord * self.scale for coord in point)

    def _scale_value(self, value: float) -> float:
        return value * self.scale

    def set_doc(self, file_path: str):

        if os.path.exists(file_path):
            self.doc = ezdxf.readfile(file_path)
            self._msp = self.doc.modelspace()

            return f"File: {file_path} loaded correctly"

        return f"File: {file_path} could not be loaded"

    def get_lines(self) -> List[Tuple[Point3D, Point3D]]:
        lines = []
        for e in self._msp.query('LINE'):
            start = self._scale_point((e.dxf.start.x, e.dxf.start.y, getattr(e.dxf.start, 'z', 0.0)))
            end = self._scale_point((e.dxf.end.x, e.dxf.end.y, getattr(e.dxf.end, 'z', 0.0)))
            lines.append({'start': start, 'end': end})
        return lines

    def get_circles(self) -> List[Tuple[Point3D, float]]:
        circles = []
        for e in self._msp.query('CIRCLE'):
            center = self._scale_point((e.dxf.center.x, e.dxf.center.y, getattr(e.dxf.center, 'z', 0.0)))
            radius = self._scale_value(e.dxf.radius)
            circles.append({'center': center, 'radius': radius})
        return circles

    def get_arcs(self) -> List[Dict[str, Any]]:
        """
        Returns a list of arcs represented by:
        (center, radius, start_point, end_point, start_angle, end_angle, clockwise)
        """
        arcs = []
        for e in self._msp.query('ARC'):
            center = self._scale_point((e.dxf.center.x, e.dxf.center.y, getattr(e.dxf.center, 'z', 0.0)))
            radius = self._scale_value(e.dxf.radius)

            start_angle = e.dxf.start_angle
            end_angle = e.dxf.end_angle

            arcs.append({'center': center, 'radius': radius, 'start_angle': start_angle, 'end_angle': end_angle, 'clockwise': False})
        return arcs

    def get_figures_parsed(self) -> Dict[str, Any]:
        """
        Returns a dictionary with all figures parsed from the DXF file.
        """
        return {
            'lines': self.get_lines(),
            'arcs': self.get_arcs(),
            'circles': self.get_circles()
        }