from typing import List
from RoboForger.types import Point3D


class Figure:
    def __init__(self, name: str, points: List[Point3D], velocity: int = 1000):
        if not points or len(points) < 2:
            raise ValueError("A figure must have at least two points.")
        self.name = name
        self.target_count = 0
        self.velocity = velocity
        self.points = points.copy()

        self.rob_targets = []
        self.rob_targets_formatted = []

        self.__generate_rob_targets()

    def set_velocity(self, velocity: int):
        if velocity <= 0:
            raise ValueError("Velocity must be a positive integer.")
        self.velocity = velocity

    def get_points(self) -> List[Point3D]:
        return self.points

    # Override this method in subclasses to provide specific move instructions
    def move_instructions(self, tool_name: str = "tool0", global_velocity: int = 1000) -> List[str]:
        ...

    def get_rob_targets(self) -> List[str]:
        """
        Returns the list of all rob targets name in order of use
        """
        return self.rob_targets

    def clear_rob_targets(self):
        """
        Clears the rob targets list and resets the target count.
        This is useful if you want to regenerate the rob targets.
        """
        self.rob_targets.clear()
        self.rob_targets_formatted.clear()
        self.target_count = 0

    def get_rob_targets_formatted(self) -> List[str]:
        if not self.rob_targets_formatted:
            self.__generate_rob_targets()
        return self.rob_targets_formatted

    def create_robtarget(self, point: Point3D) -> str:
        """
        Creates a rob target string for a given point.
        This is useful for generating individual rob targets without generating the entire list.
        """
        target_name = self.__generate_target_name(self.target_count)
        self.target_count += 1
        return f"[[{point[0]},{point[1]},{point[2]}]," \
               f"[4.14816E-8,6.1133E-9,-1,-2.53589E-16],[0,0,-1,0]," \
               f"[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]]"

    def __generate_rob_targets(self):
        """
        This function generates the rob targets for the figure based on the points provided. It will generate a point lifted,
        a point at the start(down), movements of the figure**, then a point lifted at the end.
        """
        self.rob_targets.clear()
        self.rob_targets_formatted.clear()
        self.target_count = 0

        # Pre down point, this point is used as the pre starting point, the robot needs to move here and then down
        # This is useful for avoiding collisions with the workpiece or other obstacles
        start_lifted_point = (self.points[0][0], self.points[0][1], self.points[0][2] + 50)
        self.points.insert(0, start_lifted_point)
        # Append lift point to the end of the points list
        self.points.append(
            (self.points[-1][0], self.points[-1][1], self.points[-1][2] + 50))  # Lift the tool up by 50 units
        self.points.append(
            (self.points[-1][0], self.points[-1][1], self.points[-1][2] + 50))  # Lift the tool up by 50 units

        for point in self.get_points():
            target_name = self.__generate_target_name(self.target_count)
            self.rob_targets.append(target_name)

            self.rob_targets_formatted.append(
                f"CONST robtarget {target_name}:=[[{point[0]},{point[1]},{point[2]}],"
                f"[4.14816E-8,6.1133E-9,-1,-2.53589E-16],[0,0,-1,0],"
                f"[9E+9,9E+9,9E+9,9E+9,9E+9,9E+9]];\n"
            )
            self.target_count += 1
            # print("Generated robtarget:", target_name, "for point:", point)

        return self.rob_targets_formatted

    def __generate_target_name(self, count: int) -> str:
        return f"P{self.name}{count}"
