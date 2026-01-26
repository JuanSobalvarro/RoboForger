from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtGui import QColor, QVector3D, QQuaternion
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DInput import Qt3DInput
from PySide6.QtCore import (
    Qt,
    Signal,
    Slot,
)
from PySide6.QtGui import QMatrix3x3

from RoboForger.app.models.line import Line, Polyline
from RoboForger.app.models.arc import Arc
from RoboForger.app.models.circle import Circle

from typing import Any


class Preview(QWidget):
    def __init__(self, grid_size: int = 200, grid_step: int = 10):
        """
        A 3D preview widget using Qt3D.

        The plane is the XY plane, with Z being vertical since most robotics applications use Z as up.

        :param grid_size: The size of the grid to be displayed.
        :param grid_step: The step between grid lines.
        """
        super().__init__()

        self.grid_size: int = grid_size
        self.grid_step: int = grid_step

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

        self.camera_controller = Qt3DExtras.QFirstPersonCameraController(self.root_entity)
        # self.camera_controller = Qt3DExtras.QOrbitCameraController(self.root_entity, inversePan=True, inverseTilt=True, inverseXTranslate=True, inverseYTranslate=True)
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

        self.grid_entities: list[Qt3DCore.QEntity] = []

        self.add_axis_and_grid()

        self.lines = []
        self.arcs = []
        self.circles = []

    def clear_figures(self):
        for line in self.lines:
            line.setParent(None)
        self.lines.clear()

        for arc in self.arcs:
            arc.setParent(None)
        self.arcs.clear()

        for circle in self.circles:
            circle.setParent(None)
        self.circles.clear()

    @Slot(dict)
    def load_figures(self, figures: dict[str, list[dict[str, Any]]]):
        """
        This is highly coupled with the Forger data structures.

        Forger provides "RAW FIGURES" which is a dict of lists of raw entities.
        Take a look at forger.py for more details.
        """
        print("Loading figures into preview...")
        # clear previous entities
        self.clear_figures()

        raw_lines: list[dict] = figures.get("lines", [])
        raw_arcs: list[dict] = figures.get("arcs", [])
        raw_circles: list[dict] = figures.get("circles", [])

        for line in raw_lines:
            self.lines.append(
                Line(
                    QVector3D(*line["start"]),
                    QVector3D(*line["end"]),
                    QColor("#ffff00"),
                    0.2,
                    self.root_entity,
                )
            )

        print(f"Loaded {len(self.lines)} lines.")

        for arc in raw_arcs:
            center = arc["center"]
            radius = arc["radius"]
            start_angle = arc["start_angle"]
            end_angle = arc["end_angle"]
            clockwise = arc["clockwise"]
            self.arcs.append(
                Arc(QVector3D(*center), float(radius), float(start_angle), float(end_angle), bool(clockwise), QColor("#0000ff"), 0.2, self.root_entity)
            )

        print(f"Loaded {len(self.arcs)} arcs.")

        for circle in raw_circles:
            center = circle["center"]
            radius = circle["radius"]
            self.circles.append(
                Circle(QVector3D(*center), float(radius), QColor("#00ff00"), 0.2, self.root_entity)
            )

        print(f"Loaded {len(self.circles)} circles.")

    def add_axis_and_grid(self):
        self._create_grid()

        # x axis
        x_start = QVector3D(-self.grid_size, 0, 0)
        x_end = QVector3D(self.grid_size, 0, 0)
        x_axis = Line(x_start, x_end, QColor("#ff0000"), 0.1, self.root_entity)
        self.grid_entities.append(x_axis)
        # y axis
        y_start = QVector3D(0, -self.grid_size, 0)
        y_end = QVector3D(0, self.grid_size, 0)
        y_axis = Line(y_start, y_end, QColor("#00ff00"), 0.1, self.root_entity)
        self.grid_entities.append(y_axis)
        # z axis
        z_start = QVector3D(0, 0, -self.grid_size)
        z_end = QVector3D(0, 0, self.grid_size)
        z_axis = Line(z_start, z_end, QColor("#0000ff"), 0.1, self.root_entity)
        self.grid_entities.append(z_axis)

    def _create_grid(self):
        grid_color = QColor("#ffffff")
        thickness = 0.05
        
        for i in range(-self.grid_size, self.grid_size + 1, self.grid_step):
            # horizontal line
            start_h = QVector3D(-self.grid_size, i, 0)
            end_h = QVector3D(self.grid_size, i, 0)

            line_h = Line(start_h, end_h, grid_color, thickness, self.root_entity)
            
            self.grid_entities.append(line_h)

            # vertical line
            start_v = QVector3D(i, -self.grid_size, 0)
            end_v = QVector3D(i, self.grid_size, 0)
            
            line_v = Line(start_v, end_v, grid_color, thickness, self.root_entity)
            
            self.grid_entities.append(line_v)
