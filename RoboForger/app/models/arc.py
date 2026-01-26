from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtGui import QColor, QVector3D

from RoboForger.app.models.line import Line

import numpy as np
import math


class Arc(Qt3DCore.QEntity):
    """
    Class that draws an arc using multiple line segments. Currently only supports arcs in the XY plane.

    TODO: Support arcs in arbitrary planes.
    """
    def __init__(self, center: QVector3D, radius: float, start_angle: float, end_angle: float, clockwise: bool, color: QColor, thickness: float, parent=None):
        super().__init__(parent)

        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.clockwise = clockwise
        self.thickness = thickness

        self.color = color

        self.line_entities = []
        
        print("Drawing arc:", center, radius, start_angle, end_angle, clockwise)

        self.draw_arc()

    def draw_arc(self):
        positions: list[QVector3D] = []
        
        sweep_angle = abs(self.end_angle - self.start_angle)
        num_segments = int(self.radius * sweep_angle / 180 * 2) # idk why but it looks good haha
        # num_segments = 40

        if self.clockwise:
            if self.start_angle < self.end_angle:
                self.start_angle += 360
            angles = np.linspace(self.start_angle, self.end_angle, num_segments)
        else:
            if self.end_angle < self.start_angle:
                self.end_angle += 360
            angles = np.linspace(self.start_angle, self.end_angle, num_segments)

        for angle in angles:
            x = self.center.x() + self.radius * math.cos(math.radians(angle))
            y = self.center.y() + self.radius * math.sin(math.radians(angle))
            z = self.center.z() # Assuming arc is in XY plane
            positions.append(QVector3D(x, y, z))

        for i in range(len(positions) - 1):
            line = Line(positions[i], positions[i + 1], self.color, self.thickness, self)
            self.line_entities.append(line)
