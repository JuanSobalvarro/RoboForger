from PySide6.QtQuick3D import QQuick3DGeometry, QQuick3DObject
from PySide6.QtGui import QVector3D, QQuaternion
from PySide6.QtCore import QByteArray, Property, Signal
from PySide6.QtQml import QmlElement

import struct
import math
from typing import List

QML_IMPORT_NAME = "RoboForger.Geometries"
QML_IMPORT_MAJOR_VERSION = 1

class PolylineGeometryBase(QQuick3DGeometry):
    """
    Base class containing the math to generate cylinder meshes.
    Refactored to allow generating single OR multiple lines.
    """
    
    pointsChanged = Signal()
    thicknessChanged = Signal()

    def __init__(self, parent: QQuick3DObject | None = None):
        super().__init__(parent)
        self._points: List[QVector3D] = []
        self._thickness = 1.0
        self._radial_segments = 12
    
    def get_points(self) -> List[QVector3D]: 
        return self._points
    
    def set_points(self, points: List[QVector3D]):
        if self._points == points: return
        self._points = points
        self.pointsChanged.emit()
        self.updateData() 

    points = Property(list, get_points, set_points, notify=pointsChanged)

    def get_thickness(self): return self._thickness
    def set_thickness(self, value: float):
        if self._thickness == value: return
        self._thickness = value
        self.thicknessChanged.emit()
        self.updateData()

    thickness = Property(float, get_thickness, set_thickness, notify=thicknessChanged)

    def _process_line_strip(self, points: List[QVector3D], 
                            positions: list, normals: list, indices: list, 
                            current_index_offset: int,
                            min_v: QVector3D, max_v: QVector3D) -> int:
        """
        Generates cylinders for a single strip of points and APPENDS them to the lists.
        Returns the new index_offset.
        """
        if len(points) < 2:
            return current_index_offset

        for i in range(len(points) - 1):
            p0 = points[i]
            p1 = points[i + 1]

            direction = p1 - p0
            length = direction.length()
            if length < 1e-5: continue

            direction.normalize()
            rotation = QQuaternion.rotationTo(QVector3D(0, 1, 0), direction)
            center = (p0 + p1) * 0.5

            cyl_pos, cyl_norm, cyl_idx = self._build_cylinder_segment(
                length, rotation, center, self._thickness * 0.5
            )

            # Update Bounds (In-place modification of min_v/max_v)
            for v in cyl_pos:
                min_v.setX(min(min_v.x(), v.x()))
                min_v.setY(min(min_v.y(), v.y()))
                min_v.setZ(min(min_v.z(), v.z()))
                max_v.setX(max(max_v.x(), v.x()))
                max_v.setY(max(max_v.y(), v.y()))
                max_v.setZ(max(max_v.z(), v.z()))

            positions.extend(cyl_pos)
            normals.extend(cyl_norm)
            # Offset the indices for this specific segment
            indices.extend([idx + current_index_offset for idx in cyl_idx])
            
            current_index_offset += len(cyl_pos)

        return current_index_offset

    def updateData(self):
        """Default implementation for single polyline."""
        self.clear()
        
        # Buffers
        positions = []
        normals = []
        indices = []
        
        # Bounds
        min_v = QVector3D(float('inf'), float('inf'), float('inf'))
        max_v = QVector3D(float('-inf'), float('-inf'), float('-inf'))

        # Process the single strip
        self._process_line_strip(self._points, positions, normals, indices, 0, min_v, max_v)

        self.setBounds(min_v, max_v)
        self._upload(positions, normals, indices)


    def _build_cylinder_segment(self, height, rotation, translation, radius):
        pos = []
        norm = []
        idx = []

        h = height * 0.5
        steps = self._radial_segments

        for i in range(steps):
            a0 = 2.0 * math.pi * i / steps
            a1 = 2.0 * math.pi * (i + 1) / steps

            # Precompute circle coordinates (XZ plane)
            x0, z0 = math.cos(a0) * radius, math.sin(a0) * radius
            x1, z1 = math.cos(a1) * radius, math.sin(a1) * radius

            # Vertices for the quad face (Side of cylinder)
            v0 = QVector3D(x0, -h, z0) # Bottom-Left
            v1 = QVector3D(x0, +h, z0) # Top-Left
            v2 = QVector3D(x1, +h, z1) # Top-Right
            v3 = QVector3D(x1, -h, z1) # Bottom-Right

            # Normals (Pointing out from center)
            n0 = QVector3D(x0, 0, z0).normalized()
            n1 = QVector3D(x1, 0, z1).normalized()

            verts = [v0, v1, v2, v3]
            norms = [n0, n0, n1, n1]

            base = len(pos)

            # Apply Transform (Rotate & Translate)
            for v, n in zip(verts, norms):
                v_trans = rotation.rotatedVector(v) + translation
                n_trans = rotation.rotatedVector(n)
                pos.append(v_trans)
                norm.append(n_trans)

            # Standard Quad Indexing (Two triangles)
            idx += [
                base + 0, base + 1, base + 2, # Triangle 1
                base + 0, base + 2, base + 3  # Triangle 2
            ]

        return pos, norm, idx


    def _upload(self, positions, normals, indices):
        vertex_data = QByteArray()
        index_data = QByteArray()

        # pack vertex data
        for p, n in zip(positions, normals):
            vertex_data += struct.pack("<ffffff", p.x(), p.y(), p.z(), n.x(), n.y(), n.z())
        for i in indices:
            index_data += struct.pack("<I", i)

        self.setVertexData(vertex_data)
        self.setIndexData(index_data)
        self.addAttribute(QQuick3DGeometry.Attribute.Semantic.PositionSemantic, 0, QQuick3DGeometry.Attribute.ComponentType.F32Type)
        self.addAttribute(QQuick3DGeometry.Attribute.Semantic.NormalSemantic, 12, QQuick3DGeometry.Attribute.ComponentType.F32Type)
        self.addAttribute(QQuick3DGeometry.Attribute.Semantic.IndexSemantic, 0, QQuick3DGeometry.Attribute.ComponentType.U32Type)
        self.setStride(24)
        self.setPrimitiveType(QQuick3DGeometry.PrimitiveType.Triangles)
        self.update()


