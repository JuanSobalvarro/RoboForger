"""
This module converts CAD objects to RoboForger objects.
"""
from typing import List, Any, Dict
from RoboForger.types import Point3D
from RoboForger.forger.figures import PolyLine, Arc, Circle, Figure
from math import cos, sin, radians, pi, degrees
from RoboForger.utils import real_coord2robo_coord

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
    for i, arc  in enumerate(arcs):
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
