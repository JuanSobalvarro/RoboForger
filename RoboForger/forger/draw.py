from typing import Any, List, Tuple
from RoboForger.types import Point3D
from .figures.figure import Figure


class Draw:
    def __init__(self, tool_name: str = "tool0", velocity: int = 1000,
                 workspace_limits: Tuple[Point3D, Point3D] = ((-810.0, -810.0, 0.0), (810, 810, 0)),
                 zero: Point3D = (0.0, 0.0, 0.0)):
        self.figures: List[Figure] = []
        self.tool_name = tool_name
        self.velocity = velocity
        self.robtargets = []
        self.instructions = []
        self.workspace_limits = workspace_limits if workspace_limits else None  # (xmin, ymin, zmin), (xmax, ymax, zmax)
        self.zero = zero  # New origin offset

    def _is_within_limits(self, point: Point3D) -> bool:
        if not self.workspace_limits:
            return True
        (xmin, ymin, zmin), (xmax, ymax, zmax) = self.workspace_limits
        x, y, z = point
        return xmin <= x <= xmax and ymin <= y <= ymax and zmin <= z <= zmax

    def _generate_targets_and_moves(self):
        # Move to ZERO before starting the drawing
        if not self._is_within_limits(self.zero):
            raise ValueError(f"Zero point {self.zero} is outside the robot's workspace limits.")
        
        self.instructions.append(f"        MoveAbsJ ZERO\\NoEOffs, v{self.velocity}, fine, {self.tool_name};")
        
        if not self.figures:
            raise ValueError("No figures to draw. Please add at least one figure.")
        
        for fig in self.figures:
            # Comment line for the figure
            if not isinstance(fig, Figure):
                raise TypeError(f"Expected Figure instance, got {type(fig).__name__}.")
            
            self.instructions.append(f"\n        ! Figure: {fig.name}\n")


            # Write the instructions for moving through the figure
            fig_instructions = fig.move_instructions(self.tool_name, self.velocity)
            if not fig_instructions:
                raise ValueError(f"Figure {fig.name} has no move instructions defined.")

            for instruction in fig_instructions:  # Skip the first instruction which is the initial move
                self.instructions.append(instruction)

            self.instructions.append(f"\n")

            # Save the figure's robtargets
            self.robtargets.extend(f"    {rtf}" for rtf in fig.get_rob_targets_formatted())

        # Move to zero position after finishing the drawing
        self.instructions.append(f"        MoveAbsJ ZERO\\NoEOffs, v{self.velocity}, fine, {self.tool_name};")

    def add_figure(self, figure: Figure):
        self.figures.append(figure)

    def add_figures(self, figures: List[Figure]):
        if not isinstance(figures, list):
            raise TypeError("Expected a list of Figure instances.")
        self.figures.extend(figures)

    def generate_rapid_code(self) -> str:
        self.robtargets.clear()
        self.instructions.clear()
        self._generate_targets_and_moves()  # <-- use the internal method

        code = "MODULE MainModule\n"
        code += "    CONST jointtarget ZERO:=[[0,0,0,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];\n"
        code += "".join(self.robtargets)
        code += "\n\n    PROC main()\n"
        code += "".join(self.instructions)
        code += "\n    ENDPROC\nENDMODULE\n"
        return code

