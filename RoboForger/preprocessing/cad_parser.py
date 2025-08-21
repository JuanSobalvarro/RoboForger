import ezdxf
import os
from typing import List, Tuple, Dict, Any
from RoboForger.types import Point3D, RawLine, RawArc, RawCircle, RawSpline


class CADParser:
    def __init__(self, filepath: str):
        self.doc = ezdxf.readfile(filepath)
        self._msp = self.doc.modelspace()

    def set_doc(self, file_path: str):

        if os.path.exists(file_path):
            self.doc = ezdxf.readfile(file_path)
            self._msp = self.doc.modelspace()

            return f"File: {file_path} loaded correctly"

        return f"File: {file_path} could not be loaded"

    def get_lines(self) -> List[RawLine]:
        lines = []
        for e in self._msp.query('LINE'):
            start = (e.dxf.start.x, e.dxf.start.y, getattr(e.dxf.start, 'z', 0.0))
            end = (e.dxf.end.x, e.dxf.end.y, getattr(e.dxf.end, 'z', 0.0))
            lines.append({'start': start, 'end': end})
        return lines

    def get_circles(self) -> List[RawCircle]:
        circles = []
        for e in self._msp.query('CIRCLE'):
            center = (e.dxf.center.x, e.dxf.center.y, getattr(e.dxf.center, 'z', 0.0))
            radius = e.dxf.radius
            circles.append({'center': center, 'radius': radius})
        return circles

    def get_arcs(self) -> List[RawArc]:
        """
        Returns a list of arcs represented by:
        (center, radius, start_point, end_point, start_angle, end_angle, clockwise)
        """
        arcs = []
        for e in self._msp.query('ARC'):
            center = (e.dxf.center.x, e.dxf.center.y, getattr(e.dxf.center, 'z', 0.0))
            radius = e.dxf.radius

            start_angle = e.dxf.start_angle
            end_angle = e.dxf.end_angle

            arcs.append({'center': center, 'radius': radius, 'start_angle': start_angle, 'end_angle': end_angle, 'clockwise': False})
        return arcs

    def get_splines(self) -> List[RawSpline]:
        """
        Returns a list of splines represented by
        """
        splines = []
        for e in self._msp.query('SPLINE'):
            # just for testing if it works
            # print(f"Spline: {e} - Degree: {e.dxf.degree} - Closed: {e.closed}. Control points{len(e.control_points)}: {e.control_points}. Weights: {e.weights}. Knots: {e.knots}. Fit points: {e.fit_points}")
            splines.append(
                {
                    'degree': e.dxf.degree,
                    'closed': e.closed,
                    'knots': e.knots,
                    'weights': e.weights,
                    'control_points': [(pt[0], pt[1], 0.0) for pt in e.control_points],
                    'fit_points': [(pt[0], pt[1], 0.0) for pt in e.fit_points],
                }
            )
        return splines

    def get_figures_parsed(self) -> Dict[str, Any]:
        """
        Returns a dictionary with all figures parsed from the DXF file.
        """
        return {
            'lines': self.get_lines(),
            'arcs': self.get_arcs(),
            'circles': self.get_circles(),
            'splines': self.get_splines()
        }