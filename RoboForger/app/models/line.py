from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtGui import QColor, QVector3D, QQuaternion


class Line(Qt3DCore.QEntity):
    def __init__(self, start: QVector3D, end: QVector3D, color: QColor, thickness: float, parent=None):
        super().__init__(parent)

        self.start = start
        self.end = end
        self.color = color
        self.thickness = thickness

        self.mesh = Qt3DExtras.QCylinderMesh()
        self.mesh.setRadius(self.thickness)
        self.mesh.setLength((end - start).length())
        self.addComponent(self.mesh)

        self.material = Qt3DExtras.QPhongMaterial()
        self.material.setAmbient(self.color)
        self.material.setDiffuse(QColor(0, 0, 0)) # ignore lighting effects
        self.material.setSpecular(QColor(0, 0, 0)) # ignore lighting effects
        self.addComponent(self.material)

        self.transform = Qt3DCore.QTransform()
        midpoint = QVector3D(
            (start.x() + end.x()) / 2.0,
            (start.y() + end.y()) / 2.0,
            (start.z() + end.z()) / 2.0,
        )
        self.transform.setTranslation(midpoint)

        default_cylinder_axis = QVector3D(0, 1, 0)
        target_direction = (end - start).normalized()
        
        rotation = QQuaternion.rotationTo(default_cylinder_axis, target_direction)
        self.transform.setRotation(rotation)

        self.addComponent(self.transform)


class Polyline(Qt3DCore.QEntity):
    def __init__(self, points: list[QVector3D], color: QColor, thickness: float, parent=None):
        super().__init__(parent)

        self.points = points
        self.color = color
        self.thickness = thickness

        self.line_entities = []

        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]

            line_segment = Line(start, end, color, self.thickness, self)
            self.line_entities.append(line_segment)