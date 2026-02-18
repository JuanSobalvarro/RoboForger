
from PySide6.QtQuick3D import QQuick3DGeometry
from PySide6.QtQml import QmlElement
from PySide6.QtCore import Property, Signal, Slot
from PySide6.QtGui import QVector3D

from RoboForger.app.preview.drawing.polyline.geometry import PolylineGeometryBase

import math

QML_IMPORT_NAME = "RoboForger.Geometries"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class CircleGeometry(PolylineGeometryBase):
    """
    Geometry class for drawing circles. Generates points along a circle defined by a center and radius.
    The circle is approximated using multiple line segments based on a desired chord error.
    """
    def __init__(self, parent: QQuick3DGeometry | None = None):
        super().__init__(parent)
        self._center = QVector3D(0, 0, 0)
        self._radius = 1.0
        self._axis1 = QVector3D(1, 0, 0)
        self._axis2 = QVector3D(0, 1, 0)

    def get_center(self) -> QVector3D:
        return self._center
    
    def set_center(self, value: QVector3D):
        self._center = value
        self.recalculateCircle()

    center = Property(QVector3D, get_center, set_center)

    def get_radius(self) -> float:
        return self._radius
    
    def set_radius(self, value: float):
        self._radius = value
        self.recalculateCircle()

    radius = Property(float, get_radius, set_radius)

    def recalculateCircle(self):
        self.clear()
        
        chord_error = 0.01  # maximum allowable chord error
        if self._radius <= 0:
            return

        # Calculate the number of segments needed based on chord error
        segment_angle = 2 * math.acos(1 - chord_error / self._radius)
        num_segments = max(12, int(math.ceil(2 * math.pi / segment_angle)))

        positions = []
        normals = []
        indices = []

        for i in range(num_segments):
            angle1 = (i / num_segments) * 2 * math.pi
            angle2 = ((i + 1) % num_segments / num_segments) * 2 * math.pi

            p1 = self._center + self._axis1 * (self._radius * math.cos(angle1)) + self._axis2 * (self._radius * math.sin(angle1))
            p2 = self._center + self._axis1 * (self._radius * math.cos(angle2)) + self._axis2 * (self._radius * math.sin(angle2))

            positions.append(p1)
            positions.append(p2)

            normal = QVector3D.crossProduct(self._axis1, self._axis2).normalized()
            normals.append(normal)
            normals.append(normal)

            idx = i * 2
            indices.append(idx)
            indices.append(idx + 1)
            indices.append((idx + 2) % (num_segments * 2))

        self.set_points(positions)