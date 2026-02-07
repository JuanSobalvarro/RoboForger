from PySide6.QtCore import QObject, Signal, Property, QTimer
from PySide6.QtQml import QmlElement
from PySide6.QtQuick3D import QQuick3DGeometry
from PySide6.QtGui import QVector3D

from RoboForger.app.preview.drawing.polyline.geometry import PolylineGeometryBase

import math
import numpy as np

QML_IMPORT_NAME = "RoboForger.Geometries"
QML_IMPORT_MAJOR_VERSION = 1


class ArcDef:
    __slots__ = ("center", "radius", "start", "end", "clockwise")

    def __init__(self, center: QVector3D, radius: float, start: float, end: float, clockwise: bool = False):
        self.center = center
        self.radius = radius    
        self.start = start
        self.end = end
        self.clockwise = clockwise


@QmlElement
class ArcGeometry(PolylineGeometryBase):
    """
    Geometry class for drawing arcs. Generates points along an arc defined by a center, radius, start angle, and end angle, and clockwise.
    The arc is approximated using multiple line segments based on a desired chord error.

    Then we use the polyline geometry to define all the line segments.

    remmeber the logic for drawing the arc:
    Choose the angular step so that the maximum deviation between the true arc and the straight segment is <= chord_error. MAx dev aka saggita = r - sqrt(r^2 - (l/2)^2) where l is the chord length.

    Our method is based on the geometric definition of the sagitta of a circle segment.

    TODO: Support arcs in arbitrary planes.
    """

    pointsChanged = Signal()
    thicknessChanged = Signal()
    centerChanged = Signal()
    radiusChanged = Signal()
    startAngleChanged = Signal()
    endAngleChanged = Signal()
    clockwiseChanged = Signal()

    def __init__(self, parent: QQuick3DGeometry | None = None):
        super().__init__(parent)
        # polyline geometry to hold the arc points and thickness
        self._radial_segments = 12
        self._center = QVector3D(0, 0, 0)
        self._radius = 1.0
        self._start_angle = 0.0
        self._end_angle = math.pi / 2
        self._clockwise = False

        self._chord_error = 0.1  # maximum allowed chord error

        # cache
        self._segment_cache_key = (-1.0, -1.0)  # (radius, chord_error)
        self._segment_cache_value = 0.0  # segment angle

        # update flag
        self._dirty = False
        self._recalc_timer = QTimer()
        self._recalc_timer.setSingleShot(True)
        self._recalc_timer.timeout.connect(self._doRecalculate)

    def _scheduleRecalculate(self):
        if not self._dirty:
            self._dirty = True
            self._recalc_timer.start(0)  # schedule for next event loop iteration
        
    def _doRecalculate(self):
        self._dirty = False
        self.recalculateArcPoints()

    def get_center(self) -> QVector3D:
        return self._center
    
    def set_center(self, value: QVector3D):
        if self._center == value:
            return
        self._center = value
        self.centerChanged.emit()
        self._scheduleRecalculate()

    center = Property(QVector3D, get_center, set_center, notify=centerChanged)
    
    def get_radius(self) -> float:
        return self._radius
    
    def set_radius(self, value: float):
        if self._radius == value:
            return
        self._radius = value
        self.radiusChanged.emit()
        self._scheduleRecalculate()

    radius = Property(float, get_radius, set_radius, notify=radiusChanged)

    def get_start_angle(self) -> float:
        return self._start_angle
    
    def set_start_angle(self, value: float):
        if self._start_angle == value:
            return
        self._start_angle = value
        self.startAngleChanged.emit()
        self._scheduleRecalculate()

    start_angle = Property(float, get_start_angle, set_start_angle, notify=startAngleChanged)

    def get_end_angle(self) -> float:
        return self._end_angle
    
    def set_end_angle(self, value: float):
        if self._end_angle == value:
            return
        self._end_angle = value
        self.endAngleChanged.emit()
        self._scheduleRecalculate()

    end_angle = Property(float, get_end_angle, set_end_angle, notify=endAngleChanged)

    def get_clockwise(self) -> bool:
        return self._clockwise
    
    def set_clockwise(self, value: bool):
        if self._clockwise == value:
            return
        self._clockwise = value
        self.clockwiseChanged.emit()
        self._scheduleRecalculate()

    clockwise = Property(bool, get_clockwise, set_clockwise, notify=clockwiseChanged)

    def recalculateArcPoints(self):
        self.clear()

        if self._radius <= 0:
            return
        
        positions: list[QVector3D] = []
        sweep_angle = abs(self._end_angle - self._start_angle)

        num_segments = int(sweep_angle / self._segment_angle_cached())

        if num_segments < 2:
            num_segments = 2

        # local angles to not modify the original start/end angles
        start = self._start_angle
        end = self._end_angle

        if self._clockwise:
            if start < end:
                start += (2 * np.pi)
        else:
            if end < start:
                end += (2 * np.pi)
            
        angle_step = (end - start) / num_segments
        
        x_center = self._center.x()
        y_center = self._center.y()
        z_center = self._center.z()

        for i in range(num_segments + 1):
            positions.append(QVector3D(
                x_center + self._radius * math.cos(start + i * angle_step),
                y_center + self._radius * math.sin(start + i * angle_step),
                z_center
            ))

        # print(f"Arc with {len(positions)} segments: {positions}")

        self.set_points(positions)

    def _segment_angle_cached(self):
        key = (self._radius, self._chord_error)
        if key != self._segment_cache_key:
            self._segment_cache_key = key
            self._segment_cache_value = self.segment_angle()
        return self._segment_cache_value

    def segment_angle(self) -> float:
        """
        Calculate the angle step for a given chord error and radius.
        """
        if self._radius == 0:
            return 0.0
        div = 1 - (self._chord_error / self._radius)
        
        if div < -1:
            div = -1
        
        if div > 1:
            div = 1

        angle = 2 * math.acos(div)
        return angle


