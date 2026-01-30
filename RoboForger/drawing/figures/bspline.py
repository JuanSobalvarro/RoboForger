from .figure import Figure
from typing import List, Tuple
from RoboForger.fig_types import Point3D

import numpy as np

class BSpline(Figure):
    def __init__(self, name: str, degree: int, closed: bool, knots: List[float], weights: List[float], control_points: List[Point3D], fit_points: List[Point3D], interpolation_precision: float = 10, lifting: float = 100, velocity: int = 1000, float_precision: int = 6):
        self.degree = degree
        self.closed = closed
        self.knots = np.array(knots, dtype=float)
        self.weights = np.array(weights, dtype=float) if weights else None
        self.control_points = np.array(control_points, dtype=float)
        self.fit_points = fit_points
        self.num_points = self.get_num_points(interpolation_precision)

        points = self.get_all_points()

        super().__init__(name, points, lifting, velocity, float_precision)

    def get_num_points(self, interpolation_precision: float) -> int:
        num_points = 0
        if len(self.control_points) > 0:
            max_p = np.max(self.control_points, axis=0)
            min_p = np.min(self.control_points, axis=0)
            # Simple bounding box approximation
            distance = np.linalg.norm(max_p - min_p)
            if distance > 0:
                num_points = int(distance * interpolation_precision / 10)
                # Ensure a minimum resolution so small splines don't look like triangles
                num_points = max(num_points, 20) 
            print(f"Num Points: {num_points}")
        return num_points

    def get_all_points(self) -> List[Point3D]:
        # Domain of the spline (usually [knots[degree], knots[-degree-1]])
        start_t = self.knots[self.degree]
        end_t = self.knots[-self.degree - 1]
        
        # Create evaluation parameters (t)
        t_values = np.linspace(start_t, end_t, self.num_points)

        # Evaluate using pure numpy
        points = self._evaluate_spline(t_values)

        return points.tolist()

    def _evaluate_spline(self, t_values: np.ndarray) -> np.ndarray:
        """
        Evaluates the B-Spline (or NURBS) at given t parameters using De Boor's algorithm.
        Supports Weights (NURBS) if self.weights is present.
        """
        n = len(self.control_points) - 1
        p = self.degree
        knots = self.knots
        
        # If we have weights, convert to Homogeneous coordinates (x*w, y*w, z*w, w)
        if self.weights is not None and len(self.weights) == len(self.control_points):
            # Shape (N, 4) -> [wx, wy, wz, w]
            ctrl_h = np.column_stack((self.control_points * self.weights[:, None], self.weights))
        else:
            # Shape (N, 3)
            ctrl_h = self.control_points

        result_points = []

        for t in t_values:
            # Find the knot span index 'k' such that knots[k] <= t < knots[k+1]
            # We clip to ensure we don't go out of bounds at the very end
            k = np.searchsorted(knots, t, side='right') - 1
            k = np.clip(k, p, n)

            # De Boor's Algorithm
            # Copy the relevant control points for this span
            d = ctrl_h[k - p : k + 1].copy()

            for r in range(1, p + 1):
                for j in range(p, r - 1, -1):
                    denom = knots[j + k - r + 1] - knots[j + k - p]
                    alpha = (t - knots[j + k - p]) / denom if denom != 0 else 0.0
                    d[j] = (1.0 - alpha) * d[j - 1] + alpha * d[j]

            # The result is the last point in the array
            final_val = d[p]

            # Convert back from Homogeneous if needed (NURBS projection)
            if self.weights is not None:
                # Divide x,y,z by w
                point_3d = final_val[:3] / final_val[3]
                result_points.append(point_3d)
            else:
                result_points.append(final_val)

        return np.array(result_points)

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