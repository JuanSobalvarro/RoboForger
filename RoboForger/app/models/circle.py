from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtGui import QVector3D
from PySide6.QtGui import QColor


class Circle(Qt3DCore.QEntity):
    def __init__(self, center: QVector3D, radius: float, color: QColor, thickness: float, parent=None):
        super().__init__(parent)

        self.center = center
        self.radius = radius
        self.color = color
        self.thickness = thickness

        # we can use a torus with a very small tube radius to simulate a circle
        self.torus_mesh = Qt3DExtras.QTorusMesh()
        self.torus_mesh.setRadius(self.radius)
        self.torus_mesh.setMinorRadius(self.thickness)
        self.torus_mesh.setRings(100)
        self.torus_mesh.setSlices(20)
        self.addComponent(self.torus_mesh)
        self.material = Qt3DExtras.QPhongMaterial(self)
        self.material.setAmbient(self.color)
        self.material.setDiffuse(QColor(0, 0, 0)) 
        self.material.setSpecular(QColor(0, 0, 0))
        self.addComponent(self.material)

        if parent:
            self.setParent(parent)
        
        self.transform = Qt3DCore.QTransform()
        self.addComponent(self.transform)
        self.transform.setTranslation(self.center)
        # self.transform.setRotationX(90)  # Rotate to lie in XY plane
        self.addComponent(self.transform)   
        