from PySide6.QtGui import QColor, QVector3D
from PySide6.QtCore import QObject, Slot, Signal

from RoboForger.app.preview.drawing.polyline.model import PolylineListModel
from RoboForger.app.preview.drawing.arc.model import ArcListModel
from RoboForger.app.preview.drawing.circle.model import CircleListModel

from RoboForger.drawing.figures import PolyLine as FPolyline, Arc as FArc, Circle as FCircle, BSpline as FBSpline

from typing import List
import logging
import time


class PreviewDrawing(QObject):
    
    figuresLoaded = Signal()

    def __init__(self, grid_size: int = 1000, grid_step: int = 50, parent=None):

        super().__init__(parent)
        
        self.grid_size = grid_size
        self.grid_step = grid_step

        # self.grid_polyline_model = PolylineBatchModel(self)
        self.grid_polyline_model = PolylineListModel(self)
        self.axis_polyline_model = PolylineListModel(self)
        self.drawing_polyline_model = PolylineListModel(self)
        self.drawing_arc_model = ArcListModel(self)
        self.drawing_circle_model = CircleListModel(self)
        self.limits_polyline_model = PolylineListModel(self)
        self.splines = []

        self.add_axis_and_grid()

    def clear_figures(self):
        self.drawing_polyline_model.clear()
        self.drawing_arc_model.clear()
        self.drawing_circle_model.clear()

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
            self.drawing_polyline_model.add_polyline(
                points,
                color=QColor("#0000ff"),
                thickness=1
            )
        

        logging.info(f"Loaded {self.drawing_polyline_model.rowCount()} polylines into preview in {time.time() - start_time:.2f} seconds.")

        for arc in arcs:
            center = QVector3D(arc.center[0], arc.center[1], arc.center[2]) 
            self.drawing_arc_model.add_arc(
                center,
                arc.radius,
                arc.start_angle,
                arc.end_angle,
                arc.clockwise,
                QColor("#00ff00"),
                1
            )

        logging.info(f"Loaded {self.drawing_arc_model.rowCount()} arcs into preview in {time.time() - start_time:.2f} seconds.")

        for circle in circles:
            center = QVector3D(circle.center[0], circle.center[1], circle.center[2])
            self.drawing_circle_model.add_circle(
                center,
                circle.radius,
                QColor("#ffff00"),
                1
            )

        # TODO: splines

        logging.info(f"Finished loading figures into preview in {time.time() - start_time:.2f} seconds.")
        
        self.figuresLoaded.emit()

    def add_axis_and_grid(self):
        self._create_grid()

        grid_thickness = 4

        # x axis
        x_start = QVector3D(-self.grid_size, 0, 0)
        x_end = QVector3D(self.grid_size, 0, 0)
        self.axis_polyline_model.add_polyline(
            [x_start, x_end],
            color=QColor("#ff0000"),
            thickness=grid_thickness
        )
        # y axis
        y_start = QVector3D(0, -self.grid_size, 0)
        y_end = QVector3D(0, self.grid_size, 0)
        self.axis_polyline_model.add_polyline(
            [y_start, y_end],
            color=QColor("#00ff00"),
            thickness=grid_thickness
        )
        # z axis
        z_start = QVector3D(0, 0, -self.grid_size)
        z_end = QVector3D(0, 0, self.grid_size)
        self.axis_polyline_model.add_polyline(
            [z_start, z_end],
            color=QColor("#0000ff"),
            thickness=grid_thickness
        )

    def _create_grid(self):
        grid_color = QColor("#888888")
        thickness = 2
        
        points = []
        for i in range(-self.grid_size, self.grid_size + 1, self.grid_step):
            # horizontal line
            start_h = QVector3D(-self.grid_size, i, 0)
            end_h = QVector3D(self.grid_size, i, 0)

            # horizontal line
            points.append((start_h, end_h))   

            # vertical line
            start_v = QVector3D(i, -self.grid_size, 0)
            end_v = QVector3D(i, self.grid_size, 0)
            
            points.append((start_v, end_v))

            self.grid_polyline_model.add_polyline(
                [start_h, end_h],
                color=grid_color,
                thickness=thickness
            )

            self.grid_polyline_model.add_polyline(
                [start_v, end_v],
                color=grid_color,
                thickness=thickness
            )

        # self.grid_polyline_model.add_batch(
        #     [[p[0], p[1]] for p in points],
        #     color=grid_color,
        #     thickness=thickness
        # )
    
    @Slot(QVector3D, QVector3D)
    def load_limits_square(self, vector1: QVector3D, vector2: QVector3D):
        # clear previous limits
        self.limits_polyline_model.clear()

        # create a square with the two vectors as diagonal
        v1 = vector1
        v2 = vector2
        v3 = QVector3D(vector1.x(), vector2.y(), 0)
        v4 = QVector3D(vector2.x(), vector1.y(), 0)

        self.limits_polyline_model.add_polyline(
            [v1, v3, v2, v4, v1],
            color=QColor("#ff6600"),
            thickness=2
        )