from .figure import Figure
from RoboForger.types import Point3D
from typing import List
from RoboForger.utils import vector_norm


class Circle(Figure):
    """
    A circle is a fusion of two arcs, one for the upper half and one for the lower half.
    """

    def __init__(self, name: str, center: Point3D, radius, lifting: float, velocity: int = 100, float_precision: int = 6, arc_threshold: float = 0.1):
        self.center = center
        self.radius = radius
        self.arc_threshold = arc_threshold
        # Round the center point to 4 decimal places
        center = tuple(round(coord, 4) for coord in center)
        super().__init__(name, [
            (center[0] - radius, center[1], center[2]),  # Start point
            (center[0], center[1] + radius, center[2]),  # Midpoint (top)
            (center[0] + radius, center[1], center[2]),  # Right point
            (center[0], center[1] - radius, center[2]),  # Midpoint (bottom)
            (center[0] - radius, center[1], center[2])  # End point (back to start)
        ], lifting, velocity, float_precision)

    def arc_too_small(self, start: Point3D, mid: Point3D, end: Point3D) -> int:
        """
        Returns -1 if the arc is too small start to mid, 1 if too small mid to end, and 0 if both segments are ok.
        """
        distance_start_mid = vector_norm((mid[0] - start[0], mid[1] - start[1], mid[2] - start[2]))
        distance_mid_end = vector_norm((end[0] - mid[0], end[1] - mid[1], end[2] - mid[2]))

        if distance_start_mid < self.arc_threshold:
            return -1
        elif distance_mid_end < self.arc_threshold:
            return 1

    def move_instructions(self, tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        instructions = []

        rob_target_names = self.get_rob_target_names()

        if not rob_target_names:
            raise ValueError("No robot targets generated for the circle.")

        if not self.skip_pre_down:
            instructions.append(f"        !init_lifted\n")
            # Move to the pre-down point
            instructions.append(
                f"        MoveJ {rob_target_names[0]}, v{global_velocity}, fine, {tool_name};\n"
            )

        # Move to start point (down)
        instructions.append(
            f"        MoveL {rob_target_names[1]}, v{global_velocity}, fine, {tool_name};\n"
        )

        # Create the upper half arc movement
        instructions.append(
            f"        MoveC {rob_target_names[2]}, {rob_target_names[3]}, v{self.velocity}, fine, {tool_name};\n"
        )
        # Create the lower half arc movement
        instructions.append(
            f"        MoveC {rob_target_names[4]}, {rob_target_names[5]}, v{self.velocity}, fine, {tool_name};\n"
        )

        if not self.skip_end_lifting:
            # Move to end point (lifted position)
            instructions.append(
                f"        MoveL {rob_target_names[-1]}, v{global_velocity}, fine, {tool_name};\n"
            )
            instructions.append(f"        !end_lifted\n")

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
        if self.arc_too_small(points[0], points[1], points[2]) != 0:
            instructions.append(f"        !arc_too_small\n")
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[2])}, v{self.velocity}, fine, {tool_name};\n")
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[3])}, v{self.velocity}, fine, {tool_name};\n")
        else:
            instructions.append(f"        MoveC Offs {Figure.offset_coord(origin_robtarget_name, origin, points[2])}, Offs {Figure.offset_coord(origin_robtarget_name, origin, points[3])}, v{self.velocity}, fine, {tool_name};\n")

        # Create the lower half arc movement
        if self.arc_too_small(points[2], points[3], points[4]) != 0:
            instructions.append(f"        !arc_too_small\n")
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[4])}, v{self.velocity}, fine, {tool_name};\n")
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[5])}, v{self.velocity}, fine, {tool_name};\n")
        else:
            instructions.append(f"        MoveC Offs {Figure.offset_coord(origin_robtarget_name, origin, points[4])}, Offs {Figure.offset_coord(origin_robtarget_name, origin, points[5])}, v{self.velocity}, fine, {tool_name};\n")

        # Move to end point (lifted position)
        if not self.skip_end_lifting:
            instructions.append(f"        MoveL Offs {Figure.offset_coord(origin_robtarget_name, origin, points[6])}, v{global_velocity}, fine, {tool_name};\n")
            instructions.append(f"        !end_lifted\n")

        return instructions