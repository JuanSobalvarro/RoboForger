from typing import List
from .figure import Figure
from RoboForger.types import Point3D


class PolyLine(Figure):
    """
    This figure draws a polyline connecting a series of points.
    The points are connected in the order they are provided.
    """

    def __init__(self, name: str, points: List[Point3D], velocity: int = 1000):
        super().__init__(name, points, velocity)

    def move_instructions(self, tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        instructions = []

        targets = self.get_rob_targets()

        if not targets:
            raise ValueError("No robot targets generated for the polyline.")

        # Move to the first point
        instructions.append(
            f"        MoveJ {targets[0]}, v{global_velocity}, fine, {tool_name};\n"
        )

        for rob_target in targets[:-1]:  # Skip the last target which is the lift point
            instructions.append(
                f"        MoveL {rob_target}, v{self.velocity}, fine, {tool_name};\n"
            )

        # Move to the last point (lift point)
        instructions.append(
            f"        MoveL {targets[-1]}, v{global_velocity}, fine, {tool_name};\n"
        )

        return instructions

    def __str__(self):
        format_str = f"Polyline<name={self.name}>"

        for point in self.points:
            format_str += f" -> ({point[0]}, {point[1]}, {point[2]})"

        return format_str

    def __repr__(self):
        return self.__str__()