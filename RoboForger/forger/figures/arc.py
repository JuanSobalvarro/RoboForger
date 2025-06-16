from .figure import Figure
from typing import List, Tuple, Union, Optional
from RoboForger.types import Point3D
from math import sqrt, atan2, pi, cos, sin, radians
from RoboForger.utils import round_tuple, normalize_angle, normalize_angle_deg


class Arc(Figure):
    """
    Represents an arc between two or three 3D points on the XY plane.
    The arc can be defined by start and end points with either:
        - a midpoint calculated via a provided radius, or
        - by providing explicit start and end angles.
    """

    def __init__(self, name: str, center: Optional[Point3D] = None, radius: float = 1, start_angle: float = 0, end_angle: float = 0,
                 clockwise: bool = False, lifting: float = 100, velocity: int = 1000):
        """
        Initialize an Arc object.
        :param name: Name of the arc.
        :param center: Center point of the arc (x, y, z).
        :param radius: Radius of the arc.
        :param start_angle: Start angle of the arc in degrees.
        :param end_angle: End angle of the arc in degrees.
        :param clockwise: True for clockwise arc, False for counter-clockwise.
        :param velocity: Velocity for the arc movement.
        """

        if radius <= 0:
            raise ValueError("Radius must be a positive number.")
        if start_angle is None:
            raise ValueError("Start angle cannot be None.")
        if end_angle is None:
            raise ValueError("End angle cannot be None.")

        self.center = center
        self.start_angle = normalize_angle(radians(start_angle))
        self.end_angle = normalize_angle(radians(end_angle))
        self.mid_angle = Arc.mid_angle_clock(self.start_angle, self.end_angle, clockwise)
        self.radius = radius
        self.clockwise = clockwise

        self.start, self.mid, self.end = Arc.arc_points(self.center, radius, self.start_angle, self.end_angle, clockwise)

        if Arc.arc_angle(self.start_angle, self.end_angle, self.clockwise) >= pi:
            print("Angle greater than pi, splitting the arc into two segments.")
            print(f"Init values from {start_angle} to {end_angle}")
            print(f"Arc sa {self.start_angle}, ea {self.end_angle}, mid {self.mid_angle}")

            _, self.mid_1, _ = Arc.arc_points(self.center, radius, self.start_angle, self.mid_angle, clockwise)
            _, self.mid_2, _ = Arc.arc_points(self.center, radius, self.mid_angle, self.end_angle, clockwise)

            super().__init__(name, [self.start, self.mid_1, self.mid, self.mid_2, self.end], lifting, velocity)

        else:
            self.start = round_tuple(self.start, 4)
            self.mid = round_tuple(self.mid, 4)
            self.end = round_tuple(self.end, 4)

            super().__init__(name, [self.start, self.mid, self.end], lifting, velocity)

    @staticmethod
    def arc_points(center: Point3D, radius: float, start_angle: float, end_angle: float, clockwise: bool) -> Tuple[Point3D, Point3D, Point3D]:
        """
        Calculate the start, midpoint, and end points of the arc based on center, radius, start and end angles.
        :param center: Center point of the arc (x, y, z).
        :param radius: Radius of the arc.
        :param start_angle: Start angle in radians.
        :param end_angle: End angle in radians.
        :param clockwise: True for clockwise arc, False for counter-clockwise.
        :return: Tuple of start, midpoint, and end points as Point3D tuples.
        """
        if start_angle is None or end_angle is None:
            raise ValueError("Start and end angles must be provided.")

        start = Arc.point_from_angle(center, radius, start_angle)

        end = Arc.point_from_angle(center, radius, end_angle)

        mid_angle = Arc.mid_angle_clock(start_angle, end_angle, clockwise)

        mid = Arc.point_from_angle(center, radius, mid_angle)

        return start, mid, end

    @staticmethod
    def mid_angle_clock(start_angle: float, end_angle: float, clockwise: bool) -> float:
        mid_angle = (end_angle - start_angle) / 2 + start_angle

        if clockwise:
            mid_angle += pi

        if start_angle > end_angle:
            mid_angle += pi

        return mid_angle % (2 * pi)

    @staticmethod
    def arc_angle(start_angle: float, end_angle: float, clockwise: bool) -> float:
        """
        Calculate the angle of the arc in radians.
        :param start_angle: Start angle in radians.
        :param end_angle: End angle in radians.
        :param clockwise: True for clockwise arc, False for counter-clockwise.
        :return: Angle of the arc in radians.
        """
        angle = end_angle - start_angle
        if clockwise:
            angle += pi

        return angle % (2 * pi)

    @staticmethod
    def point_from_angle(center: Point3D, radius: float, angle_rad: float) -> Point3D:
        x = center[0] + radius * cos(angle_rad)
        y = center[1] + radius * sin(angle_rad)
        z = center[2]  # Assuming z-coordinate remains the same
        return x, y, z

    def move_instructions(self, tool_name: str = "tool0", global_velocity: int = 1000) -> List[
        str]:
        """
        Generate robot move instructions, splitting the arc into smaller MoveC segments if necessary.

        Args:
            tool_name (str): The robot tool to use.
            global_velocity (int): Global velocity for MoveJ/MoveL.

        Returns:
            List[str]: List of move instruction strings.
        """
        instructions = []

        # Move to start position
        robtargets = self.get_rob_targets()
        instructions.append(f"        MoveJ {robtargets[0]}, v{global_velocity}, fine, {tool_name};\n")
        instructions.append(f"        MoveL {robtargets[1]}, v{global_velocity}, fine, {tool_name};\n")

        # # If angle is greater or equal than 180 degrees (pi radians), split the arc into 2 segments
        # angle_diff = abs(self.end_angle - self.start_angle)

        # If we dont have a sweep limitation proceed as a single arc
        if Arc.arc_angle(self.start_angle, self.end_angle, self.clockwise) < pi:

            print(f"Arc is less than 180 degrees, robtargets: {robtargets}")

            instructions.append(f"        MoveC {robtargets[2]}, {robtargets[3]}, v{self.velocity}, fine, {tool_name};\n")

            # MoveL to ensure finishing precisely at the end
            instructions.append(f"        MoveL {robtargets[4]}, v{global_velocity}, fine, {tool_name};\n")

            return instructions

        print(f"Robtargets for arc greater than 180 {self.name}: {robtargets}")

        # Move to the first mid point
        instructions.append(f"        MoveC {robtargets[2]}, {robtargets[3]}, v{self.velocity}, fine, {tool_name};\n")
        # Move to the second mid point
        instructions.append(f"        MoveC {robtargets[4]}, {robtargets[5]}, v{self.velocity}, fine, {tool_name};\n")

        # MoveL to ensure finishing in end point
        instructions.append(f"        MoveL {robtargets[5]}, v{global_velocity}, fine, {tool_name};\n")

        return instructions

    def __str__(self):
        name = f"Arc<name={self.name}>"
        mid = f", mid=({self.mid[0]}, {self.mid[1]}, {self.mid[2]})" if self.mid else ""
        return f"{name}, start={self.start}{mid}, end={self.end}, radius={self.radius}, clockwise={self.clockwise}>"
