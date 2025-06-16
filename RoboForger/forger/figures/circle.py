from .figure import Figure
from RoboForger.types import Point3D
from typing import List


class Circle(Figure):
    """
    A circle is a fusion of two arcs, one for the upper half and one for the lower half.
    """

    def __init__(self, name: str, center: Point3D, radius, velocity: int = 100):
        self.center = center
        self.radius = radius
        super().__init__(name, [
            (center[0] - radius, center[1], center[2]),  # Start point
            (center[0], center[1] + radius, center[2]),  # Midpoint (top)
            (center[0] + radius, center[1], center[2]),  # Right point
            (center[0], center[1] - radius, center[2]),  # Midpoint (bottom)
            (center[0] - radius, center[1], center[2])  # End point (back to start)
        ], velocity)

    def move_instructions(self, tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        instructions = []

        robtargets = self.get_rob_targets()
        if not robtargets:
            raise ValueError("No robot targets generated for the circle.")

        # Move to start point (lifted position)
        instructions.append(
            f"        MoveJ {robtargets[0]}, v{global_velocity}, fine, {tool_name};\n"
        )

        # Move to start point (down)
        instructions.append(
            f"        MoveL {robtargets[1]}, v{global_velocity}, fine, {tool_name};\n"
        )

        # Create the upper half arc movement
        instructions.append(
            f"        MoveC {robtargets[2]}, {robtargets[3]}, v{self.velocity}, fine, {tool_name};\n"
        )
        # Create the lower half arc movement
        instructions.append(
            f"        MoveC {robtargets[4]}, {robtargets[5]}, v{self.velocity}, fine, {tool_name};\n"
        )
        # Move to end point (lifted position)
        instructions.append(
            f"        MoveL {robtargets[6]}, v{global_velocity}, fine, {tool_name};\n"
        )

        return instructions