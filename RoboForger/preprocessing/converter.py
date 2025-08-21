"""
This module converts CAD objects to RoboForger objects.
"""
from typing import List, Any, Dict
from RoboForger.types import Point3D, RawLine, RawCircle, RawArc, RawSpline
from RoboForger.drawing.figures import PolyLine, Arc, Circle, Figure, BSpline
from math import cos, sin, radians, pi, degrees
from RoboForger.utils import real_coord2robo_coord
import logging

class Converter:
    """
    Converter takes the raw figures and converts them into roboforger figures (initializing the figure objects). Converter only needs the figure points,
    the code is able to change values like velocity later.
    """
    def __init__(self, float_precision: int = 4, pre_scale: float = 1.0, lifting: float = 50.0, origin: Point3D = (450.0, 0, 450.0)):
        self.float_precision = float_precision
        self.lifting = lifting
        self.origin = origin
        self.pre_scale = pre_scale

    def apply_pre_scaling(self, point: Point3D) -> Point3D:
        """
        **IMPORTANT in this function we ensure that every point of the raw figures has Z = 0**
        """
        x, y, z = point
        # To robo coordinates the figures are moved down by lifting value relative to the origin used
        return (x * self.pre_scale, y * self.pre_scale, -self.lifting)

    def convert_lines_to_polylines(self, lines: List[RawLine]) -> List[PolyLine]:
        polylines = []
        for i, line in enumerate(lines):
            # First apply pre scaling
            start = self.apply_pre_scaling(line['start'])
            end = self.apply_pre_scaling(line['end'])
            robo_coords = [real_coord2robo_coord(start, self.origin), real_coord2robo_coord(end, self.origin)]
            # print(f"Robo coords generated: {robo_coords}")
            pl = PolyLine(f"Line{i}", robo_coords, lifting=self.lifting, velocity=1000, float_precision=self.float_precision)
            polylines.append(pl)
        return polylines

    def convert_circles(self, circles: List[RawCircle]) -> List[Circle]:
        circle_figs = []
        for i, circle in enumerate(circles):
            center = self.apply_pre_scaling(circle['center'])
            radius = circle['radius'] * self.pre_scale  
            c = Circle(f"Circle{i}", real_coord2robo_coord(center, self.origin), radius, lifting=self.lifting, float_precision=self.float_precision)
            circle_figs.append(c)
        return circle_figs

    def convert_arcs(self, arcs: List[RawArc]) -> List[Arc]:
        arc_figs = []
        for i, arc  in enumerate(arcs):
            center = self.apply_pre_scaling(arc["center"])
            radius = arc["radius"] * self.pre_scale
            start_angle = arc["start_angle"]
            end_angle = arc["end_angle"]

            print(f"Converting arc center: {center} to {real_coord2robo_coord(center, self.origin)}")

            arc_figs.append(Arc(f"Arc{i}",
                                         center=real_coord2robo_coord(center, self.origin),
                                         radius=radius,
                                         start_angle=start_angle,
                                         end_angle=end_angle,
                                         clockwise=arc["clockwise"],
                                         lifting=self.lifting,
                                         float_precision=self.float_precision))

        return arc_figs

    def convert_splines(self, splines: List[RawSpline]) -> List[BSpline]:

        spline_figs = []
        for i, spline in enumerate(splines):
            control_points = [self.apply_pre_scaling(pt) for pt in spline['control_points']]
            fit_points = [self.apply_pre_scaling(pt) for pt in spline['fit_points']]
            spline_figs.append(BSpline(f"Spline{i}",
                                      degree=spline['degree'],
                                      closed=spline['closed'],
                                      knots=spline['knots'],
                                      weights=spline['weights'],
                                      control_points=[real_coord2robo_coord(pt, self.origin) for pt in control_points],
                                      fit_points=[real_coord2robo_coord(pt, self.origin) for pt in fit_points],
                                      interpolation_precision=0.1,
                                      lifting=self.lifting,
                                      velocity=1000,
                                      float_precision=self.float_precision))
        return spline_figs

    def convert_figures(self, lines: List[RawLine], arcs: List[RawArc], circles: List[RawCircle], splines: List[RawSpline]) -> Dict[str, List[Figure]]:
        """
        Converts all figures into a list of Figure objects.
        """
        figures = {"lines": self.convert_lines_to_polylines(lines),
                   "arcs": self.convert_arcs(arcs),
                   "circles": self.convert_circles(circles),
                   "splines": self.convert_splines(splines)}
        
        return figures