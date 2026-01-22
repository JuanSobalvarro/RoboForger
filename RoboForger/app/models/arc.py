from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtGui import QColor, QVector3D

from RoboForger.app.models.line import Line

import numpy as np
import math


class Arc(Qt3DCore.QEntity):
    def __init__(self, center: QVector3D, radius: float, start_angle: float, end_angle: float, clockwise: bool, color: QColor, thickness: float, parent=None):
        super().__init__(parent)

        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
        self.clockwise = clockwise
        self.thickness = thickness

        self.line_entities = []

        if clockwise:
            # If going clockwise (decreasing angle), but start < end, 
            # we must wrap around 360 (2pi) to go "backwards"
            if self.start_angle < self.end_angle:
                self.start_angle += 2 * np.pi
        else:
            # If going counter-clockwise (increasing), but end < start,
            # we must wrap around to go "forwards"
            if self.end_angle < self.start_angle:
                self.end_angle += 2 * np.pi

        sweep = abs(self.end_angle - self.start_angle)
        
        # Determine segments based on size (adaptive resolution)
        # Minimal resolution of 4, max of 64
        num_segments = int(max(4, min(10, self.radius * sweep * 2)))
        
        # Generate the angles
        angles = np.linspace(self.start_angle, self.end_angle, num_segments)

        print(f"Number of segments for arc: {num_segments}, angles: {angles}")

        # --- 2. GENERATE POINTS ---
        points = []
        for angle in angles:
            x = self.center.x() + self.radius * math.cos(angle)
            y = self.center.y() + self.radius * math.sin(angle)
            z = self.center.z()
            points.append(QVector3D(x, y, z))

        # --- 3. CREATE LINE SEGMENTS ---
        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]

            line_segment = Line(start, end, color, self.thickness, self)
            self.line_entities.append(line_segment)

