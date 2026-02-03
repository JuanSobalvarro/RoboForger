from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtGui import QColor, QVector3D, QQuaternion

from typing import Tuple

class PolylineSharedResources:
    """
    Holds shared resources (Meshes, Materials) to optimize memory usage.
    Instantiate ONCE and pass to multiple Polyline instances.
    """
    def __init__(self, color: QColor = QColor("#0000ff"), thickness: float = 0.1, rounded_corners: bool = False, parent: Qt3DCore.QEntity | None = None):

        if parent is None:
            raise ValueError("Parent entity must be provided for shared resources. This ensures proper scene graph hierarchy.")
        
        self.parent = parent

        self._color = color
        self._thickness = thickness
        self._rounded_corners = rounded_corners
        
        self._material = self._generate_material(color)
        self._line_mesh, self._sphere_mesh = self._generate_meshes()

    def _generate_material(self, color: QColor) -> Qt3DExtras.QPhongMaterial:
        material = Qt3DExtras.QPhongMaterial(self.parent)
        material.setAmbient(color)
        material.setDiffuse(QColor("#000000"))
        material.setSpecular(QColor("#000000"))
        return material
    
    def _generate_meshes(self) -> Tuple[Qt3DExtras.QCylinderMesh, Qt3DExtras.QSphereMesh]:
        line_mesh = Qt3DExtras.QCylinderMesh(self.parent)
        line_mesh.setRadius(0.5) 
        line_mesh.setLength(1.0)
        line_mesh.setRings(10)
        line_mesh.setSlices(12)
        
        sphere_mesh = Qt3DExtras.QSphereMesh(self.parent)
        sphere_mesh.setRadius(0.5)
        sphere_mesh.setRings(10)
        sphere_mesh.setSlices(10)
        
        return line_mesh, sphere_mesh
    
    def get_material(self) -> Qt3DExtras.QPhongMaterial: return self._material
    def get_line_mesh(self) -> Qt3DExtras.QCylinderMesh: return self._line_mesh
    def get_sphere_mesh(self) -> Qt3DExtras.QSphereMesh: return self._sphere_mesh
    def get_thickness(self) -> float: return self._thickness
    def get_rounded_corners(self) -> bool: return self._rounded_corners


class Polyline(Qt3DCore.QEntity):
    def __init__(self, 
                 points: list[QVector3D],
                 shared_resources: PolylineSharedResources,
                 parent: Qt3DCore.QEntity):
        super().__init__(parent)

        if len(points) < 2:
            return
        
        self.shared = shared_resources
        
        # ALWAYS REMEMBER PLEASE, python does garbage collection so keep it in memory

        self.segments = [] 
        self.sphere_entities = []

        self.transforms = []

        if self.shared.get_rounded_corners():
            for point in points:
                sphere_entity = Qt3DCore.QEntity(self)
                
                transform = Qt3DCore.QTransform()
                transform.setTranslation(point)

                t = self.shared.get_thickness()
                transform.setScale3D(QVector3D(t, t, t)) 

                sphere_entity.addComponent(self.shared.get_sphere_mesh())
                sphere_entity.addComponent(self.shared.get_material())
                sphere_entity.addComponent(transform)
                
                self.sphere_entities.append(sphere_entity)

        for i in range(len(points) - 1):
            self._create_segment(points[i], points[i + 1])

    def _create_segment(self, p0: QVector3D, p1: QVector3D):
        direction = p1 - p0
        length = direction.length()

        if length < 0.0001: return

        segment = Qt3DCore.QEntity(self)
        transform = Qt3DCore.QTransform()
        
        t = self.shared.get_thickness()
        transform.setScale3D(QVector3D(t, length, t))
        
        transform.setRotation(QQuaternion.rotationTo(QVector3D(0, 1, 0), direction.normalized()))
        
        midpoint = (p0 + p1) * 0.5
        transform.setTranslation(midpoint)

        segment.addComponent(self.shared.get_line_mesh())
        segment.addComponent(self.shared.get_material())
        segment.addComponent(transform)

        self.segments.append(segment)
        self.transforms.append(transform)
