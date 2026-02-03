from PySide6.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.QtGui import QColor, QVector3D
from PySide6.QtCore import QObject, Slot, Signal

from RoboForger.app.geometries.line import Polyline, PolylineSharedResources
from RoboForger.app.geometries.arc import Arc
from RoboForger.app.geometries.circle import Circle

from RoboForger.drawing.figures import PolyLine as FPolyline, Arc as FArc, Circle as FCircle, BSpline as FBSpline

from typing import List
import logging
import time

class PreviewDrawing(QObject):
    
    figuresLoaded = Signal()

    def __init__(self, grid_size: int = 1000, grid_step: int = 50, root_entity: Qt3DCore.QEntity | None = None, parent=None):

        super().__init__(parent)

        if root_entity is None:
            raise ValueError("A root_entity must be provided to PreviewDrawing.")
        
        self.grid_size = grid_size
        self.grid_step = grid_step

        self.root_entity = root_entity
        
        self.grid_entities: list[Qt3DCore.QEntity] = []

        self.shared_resources_pline = PolylineSharedResources(
            QColor("#0000ff"),
            0.5,
            True,
            self.root_entity
        )
        self.shared_resources_grid = PolylineSharedResources(
            QColor("#ffffff"),
            0.5,
            False,
            self.root_entity
        )
        self.shared_resources_arc = PolylineSharedResources(
            QColor("#00ff00"),
            0.5,
            True,
            self.root_entity
        )

        self.polylines: List[Polyline] = []
        self.arcs = []
        self.circles = []
        self.splines = []

        self.add_axis_and_grid()

    def clear_figures(self):
        for pline in self.polylines:
            pline.setParent(None) # type: ignore
        self.polylines.clear()

        for arc in self.arcs:
            arc.setParent(None)
        self.arcs.clear()

        for circle in self.circles:
            circle.setParent(None)
        self.circles.clear()

    @Slot(dict)
    def load_figures(self, figures: dict[str, List[FPolyline | FArc | FCircle | FBSpline]]):
        """
        This is highly coupled with the Forger data structures.

        Forger provides "RAW FIGURES" which is a dict of lists of raw entities.
        Take a look at forger.py for more details.
        """
        print("Loading figures into preview...")
        start_time = time.time()

        # clear previous entities
        self.clear_figures()

        polylines: List[FPolyline] = figures.get("polylines", []) # type: ignore
        arcs: List[FArc] = figures.get("arcs", []) # type: ignore
        circles: List[FCircle] = figures.get("circles", []) # type: ignore
        splines: List[FBSpline] = figures.get("splines", []) # type: ignore

        logging.info(f"Preview loading {len(polylines)} polylines, {len(arcs)} arcs, {len(circles)} circles, {len(splines)} splines.")

        for pline in polylines:
            points = [QVector3D(pt[0], pt[1], pt[2]) for pt in pline.get_points()[1:-1]]  # skip first and last (lifting)
            entity = Polyline(points, self.shared_resources_pline, self.root_entity)
            self.polylines.append(entity)

        logging.info(f"Loaded {len(self.polylines)} polylines into preview in {time.time() - start_time:.2f} seconds.")

        for arc in arcs:
            center = QVector3D(arc.center[0], arc.center[1], arc.center[2]) 
            entity = Arc(
                center,
                arc.radius,
                arc.start_angle,
                arc.end_angle,
                arc.clockwise,
                self.shared_resources_arc,
                self.root_entity
            )
            self.arcs.append(entity)

        logging.info(f"Loaded {len(self.arcs)} arcs into preview in {time.time() - start_time:.2f} seconds.")

        for circle in circles:
            center = QVector3D(circle.center[0], circle.center[1], circle.center[2])
            entity = Circle(
                center,
                circle.radius,
                QColor("#ffff00"),
                0.5,
                self.root_entity
            )
            self.circles.append(entity)

        # TODO: splines

        logging.info(f"Finished loading figures into preview in {time.time() - start_time:.2f} seconds.")
        
        self.figuresLoaded.emit()

    def add_axis_and_grid(self):
        self._create_grid()

        grid_thickness = 1.5

        # x axis
        x_start = QVector3D(-self.grid_size, 0, 0)
        x_end = QVector3D(self.grid_size, 0, 0)
        x_axis = Polyline([x_start, x_end], PolylineSharedResources(QColor("#ff0000"), 1.5, False, self.root_entity), self.root_entity)
        self.grid_entities.append(x_axis)
        # y axis
        y_start = QVector3D(0, -self.grid_size, 0)
        y_end = QVector3D(0, self.grid_size, 0)
        y_axis = Polyline([y_start, y_end], PolylineSharedResources(QColor("#00ff00"), 1.5, False, self.root_entity), self.root_entity)
        self.grid_entities.append(y_axis)
        # z axis
        z_start = QVector3D(0, 0, -self.grid_size)
        z_end = QVector3D(0, 0, self.grid_size)
        z_axis = Polyline([z_start, z_end], PolylineSharedResources(QColor("#0000ff"), 1.5, False, self.root_entity), self.root_entity)
        self.grid_entities.append(z_axis)

    def _create_grid(self):
        grid_color = QColor("#ffffff")
        thickness = 0.5
        
        for i in range(-self.grid_size, self.grid_size + 1, self.grid_step):
            # horizontal line
            start_h = QVector3D(-self.grid_size, i, 0)
            end_h = QVector3D(self.grid_size, i, 0)

            line_h = Polyline([start_h, end_h], self.shared_resources_grid, self.root_entity)
            
            self.grid_entities.append(line_h)

            # vertical line
            start_v = QVector3D(i, -self.grid_size, 0)
            end_v = QVector3D(i, self.grid_size, 0)
            
            line_v = Polyline([start_v, end_v], self.shared_resources_grid, self.root_entity)
            
            self.grid_entities.append(line_v)
