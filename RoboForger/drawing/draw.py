"""
RoboForger - Draw Module
This module provides the Draw class that is used to generate Rapid Code for robotic drawing tasks given some figures and
parameters such as tool name, velocity, workspace limits, origin, and zero point.
Draw 'draws' the figures one after another, if detector is enabled it will unify figures that are close to each other
"""
from typing import Any, List, Tuple
from RoboForger.types import Point3D
from .figures.figure import Figure
from RoboForger.detector.detector import Detector


class Draw:
    def __init__(self, tool_name: str = "tool0", velocity: int = 1000,
                 workspace_limits: Tuple[Point3D, Point3D] = ((-810.0, -810.0, 0.0), (810, 810, 0)),
                 origin: Point3D = (450.0, 0.0, 450.0), zero: Point3D = (0.0, 0.0, 0.0), use_detector: bool = True):
        self.figures: List[Figure] = []
        self.tool_name = tool_name
        self.velocity = velocity
        self.robtargets = []
        self.instructions = []
        self.workspace_limits = workspace_limits if workspace_limits else None  # (xmin, ymin, zmin), (xmax, ymax, zmax)
        self.origin = origin
        self.zero = zero  # zero point for the robot
        self.use_detector = use_detector

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

        self.instructions.clear()
        self.robtargets.clear()
        
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

    def _generate_targets_and_moves_offset(self) -> List[str]:

        figures = []

        if self.use_detector:
            detector = Detector(self.figures)
            figures = detector.detect_and_simplify()
        else:
            figures = self.figures

        self.instructions.clear()
        self.robtargets.clear()

        if not figures:
            raise ValueError("No figures to draw. Please add at least one figure.")

        # First move to zero
        self.instructions.append(f"        ! Move to ZERO before starting the drawing\n")
        self.instructions.append(f"        MoveAbsJ ZERO\\NoEOffs, v{self.velocity}, fine, {self.tool_name};\n\n")

        # Since we are using offsets the first rob target will be the origin point
        self.robtargets = [f"    {Figure.rob_target_format("origin", self.origin)}\n"]

        self.instructions.append(f"        ! Move to origin point\n")
        self.instructions.append(f"        MoveJ {"origin"}, v{self.velocity}, fine, {self.tool_name};\n\n")

        # First figure will be the origin point, so we need to move to it first with robtarget, so the first instruction of the
        # first figure will be the MoveJ to the origin point (no offset)
        self.instructions.append(f"        ! Figure: {figures[0].name}\n")
        first_fig_instructions = figures[0].move_instructions_offset(origin_robtarget_name="origin",
                                                                            origin=self.origin,
                                                                            tool_name=self.tool_name,
                                                                            global_velocity=self.velocity)

        self.instructions.extend(first_fig_instructions)

        # For each figure append its instructions to the instructions list
        for fig in figures[1:]:

            self.instructions.append(f"\n        ! Figure: {fig.name}\n")

            self.instructions.extend(fig.move_instructions_offset(origin_robtarget_name="origin",
                                                                    origin=self.origin,
                                                                    tool_name=self.tool_name,
                                                                    global_velocity=self.velocity))

        # Move to origin
        self.instructions.append(f"\n        ! Move to origin point after finishing the drawing\n")
        self.instructions.append(f"        MoveJ {"origin"}, v{self.velocity}, fine, {self.tool_name};\n")

        # Remember to move to the zero position after finishing the drawing
        self.instructions.append(f"        MoveAbsJ ZERO\\NoEOffs, v{self.velocity}, fine, {self.tool_name};")

    def add_figure(self, figure: Figure):
        self.figures.append(figure)

    def add_figures(self, figures: List[Figure]):
        if not isinstance(figures, list):
            raise TypeError("Expected a list of Figure instances.")
        self.figures.extend(figures)

    def generate_rapid_code(self, use_offset: bool) -> str:
        self.robtargets.clear()
        self.instructions.clear()

        if use_offset:
            self._generate_targets_and_moves_offset()
        else:
            self._generate_targets_and_moves()

        code = "MODULE MainModule\n"
        code += "    CONST jointtarget ZERO:=[[0,0,0,0,0,0],[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];\n"
        code += "".join(self.robtargets)
        code += "\n\n    PROC main()\n"
        code += "".join(self.instructions)
        code += "\n    ENDPROC\nENDMODULE\n"
        return code

