from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtGui import QColor, QVector3D

from RoboForger.app.models.line import Polyline

import numpy as np
import math


class Arc(Qt3DCore.QEntity):
    """
    Class that draws an arc using multiple line segments. Currently only supports arcs in the XY plane.

    remmeber the logic for drawing the arc:
    Choose the angular step so that the maximum deviation between the true arc and the straight segment is <= chord_error. MAx dev aka saggita = r - sqrt(r^2 - (l/2)^2) where l is the chord length.

    Our method is based on the geometric definition of the sagitta of a circle segment.

    TODO: Support arcs in arbitrary planes.
    """
    def __init__(self, center: QVector3D, radius: float, start_angle: float, end_angle: float, clockwise: bool, color: QColor, thickness: float, rounded_corners: bool = False, parent=None):
        super().__init__(parent)

        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.clockwise = clockwise
        self.thickness = thickness
        self.rounded_corners = rounded_corners

        self.color = color

        self.polyline: Polyline | None = None

        self.draw_arc()

    def draw_arc(self):
        """
        So we know that to draw an arc we need to sample points along the arc and create a polyline from those points.

        We will do that using the saggita, for a chord error we calculate the angle step and then sample points along the arc.

        The steps are:
        1. Calculate the total angle of the arc.
        2. Determine the number of segments based on the radius and a desired chord error.
        3. Sample points along the arc at equal angle intervals.
        4. Create a polyline from those points.

        And thats it -.- it only took me a few months to figure it out :D
        """
        positions: list[QVector3D] = []
        
        sweep_angle = abs(self.end_angle - self.start_angle)
        # print(f"Sweep angle: {sweep_angle} radians.")

        # Desired chord error
        chord_error = 0.01  # in the same units as radius
        num_segments = int(sweep_angle / self.segment_angle(chord_error))

        if num_segments < 2:
            num_segments = 2

        if self.clockwise:
            if self.start_angle < self.end_angle:
                self.start_angle += (2 * np.pi)
            angles = np.linspace(self.start_angle, self.end_angle, num_segments)
        else:
            if self.end_angle < self.start_angle:
                self.end_angle += (2 * np.pi)
            angles = np.linspace(self.start_angle, self.end_angle, num_segments)

        for angle in angles:
            x = self.center.x() + self.radius * math.cos(angle)
            y = self.center.y() + self.radius * math.sin(angle)
            z = self.center.z() # Assuming arc is in XY plane
            positions.append(QVector3D(x, y, z))

        # print(f"Arc with {len(positions)} segments: {positions}")

        self.polyline = Polyline(positions, self.color, self.thickness, self.rounded_corners, self)

    def segment_angle(self, chord_error: float) -> float:
        """
        Calculate the angle step for a given chord error and radius.
        """
        if self.radius == 0:
            return 0.0
        angle = 2 * math.acos(1 - (chord_error / self.radius))
        return angle