from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.QtGui import QColor, QVector3D, QQuaternion

from math import sqrt


# ------------------------------------------------------------
# Math helpers
# ------------------------------------------------------------

def normalize(v: QVector3D) -> QVector3D:
    l = sqrt(v.x() * v.x() + v.y() * v.y() + v.z() * v.z())
    if l == 0.0:
        return QVector3D(0, 0, 0)
    return QVector3D(v.x() / l, v.y() / l, v.z() / l)


# ------------------------------------------------------------
# Polyline as Cylinders
# ------------------------------------------------------------

class Polyline(Qt3DCore.QEntity):
    def __init__(self, points: list[QVector3D], color: QColor, thickness: float = 0.1, rounded_corners: bool = False, parent=None):
        super().__init__(parent)

        if len(points) < 2:
            return

        # shared resouces across the multiple segments to optimize memory usage
        self.material = Qt3DExtras.QPhongMaterial(self)
        self.material.setDiffuse(color)
        self.material.setAmbient(color)
        self.material.setSpecular(QColor("black"))

        self.mesh = Qt3DExtras.QCylinderMesh(self)
        self.mesh.setRings(10)
        self.mesh.setSlices(12)

        self.transform_list = []
        self.sphere_transforms = []

        # shared sphere mesh
        self.sphere_mesh = Qt3DExtras.QSphereMesh(self)
        self.sphere_mesh.setRings(10)
        self.sphere_mesh.setSlices(10)
        self.sphere_mesh.setRadius(thickness)

        self.sphere_entities = []

        # if rounded corners means that we should put a sphere at each point
        if rounded_corners:

            for point in points:
                sphere_entity = Qt3DCore.QEntity(self)

                sphere_transform = Qt3DCore.QTransform()
                sphere_transform.setTranslation(point)
                self.sphere_transforms.append(sphere_transform)

                sphere_entity.addComponent(self.sphere_mesh)
                sphere_entity.addComponent(self.material)
                sphere_entity.addComponent(sphere_transform)
                self.sphere_entities.append(sphere_entity)

        # Generate Segments
        for i in range(len(points) - 1):
            self._create_segment(points[i], points[i + 1], thickness)

    def _create_segment(self, p0: QVector3D, p1: QVector3D, thickness: float):
        # Calculate vector math
        direction = p1 - p0
        length = direction.length()

        # if length < 0.0001:
        #     return

        segment = Qt3DCore.QEntity(self)
        transform = Qt3DCore.QTransform()
        
        transform.setScale3D(QVector3D(thickness, length, thickness))
        
        transform.setRotation(QQuaternion.rotationTo(QVector3D(0, 1, 0), direction.normalized()))
        
        midpoint = (p0 + p1) * 0.5
        transform.setTranslation(midpoint)

        self.transform_list.append(transform)

        segment.addComponent(self.mesh)
        segment.addComponent(self.material)
        segment.addComponent(transform)
