from typing import List
from RoboForger.types import Point3D


class Figure:
    """
    Base class for all figures in RoboForger.

    ** IMPORTANT: **
    A figure points always should start by the pre down (lifted) point, ... figure points, then the end point is the
    lifted point.
    """
    def __init__(self, name: str, points: List[Point3D], lifting: float = 100,  velocity: int = 1000, float_precision: int = 4):

        if not points or len(points) < 2:
            raise ValueError("A figure must have at least two points.")

        self.name = name
        self.lifting = lifting
        self.velocity = velocity
        self.float_precision = float_precision

        # Round points to the specified float precision
        self._points: List[Point3D] = [Figure.round_point(point, self.float_precision) for point in points]

        self.__skip_pre_down = False
        self.__skip_end_lifting = False

        self.rob_targets = []
        self.target_count = 0

        # Add lifting points
        self._add_lifted_points()
        self.__generate_rob_targets()

    @staticmethod
    def round_point(point: Point3D, precision: int) -> Point3D:
        """
        Rounds the point coordinates to the specified float precision.
        """
        if len(point) != 3:
            raise ValueError("Point must be a tuple of three float values (x, y, z).")

        if not isinstance(precision, int) or precision <= 0:
            raise ValueError("Precision must be a positive integer.")

        return tuple(round(coord, precision) for coord in point)

    def _add_lifted_points(self):
        """
        Adds a lifted point at the start and end of the figure points. Pre-down and end-lifted points
        """
        start_lifted_point = (self._points[0][0], self._points[0][1], self._points[0][2] + self.lifting)
        end_lifted_point = (self._points[-1][0], self._points[-1][1], self._points[-1][2] + self.lifting)

        self._points.insert(0, start_lifted_point)
        self._points.append(end_lifted_point)

    def get_start_and_end_points(self) -> (Point3D, Point3D):
        """
        Returns the first and last points of the figure.
        The first point is the pre-down (lifted) point, and the last point is the end lifted point.
        """
        if not self._points:
            raise ValueError("The figure has no points.")
        return self._points[0], self._points[-1]

    def reverse_points(self):
        """
        Reverses the order of points in the figure.
        This is useful for drawing figures in reverse order.
        """
        self._points.reverse()
        self.rob_targets.clear()

    def set_velocity(self, velocity: int):
        if velocity <= 0:
            raise ValueError("Velocity must be a positive integer.")
        self.velocity = velocity

    @property
    def skip_pre_down(self) -> bool:
        """
        Returns True if the first point is not a pre-down (lifted) point.
        """
        return self.__skip_pre_down

    @property
    def skip_end_lifting(self) -> bool:
        """
        Returns True if the last point is not a lifted point.
        """
        return self.__skip_end_lifting

    def set_skip_pre_down(self, skip: bool = True):
        """
        If True, the first point is not a pre-down (lifted) point.
        """
        self.__skip_pre_down = skip

    def set_skip_end_lifted(self, skip: bool = True):
        """
        If True, the last point is not a lifted point.
        """
        self.__skip_end_lifting = skip

    def get_points(self) -> List[Point3D]:
        return self._points

    @staticmethod
    def offset_coord(origin_target_name: str, origin: Point3D, point: Point3D) -> str:

        return f"({origin_target_name}, {round(point[0] - origin[0], 4)}, {round(point[1] - origin[1], 4)}, {round(point[2] - origin[2], 4)})"

    # Override this method in subclasses to provide specific move instructions
    def move_instructions(self, tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        ...

    def move_instructions_offset(self, origin_robtarget_name: str, origin: Point3D = (450.0, 0, 450.0), tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        """
        This method is used to generate move instructions with the offset method for the tool.
        It can be overridden in subclasses if needed.
        """
        ...

    def clear_rob_targets(self):
        """
        Clears the rob targets list and resets the target count.
        This is useful if you want to regenerate the rob targets.
        """
        self.rob_targets.clear()
        self.target_count = 0

    def get_rob_targets(self) -> List[str]:
        """
        Returns the list of all rob targets name in order of use
        """
        return self.rob_targets

    def get_rob_targets_formatted(self) -> List[str]:
        return self.__generate_rob_targets()

    @staticmethod
    def _create_rob_target_coord(point: Point3D) -> str:
        """
        Creates a rob target string for a given point.
        This is useful for generating individual rob targets without generating the entire list.
        """
        return f"[[{point[0]},{point[1]},{point[2]}]," \
               f"[4.14816E-8,6.1133E-9,-1,-2.53589E-16],[0,0,-1,0]," \
               f"[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]"

    @staticmethod
    def rob_target_format(target_name: str, point: Point3D) -> str:
        """
        Formats a rob target string for a given point and target name.
        This is useful for generating individual rob targets without generating the entire list.
        """
        return f"CONST robtarget {target_name}:={Figure._create_rob_target_coord(point)};\n"

    def __generate_rob_targets(self):
        """
        This function generates the rob targets for the figure based on the points the figure has. It will generate a point lifted,
        a point at the start(down), movements of the figure**, then a point lifted at the end.

        ** The generated rob targets are in ORDER ACCORDING TO THE POINTS at the current state of the figure.
        """
        self.rob_targets.clear()
        rob_targets_formatted: List[str] = []
        self.target_count = 0

        for point in self.get_points():
            target_name = self.__generate_target_name(self.target_count)
            self.target_count += 1

            rob_targets_formatted.append(Figure.rob_target_format(target_name, point))

        return rob_targets_formatted

    def __generate_target_name(self, count: int) -> str:
        return f"P{self.name}{count}"
