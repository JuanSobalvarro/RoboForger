from .figure import Figure
from typing import List, Tuple
from RoboForger.types import Point3D\

import numpy as np
from scipy import interpolate as spi

class BSpline(Figure):
    """
    Represents a B-Spline figure in RoboForger.
    Inherits from the Figure class and adds functionality specific to B-Splines.

    Spline will be approximated using MoveL commands between calculated points.
    """

    def __init__(self, name: str, degree: int, closed: bool, knots: List[float], weights: List[float], control_points: List[Point3D], fit_points: List[Point3D], interpolation_precision: float = 10, lifting: float = 100, velocity: int = 1000, float_precision: int = 6):
        """
        :param interpolation_precision: Amount of points per unity of distance
        """
        self.degree = degree
        self.closed = closed
        self.knots = knots
        self.weights = weights
        self.control_points = control_points
        self.fit_points = fit_points
        self.num_points = self.get_num_points(interpolation_precision)

        points = self.get_all_points()

        super().__init__(name, points, lifting, velocity, float_precision)

    def get_num_points(self, interpolation_precision: float) -> int:
        """
        This function calculates the interpolation precision (amount of points) based on the distance
        between the maximum and minimum control points.
        """
        num_points = 0

        if self.control_points:
            max_point_x = np.max(self.control_points, axis=0)
            max_point_y = np.max(self.control_points, axis=1)
            min_point_x = np.min(self.control_points, axis=0)
            min_point_y = np.min(self.control_points, axis=1)
            distance = np.linalg.norm(max_point_x - min_point_x) + np.linalg.norm(max_point_y - min_point_y)
            if distance > 0:
                num_points = int(distance * interpolation_precision / 10)
            print(f"Num Points: {num_points}")

        return num_points

    def get_all_points(self) -> List[Point3D]:

        # Create a B-Spline object using scipy
        spline = spi.BSpline(self.knots, self.control_points, self.degree)
        
        t_values = np.linspace(self.knots[self.degree], self.knots[-self.degree-1], self.num_points)

        points = spline(t_values)

        return points.tolist()

    def move_instructions_offset(self, origin_robtarget_name: str, origin: Point3D = (450.0, 0.0, 450.0), tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        instructions = []

        robtargets = self.get_rob_target_names()

        points = self.get_points()

        if not self.skip_pre_down:
            instructions.append(f"        !init_lifted\n")
            instructions.append(f"        MoveJ Offs {Figure.offset_coord(origin_robtarget_name, origin, points[0])}, v{global_velocity}, fine, {tool_name};\n")

        # Now MoveL approximations of the spline
        for i, point in enumerate(points[1:-1]):
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, point)}, v{self.velocity}, fine, {tool_name}; !Spline Point {i}\n")
    
        if not self.skip_end_lifting:
            instructions.append(f"        MoveJ Offs {Figure.offset_coord(origin_robtarget_name, origin, points[-1])}, v{global_velocity}, fine, {tool_name};\n")
            instructions.append(f"        !end_lifted\n")
    
        return instructions

    def __str__(self) -> str:
        return f"Spline(Name: {self.name}, Degree: {self.degree}, Closed: {self.closed}, Control Points: {len(self.control_points)}, Fit Points: {len(self.fit_points)}, Knots: {self.knots}, Weights: {self.weights}, Number of Points: {self.num_points}, Total Points: {len(self._points)})"
    
    def __repr__(self) -> str:
        return self.__str__()