@QmlElement
class PolylineGeometry(PolylineGeometryBase):
    def __init__(self, parent: QQuick3DObject | None = None):
        super().__init__(parent)


@QmlElement
class PolylineBatchGeometry(PolylineGeometryBase):
    """
    Renders multiple polylines as a single mesh.
    """
    batchedPointsChanged = Signal()

    def __init__(self, parent: QQuick3DObject | None = None):
        super().__init__(parent)
        self._batched_points: List[List[QVector3D]] = []

    def get_batched_points(self) -> List[List[QVector3D]]:
        return self._batched_points

    def set_batched_points(self, value: List[List[QVector3D]]):
        if self._batched_points == value: return
        self._batched_points = value
        self.batchedPointsChanged.emit()
        self.updateData()

    batchedPoints = Property(list, get_batched_points, set_batched_points, notify=batchedPointsChanged)

    def updateData(self):
        """
        Iterates over ALL polylines and combines them into one buffer.
        """
        self.clear()
        
        if not self._batched_points:
            return

        positions = []
        normals = []
        indices = []
        index_offset = 0
        
        min_v = QVector3D(float('inf'), float('inf'), float('inf'))
        max_v = QVector3D(float('-inf'), float('-inf'), float('-inf'))

        for polyline_strip in self._batched_points:
            index_offset = self._process_line_strip(
                polyline_strip, 
                positions, 
                normals, 
                indices, 
                index_offset, 
                min_v, 
                max_v
            )

        self.setBounds(min_v, max_v)
        self._upload(positions, normals, indices)