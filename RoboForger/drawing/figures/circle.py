from .figure import Figure
from RoboForger.types import Point3D
from typing import List


class Circle(Figure):
    """
    A circle is a fusion of two arcs, one for the upper half and one for the lower half.
    """

    def __init__(self, name: str, center: Point3D, radius, lifting: float, velocity: int = 100):
        self.center = center
        self.radius = radius
        # Round the center point to 4 decimal places
        center = tuple(round(coord, 4) for coord in center)
        super().__init__(name, [
            (center[0] - radius, center[1], center[2]),  # Start point
            (center[0], center[1] + radius, center[2]),  # Midpoint (top)
            (center[0] + radius, center[1], center[2]),  # Right point
            (center[0], center[1] - radius, center[2]),  # Midpoint (bottom)
            (center[0] - radius, center[1], center[2])  # End point (back to start)
        ], lifting, velocity)

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

    def move_instructions_offset(self, origin_robtarget_name: str, origin: Point3D = (450.0, 0, 450.0), tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        instructions = []

        points = self.get_points()

        # Pre down point
        if not self.skip_pre_down:
            instructions.append(f"        !init_lifted\n")
            instructions.append(f"        MoveJ Offs {Figure.offset_coord(origin_robtarget_name, origin, points[0])}, v{global_velocity}, fine, {tool_name};\n")

        # Move to start point (down)
        instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[1])}, v{global_velocity}, fine, {tool_name};\n")

        # Create the upper half arc movement
        instructions.append(f"        MoveC Offs {Figure.offset_coord(origin_robtarget_name, origin, points[2])}, Offs {Figure.offset_coord(origin_robtarget_name, origin, points[3])}, v{self.velocity}, fine, {tool_name};\n")

        # Create the lower half arc movement
        instructions.append(f"        MoveC Offs {Figure.offset_coord(origin_robtarget_name, origin, points[4])}, Offs {Figure.offset_coord(origin_robtarget_name, origin, points[5])}, v{self.velocity}, fine, {tool_name};\n")

        # Move to end point (lifted position)
        if not self.skip_end_lifting:
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[6])}, v{global_velocity}, fine, {tool_name};\n")
            instructions.append(f"        !end_lifted\n")

        return instructions