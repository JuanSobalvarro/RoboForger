import numpy as np
from PySide6.QtGui import QVector3D
from PySide6.QtQml import QmlElement
from PySide6.QtQuick3D import QQuick3DGeometry
from PySide6.QtCore import Slot, Signal, Property, QByteArray

QML_IMPORT_NAME = "CircleGeometry"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class CircleGeometry(QQuick3DGeometry):
    _circles_data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._circles_data = []
        self._thickness = 0.1
        self._scale = 1.0
        self._circles_data_changed.connect(self._generate_geometry)
        self._generate_geometry()

    @Property(float)
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if self._thickness != value:
            self._thickness = value
            self._generate_geometry()

    @Property(float)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        if self._scale != value:
            self._scale = value
            self._generate_geometry()

    @Slot(list)
    def set_circles(self, circles_data):
        print("Setting circles data:", circles_data)
        if self._circles_data != circles_data:
            self._circles_data = circles_data
            self._circles_data_changed.emit()

    @staticmethod
    def _to_vec3(value):
        if isinstance(value, QVector3D):
            return value
        elif isinstance(value, (list, tuple)) and len(value) == 3:
            return QVector3D(*value)
        else:
            raise TypeError("Invalid point format, must be QVector3D or [x, y, z] list")

    def _generate_geometry(self):
        self.clear()

        positions = []

        for circle in self._circles_data:
            center = self._to_vec3(circle['center'])
            center = QVector3D(center.x() * self._scale, center.y() * self._scale, center.z() * self._scale)
            radius = circle['radius']

            num_segments = int(radius * 10)
            angles = np.linspace(0, 2 * np.pi, num_segments)

            for angle in angles:
                x = center.x() + radius * np.cos(angle) * self._scale
                y = center.y() + radius * np.sin(angle) * self._scale
                z = center.z() # Assuming z is constant for circles
                positions.append(QVector3D(x, y, z))

        if not positions:
            self.setVertexData(QByteArray())

        pos_np = np.array([[p.x(), p.y(), p.z()] for p in positions], dtype=np.float32)
        vertex_data = pos_np.flatten()

        self.addAttribute(
            QQuick3DGeometry.Attribute.PositionSemantic,
            0,
            QQuick3DGeometry.Attribute.F32Type
        )
        self.setVertexData(QByteArray(vertex_data.tobytes()))
        self.setStride(3 * 4)
        self.setPrimitiveType(QQuick3DGeometry.PrimitiveType.LineStrip)