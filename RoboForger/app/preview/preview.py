from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QSizePolicy,
    QGridLayout,
    QLabel,
    QPushButton,
    QStackedLayout,
)
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DInput import Qt3DInput
from PySide6.Qt3DLogic import Qt3DLogic
from PySide6.QtCore import (
    Qt,
    Signal,
    Slot,
    QEvent,
    QObject,
    QPoint,
)
from PySide6.QtGui import (
    QKeyEvent,
    QQuaternion,
    QVector3D,
    QColor,
    QFont,
)

from RoboForger.app.preview.drawing import PreviewDrawing
from RoboForger.drawing.figures import PolyLine as FPolyline, Arc as FArc, Circle as FCircle, BSpline as FBSpline, Figure

from RoboForger.app.geometries.line import Polyline, PolylineSharedResources
from RoboForger.app.geometries.arc import Arc
from RoboForger.app.geometries.circle import Circle

from RoboForger.app.preview.camera import WASDCameraController
from RoboForger.app.preview.overlay import PreviewOverlay

from typing import Any, List, Dict
import logging
import time


class Preview(QWidget):
    def __init__(self, grid_size: int = 1000, grid_step: int = 50, parent=None):
        """
        A 3D preview widget using Qt3D.

        Coordinate system:
        - X, Y plane = ground
        - Z = up (robotics convention)
        """
        super().__init__(parent)

        self.grid_size = grid_size
        self.grid_step = grid_step

        self.view = Qt3DExtras.Qt3DWindow()
        self.view.defaultFrameGraph().setClearColor(QColor("#101010"))

        self.container = self.createWindowContainer(self.view)
        # self.container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # self.container.setSizePolicy(
        #     QSizePolicy.Policy.Expanding,
        #     QSizePolicy.Policy.Expanding
        # )

        self.overlay = PreviewOverlay(self.container)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.container)

        self.setMinimumSize(200, 200)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # scene
        self.root_entity = Qt3DCore.QEntity()
        self.view.setRootEntity(self.root_entity)

        # camera
        self.camera = self.view.camera()
        self.camera.lens().setPerspectiveProjection(
            45.0,
            16.0 / 9.0,   # updated dynamically later
            0.1,
            5000.0
        )

        self.camera.setPosition(QVector3D(0, 0, 2000))
        self.camera.setViewCenter(QVector3D(0, 0, 0))

        self.input_settings = Qt3DInput.QInputSettings(self.root_entity)
        self.input_settings.setEventSource(self.view)
        self.root_entity.addComponent(self.input_settings)

        self.keyboard_device = Qt3DInput.QKeyboardDevice(self.root_entity)
        self.mouse_device = Qt3DInput.QMouseDevice(self.root_entity)

        self.wasd_controller = WASDCameraController(
            150.0,
            self.camera,
            self.keyboard_device,
            self.mouse_device,
            self.root_entity
        )

        self.preview_drawing = PreviewDrawing(
            grid_size=self.grid_size,
            grid_step=self.grid_step,
            root_entity=self.root_entity,
            parent=self
        )

        self.preview_drawing.figuresLoaded.connect(self.update_overlay_stats)

        self.update_overlay_stats()

    def update_camera_coords(self):
        """Called whenever the camera moves."""
        pos = self.camera.position()
        self.overlay.set_camera_position(pos.x(), pos.y(), pos.z())

    def reset_camera_position(self):
        """Resets camera to default home position."""
        self.camera.setPosition(QVector3D(0, 0, 2000))
        self.camera.setViewCenter(QVector3D(0, 0, 0))
        self.camera.setUpVector(QVector3D(0, 1, 0))

    def update_overlay_stats(self):
        """Pushes current counts to the overlay."""
        self.overlay.set_stats(
            polylines=len(self.preview_drawing.polylines),
            arcs=len(self.preview_drawing.arcs),
            circles=len(self.preview_drawing.circles),
            splines=len(self.preview_drawing.splines)
        )

    @Slot()
    def load_figures(
        self,
        figures: List[Figure]
    ):
        """Loads figures into the 3D preview."""
        self.preview_drawing.load_figures(
            figures
        )