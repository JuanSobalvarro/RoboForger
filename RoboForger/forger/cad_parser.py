import ezdxf
import os
from typing import List, Tuple, Dict, Any

Point3D = Tuple[float, float, float]


class CADParser:
    def __init__(self, filepath: str, scale: float = 1.0, float_precision: int = 4):
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
            lines.append((start, end))
        return lines

    def get_circles(self) -> List[Tuple[Point3D, float]]:
        circles = []
        for e in self._msp.query('CIRCLE'):
            center = self._scale_point((e.dxf.center.x, e.dxf.center.y, getattr(e.dxf.center, 'z', 0.0)))
            radius = self._scale_value(e.dxf.radius)
            circles.append((center, radius))
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

    def convert_lines_to_polylines(lines: List[tuple]) -> List[PolyLine]:
        polylines = []
        for i, (start, end) in enumerate(lines):
            # Each line is a PolyLine with two points
            robo_coords = [real_coord2robo_coord(start), real_coord2robo_coord(end)]
            pl = PolyLine(f"Line{i}", robo_coords, lifting=100, velocity=1000)
            polylines.append(pl)
        return polylines

    def convert_circles(circles: List[tuple]) -> List[Circle]:
        circle_figs = []
        for i, (center, radius) in enumerate(circles):
            c = Circle(f"Circle{i}", real_coord2robo_coord(center), radius, lifting=100)
            circle_figs.append(c)
        return circle_figs

    def convert_arcs(arcs: List[Dict]) -> List[Arc]:
        arc_figs = []
        for i, arc in enumerate(arcs):
            # If angle is too wide (>180) split arc in two
            center = real_coord2robo_coord(arc["center"])
            # center = arc["center"]
            start_angle = arc["start_angle"]
            end_angle = arc["end_angle"]

            arc_figs.append(Arc(f"Arc{i}",
                                center=center,
                                radius=arc["radius"],
                                start_angle=start_angle,
                                end_angle=end_angle,
                                clockwise=arc["clockwise"],
                                lifting=100))

        return arc_figs
