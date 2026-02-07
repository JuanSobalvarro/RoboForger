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
    QByteArray,
)
from PySide6.QtGui import (
    QKeyEvent,
    QQuaternion,
    QVector3D,
    QColor,
    QFont,
)
from PySide6.QtQml import qmlRegisterType
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl

from RoboForger.app.preview.drawing.drawing import PreviewDrawing
from RoboForger.app.preview.drawing.polyline.geometry import PolylineGeometry, PolylineBatchGeometry
from RoboForger.app.preview.drawing.arc.geometry import ArcGeometry
from RoboForger.app.preview.drawing.circle.geometry import CircleGeometry

from RoboForger.drawing.figures import PolyLine as FPolyline, Arc as FArc, Circle as FCircle, BSpline as FBSpline, Figure

# from RoboForger.app.preview.camera import WASDCameraController
# from RoboForger.app.preview.overlay import PreviewOverlay

from RoboForger.utils import get_resource_path

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

        self.load_geometries_into_qml()

        self.preview_drawing = PreviewDrawing(
            grid_size=self.grid_size,
            grid_step=self.grid_step,
            parent=self
        )

        self.qml_widget = QQuickWidget()
        self.qml_widget.setParent(self)
        self.qml_widget.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.qml_widget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.load_models_into_qml()
        
        self.qml_widget.setSource(QUrl.fromLocalFile(get_resource_path("qml/PreviewScene.qml")))


        if self.qml_widget.status() != QQuickWidget.Status.Ready:
            for error in self.qml_widget.errors():
                logging.error(f"QML Error: {error.toString()}")
            raise RuntimeError("Failed to load PreviewScene.qml")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.qml_widget)


        self.setMinimumSize(200, 200)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

    def load_geometries_into_qml(self):
        qmlRegisterType(PolylineGeometry, "RoboForger.Geometries", 1, 0, "PolylineGeometry") # type: ignore
        qmlRegisterType(ArcGeometry, "RoboForger.Geometries", 1, 0, "ArcGeometry") # type: ignore
        qmlRegisterType(CircleGeometry, "RoboForger.Geometries", 1, 0, "CircleGeometry") # type: ignore
        qmlRegisterType(PolylineBatchGeometry, "RoboForger.Geometries", 1, 0, "PolylineBatchGeometry") # type: ignore

    def load_models_into_qml(self):
        self.qml_widget.rootContext().setContextProperty(
            "gridPolylineModel",
            self.preview_drawing.grid_polyline_model
        )
        self.qml_widget.rootContext().setContextProperty(
            "axisPolylineModel",
            self.preview_drawing.axis_polyline_model
        )
        self.qml_widget.rootContext().setContextProperty(
            "drawingPolylineModel",
            self.preview_drawing.drawing_polyline_model
        )
        self.qml_widget.rootContext().setContextProperty(
            "drawingArcModel",
            self.preview_drawing.drawing_arc_model
        )
        self.qml_widget.rootContext().setContextProperty(
            "drawingCircleModel",
            self.preview_drawing.drawing_circle_model
        )
        self.qml_widget.rootContext().setContextProperty(
            "limitsPolylineModel",
            self.preview_drawing.limits_polyline_model
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

    @Slot()
    def load_limits(
        self,
        limit1: QVector3D,
        limit2: QVector3D
    ):
        """Loads the workspace limits into the 3D preview."""
        self.preview_drawing.load_limits_square(limit1, limit2)