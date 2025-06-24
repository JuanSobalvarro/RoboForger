from typing import List
from .figure import Figure
from RoboForger.types import Point3D


class PolyLine(Figure):
    """
    This figure draws a polyline connecting a series of points.
    The points are connected in the order they are provided.
    """

    def __init__(self, name: str, points: List[Point3D], lifting: float, velocity: int = 1000, float_precision: int = 6):

        super().__init__(name, points, lifting, velocity, float_precision)

    def move_instructions(self, tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        instructions = []

        targets = self.get_rob_target_names()

        if not targets:
            raise ValueError("No robot targets generated for the polyline.")

        # Move to the first point
        if not self.skip_pre_down:
            instructions.append(f"        !init_lifted\n")
            instructions.append(
                f"        MoveJ {targets[0]}, v{global_velocity}, fine, {tool_name};\n"
            )

        for rob_target in targets[1:-1]:  # Skip the last target which is the lift point
            instructions.append(
                f"        MoveL {rob_target}, v{self.velocity}, fine, {tool_name};\n"
            )

        # Move to the last point (lift point)
        if not self.skip_end_lifting:
            instructions.append(f"        !end_lifted\n")
            instructions.append(
                f"        MoveL {targets[-1]}, v{global_velocity}, fine, {tool_name};\n"
            )

        return instructions

    def move_instructions_offset(self, origin_robtarget_name: str, origin: Point3D = (450.0, 0.0, 450.0), tool_name: str = "tool0",  global_velocity: int = 1000) -> List[str]:
        instructions = []

        points = self.get_points()

        # Pre down point
        if not self.skip_pre_down:
            instructions.append(f"        !init_lifted\n")
            instructions.append(f"        MoveJ Offs {Figure.offset_coord(origin_robtarget_name, origin, points[0])}, v{global_velocity}, fine, {tool_name};\n")

        for point in points[1:-1]:  # Skip the first and last points (lifted points)

            instruction = f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, point)}, v{global_velocity}, fine, {tool_name};\n"

            instructions.append(instruction)

        # Final lifted point
        if not self.skip_end_lifting:
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[-1])}, v{global_velocity}, fine, {tool_name};\n")
            instructions.append(f"        !end_lifted\n")

        return instructions

    def __str__(self):
        format_str = f"Polyline<name={self.name}>"

        for point in self._points:
            format_str += f" -> ({point[0]}, {point[1]}, {point[2]})"

        return format_str

    def __repr__(self):
        return self.__str__()