@QmlElement
class ArcBatchGeometry(PolylineGeometryBase):
    """
    Geometry class for drawing multiple arcs in a single geometry.

    CURRENTLY NOT USED.
    """

    arcsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._arcs: list[ArcDef] = []
        self._chord_error = 0.1

        self._segment_cache_key = (-1.0, -1.0)
        self._segment_cache_value = 0.0

    def clear_arcs(self):
        if not self._arcs:
            return
        self._arcs.clear()
        self.arcsChanged.emit()
        self.updateData()

    def add_arc(
        self,
        center: QVector3D,
        radius: float,
        start_angle: float,
        end_angle: float,
        clockwise: bool = False,
    ):
        self._arcs.append(
            ArcDef(center, radius, start_angle, end_angle, clockwise)
        )
        self.arcsChanged.emit()
        self.updateData()

    def updateData(self):
        """Override: build a single mesh from multiple arcs."""
        self.clear()

        positions = []
        normals = []
        indices = []

        min_v = QVector3D(float("inf"), float("inf"), float("inf"))
        max_v = QVector3D(float("-inf"), float("-inf"), float("-inf"))

        index_offset = 0

        for arc in self._arcs:
            points = self._build_arc_points(arc)
            index_offset = self._process_line_strip(
                points,
                positions,
                normals,
                indices,
                index_offset,
                min_v,
                max_v,
            )

        if positions:
            self.setBounds(min_v, max_v)
            self._upload(positions, normals, indices)

    def _build_arc_points(self, arc: ArcDef) -> list[QVector3D]:
        if arc.radius <= 0:
            return []

        start = arc.start
        end = arc.end

        if arc.clockwise:
            if start < end:
                start += 2 * math.pi
        else:
            if end < start:
                end += 2 * math.pi

        sweep = abs(end - start)
        seg_angle = self._segment_angle_cached(arc.radius)

        num_segments = max(2, int(sweep / seg_angle))
        step = (end - start) / num_segments

        cx, cy, cz = arc.center.x(), arc.center.y(), arc.center.z()

        return [
            QVector3D(
                cx + arc.radius * math.cos(start + i * step),
                cy + arc.radius * math.sin(start + i * step),
                cz,
            )
            for i in range(num_segments + 1)
        ]

    def _segment_angle_cached(self, radius: float) -> float:
        key = (radius, self._chord_error)
        if key != self._segment_cache_key:
            self._segment_cache_key = key
            self._segment_cache_value = self._segment_angle(radius)
        return self._segment_cache_value

    def _segment_angle(self, radius: float) -> float:
        if radius <= 0:
            return math.pi / 8

        div = 1.0 - (self._chord_error / radius)
        div = max(-1.0, min(1.0, div))
        return 2.0 * math.acos(div)
