from typing import Tuple, List, Dict, Union, TypedDict


Point3D = Tuple[float, float, float]

class RawLine(TypedDict):
    start: Point3D
    end: Point3D

class RawCircle(TypedDict):
    center: Point3D
    radius: float

class RawArc(TypedDict):
    center: Point3D
    radius: float
    start_angle: float
    end_angle: float
    clockwise: bool

class RawSpline(TypedDict):
    degree: int
    closed: bool
    knots: List[float]
    weights: List[float]
    control_points: List[Point3D]
    fit_points: List[Point3D]
