from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QColor, QVector3D, QQuaternion
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DInput import Qt3DInput
from PySide6.QtCore import Qt


class Preview(QWidget):
    def __init__(self):
        super().__init__()
        self.view = Qt3DExtras.Qt3DWindow()
        self.view.defaultFrameGraph().setClearColor(QColor("#000000"))

        container = QWidget.createWindowContainer(self.view, self)

        container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(container)

        self.root_entity = Qt3DCore.QEntity()
        self.view.setRootEntity(self.root_entity)

        self.camera = self.view.camera()
        self.camera.lens().setPerspectiveProjection(45.0, 16.0/9.0, 0.1, 1000.0)
        self.camera.setPosition(QVector3D(0, 0, 100))
        self.camera.setViewCenter(QVector3D(0, 0, 0))

        self.keyboard = Qt3DInput.QKeyboardDevice(self.root_entity)

        self.camera_controller = Qt3DExtras.QOrbitCameraController(self.root_entity, inversePan=True, inverseTilt=True, inverseXTranslate=True, inverseYTranslate=True)
        self.camera_controller.setCamera(self.camera)
        self.camera_controller.setLinearSpeed(100)
        self.camera_controller.setLookSpeed(180)

        self.input_settings = Qt3DInput.QInputSettings(self.root_entity)
        self.input_settings.setEventSource(self.view)
        self.root_entity.addComponent(self.input_settings)

        # universal lighting
        self.light_entity = Qt3DCore.QEntity(self.root_entity)
        self.light = Qt3DRender.QPointLight(self.light_entity)
        self.light.setColor(QColor("#ffffff"))
        self.light.setIntensity(1)
        self.light_entity.addComponent(self.light)
        self.light_transform = Qt3DCore.QTransform()
        self.light_transform.setTranslation(QVector3D(0, 50, 50))
        self.light_entity.addComponent(self.light_transform)

        # self.add_axis_and_grid()

        # test cube
        self.cube_entity = Qt3DCore.QEntity(self.root_entity)
        self.cube_mesh = Qt3DExtras.QCuboidMesh()
        self.cube_mesh.setXExtent(10)
        self.cube_mesh.setYExtent(10)
        self.cube_mesh.setZExtent(10)
        self.cube_entity.addComponent(self.cube_mesh)
        self.cube_material = Qt3DExtras.QPhongMaterial()
        self.cube_material.setDiffuse(QColor("#00FF00"))
        self.cube_entity.addComponent(self.cube_material)
        self.cube_transform = Qt3DCore.QTransform()
        self.cube_transform.setTranslation(QVector3D(0, 0, 0))
        self.cube_entity.addComponent(self.cube_transform)


    def add_axis_and_grid(self):
        # # X Axis (Red)
        # self._create_axis_arrow(
        #     "#FF0000", 20, 
        #     QQuaternion.fromAxisAndAngle(QVector3D(0, 0, 1), -90)
        # )
        # # Y Axis (Green)
        # self._create_axis_arrow(
        #     "#00FF00", 20, 
        #     QQuaternion()
        # )
        # # Z Axis (Blue)
        # self._create_axis_arrow(
        #     "#0000FF", 20, 
        #     QQuaternion.fromAxisAndAngle(QVector3D(1, 0, 0), 90)
        # )

        self._create_grid(size=50, step=5)

    def _create_axis_arrow(self, color, length, rotation):
        root = self.root_entity
        radius = 0.2
        cone_height = 2.0

        # Cylinder
        cylinder_entity = Qt3DCore.QEntity(root)
        mesh = Qt3DExtras.QCylinderMesh()
        mesh.setRadius(radius)
        mesh.setLength(length)
        
        material = Qt3DExtras.QPhongMaterial()
        material.setDiffuse(QColor(color))
        
        transform = Qt3DCore.QTransform()
        transform.setRotation(rotation)
        
        # FIX: Use rotatedVector() instead of * operator
        offset_vector = QVector3D(0, length / 2.0, 0)
        transform.setTranslation(rotation.rotatedVector(offset_vector))

        cylinder_entity.addComponent(mesh)
        cylinder_entity.addComponent(material)
        cylinder_entity.addComponent(transform)

        # Cone
        cone_entity = Qt3DCore.QEntity(root)
        cone_mesh = Qt3DExtras.QConeMesh()
        cone_mesh.setBottomRadius(radius * 3)
        cone_mesh.setLength(cone_height)
        
        cone_transform = Qt3DCore.QTransform()
        cone_transform.setRotation(rotation)
        
        # FIX: Use rotatedVector() instead of * operator
        cone_offset = QVector3D(0, length + (cone_height / 2.0), 0)
        cone_transform.setTranslation(rotation.rotatedVector(cone_offset))

        cone_entity.addComponent(cone_mesh)
        cone_entity.addComponent(material)
        cone_entity.addComponent(cone_transform)

    def _create_grid(self, size=50, step=5):
        grid_color = QColor("#ffffff")
        thickness = 0.05
        
        for i in range(-size, size + 1, step):
            self._create_grid_line(QVector3D(i, 0, 0), size*2, thickness, grid_color, True)
            self._create_grid_line(QVector3D(0, i, 0), size*2, thickness, grid_color, False)

    def _create_grid_line(self, position, length, thickness, color, is_vertical):
        entity = Qt3DCore.QEntity(self.root_entity)
        
        mesh = Qt3DExtras.QCylinderMesh()
        mesh.setRadius(thickness)
        mesh.setLength(length)
        
        material = Qt3DExtras.QPhongMaterial()
        material.setDiffuse(color)
        
        transform = Qt3DCore.QTransform()
        
        if is_vertical:
            transform.setTranslation(position)
        else:
            transform.setRotation(QQuaternion.fromAxisAndAngle(QVector3D(0, 0, 1), -90))
            transform.setTranslation(position)

        entity.addComponent(mesh)
        entity.addComponent(material)
        entity.addComponent(transform)