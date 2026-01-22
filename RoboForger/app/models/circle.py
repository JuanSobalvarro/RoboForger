from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras


class Circle(Qt3DCore.QEntity):
    def __init__(self, center: Qt3DCore.QEntity, radius: float, color: Qt3DExtras.QPhongMaterial, thickness: float, parent=None):
        super().__init__(parent)

        self.center = center
        self.radius = radius
        self.color = color
        self.thickness = thickness

        # TODO: Implement the 3D representation of the circle using Qt3D components