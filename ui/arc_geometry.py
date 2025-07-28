import numpy as np
from PySide6.QtGui import QVector3D
from PySide6.QtQml import QmlElement
from PySide6.QtQuick3D import QQuick3DGeometry
from PySide6.QtCore import Slot, Signal, Property, QByteArray

QML_IMPORT_NAME = "ArcGeometry"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class ArcGeometry(QQuick3DGeometry):

    _arcs_data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._arcs_data = []
        self._thickness = 0.1
        self._scale = 1.0
        self._arcs_data_changed.connect(self._generate_geometry)
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
    def set_arcs(self, arcs_data):
        print("Setting arcs data:", arcs_data)
        if self._arcs_data != arcs_data:
            self._arcs_data = arcs_data
            self._arcs_data_changed.emit()

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

        # arcs data contains, center, radius, start_angle, end_angle, clockwise
        for arc in self._arcs_data:
            print('Processing arc:', arc)
            center = self._to_vec3(arc['center']) * self._scale
            radius = arc['radius']
            start_angle = np.deg2rad(arc['startAngle'])
            end_angle = np.deg2rad(arc['endAngle'])
            clockwise = arc['clockwise']

            # norm_start_angle = start_angle % (2 * np.pi)
            # norm_end_angle = end_angle % (2 * np.pi)

            # if norm_start_angle > norm_end_angle:
            #     clockwise = True

            print(f"Arc detected: Center={center}, Radius={radius}, StartAngle={start_angle}, EndAngle={end_angle}, Clockwise={clockwise}")

            # the number of segments should be propotional to the radius and the sweep angle( sweep max at 360)
            sweep_angle = abs(end_angle - start_angle)
            num_segments = int(radius * sweep_angle / np.pi * 10)
            if clockwise:
                if start_angle < end_angle:
                    start_angle += 2 * np.pi
                angles = np.linspace(start_angle, end_angle, num=num_segments)
            else:
                if end_angle < start_angle:
                    end_angle += 2 * np.pi
                angles = np.linspace(start_angle, end_angle, num=num_segments)

            for angle in angles:
                x = center.x() + radius * np.cos(angle) * self._scale
                y = center.y() + radius * np.sin(angle) * self._scale
                z = center.z()  # Assuming z is constant for arcs
                positions.append(QVector3D(x, y, z))

        if not positions:
            self.setVertexData(QByteArray())

        # print("Generated positions:", positions)

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
