import numpy as np
from PySide6.QtGui import QVector3D
from PySide6.QtQml import QmlElement
from PySide6.QtQuick3D import QQuick3DGeometry
from PySide6.QtCore import Slot, QByteArray, Signal, Property

QML_IMPORT_NAME = "LineGeometry"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class LineGeometry(QQuick3DGeometry):

    _lines_data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lines_data = []  # [{'start': [x,y,z], 'end': [x,y,z]}]
        self._thickness = 0.1
        self._scale = 1.0
        self._lines_data_changed.connect(self._generate_geometry)
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
    def set_lines(self, lines_data):
        print("Setting lines data:", lines_data)
        if self._lines_data != lines_data:
            self._lines_data = lines_data
            self._lines_data_changed.emit()

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
        for line in self._lines_data:
            print('Processing line:', line)
            print('Start:', line['start'], 'End:', line['end'])
            start = self._to_vec3(line['start']) * self._scale
            end = self._to_vec3(line['end']) * self._scale
            positions.append(start)
            positions.append(end)

        if not positions:
            self.setVertexData(QByteArray())
            return

        pos_np = np.array([[p.x(), p.y(), p.z()] for p in positions], dtype=np.float32)
        vertex_data = pos_np.flatten()

        self.addAttribute(
            QQuick3DGeometry.Attribute.PositionSemantic,
            0,
            QQuick3DGeometry.Attribute.F32Type
        )

        self.setVertexData(QByteArray(vertex_data.tobytes()))
        self.setStride(3 * 4)  # only positions (x,y,z)
        self.setPrimitiveType(QQuick3DGeometry.PrimitiveType.LineStrip)

