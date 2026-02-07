from PySide6.QtCore import (
    QAbstractListModel, 
    Qt, 
    QModelIndex, 
    Slot, 
    Signal, 
    QByteArray, 
    QPersistentModelIndex, 
    QObject,
    Property,
)
from PySide6.QtGui import QVector3D, QColor


class ArcListModel(QAbstractListModel):
    # Custom Roles to pass data to QML
    CenterRole = Qt.ItemDataRole.UserRole + 1
    RadiusRole = Qt.ItemDataRole.UserRole + 2
    StartAngleRole = Qt.ItemDataRole.UserRole + 3
    EndAngleRole = Qt.ItemDataRole.UserRole + 4
    ClockwiseRole = Qt.ItemDataRole.UserRole + 5
    ColorRole = Qt.ItemDataRole.UserRole + 6
    ThicknessRole = Qt.ItemDataRole.UserRole + 7

    def __init__(self, parent=None):
        super().__init__(parent)
        # Each item is a dict: {'center': QVector3D, 'radius': float, 'start_angle': float, 'end_angle': float, 'clockwise': bool, 'color': QColor, 'thickness': float}
        self._items = []

    def roleNames(self):
        return {
            ArcListModel.CenterRole: QByteArray(b"center"),
            ArcListModel.RadiusRole: QByteArray(b"radius"),
            ArcListModel.StartAngleRole: QByteArray(b"start_angle"),
            ArcListModel.EndAngleRole: QByteArray(b"end_angle"),
            ArcListModel.ClockwiseRole: QByteArray(b"clockwise"),
            ArcListModel.ColorRole: QByteArray(b"color"),
            ArcListModel.ThicknessRole: QByteArray(b"thickness")
        }

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()):
        return len(self._items)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._items):
            return None
        
        item = self._items[index.row()]
        
        if role == ArcListModel.CenterRole:
            return item['center']
        elif role == ArcListModel.RadiusRole:
            return item['radius']
        elif role == ArcListModel.StartAngleRole:
            return item['start_angle']
        elif role == ArcListModel.EndAngleRole:
            return item['end_angle']
        elif role == ArcListModel.ClockwiseRole:
            return item['clockwise']
        elif role == ArcListModel.ColorRole:
            return item['color']
        elif role == ArcListModel.ThicknessRole:
            return item['thickness']
        
    def add_arc(self, center: QVector3D, radius: float, start_angle: float, end_angle: float, clockwise: bool, color: QColor, thickness: float):
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append({
            'center': center,
            'radius': radius,
            'start_angle': start_angle,
            'end_angle': end_angle,
            'clockwise':clockwise,
            'color': color,
            'thickness': thickness
        })
        self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self._items.clear()
        self.endResetModel()


class ArcBatchModel(QObject):
    """
    Currently not used
    """

    centerChanged = Signal()
    radiusChanged = Signal()
    startAngleChanged = Signal()
    endAngleChanged = Signal()
    clockwiseChanged = Signal()
    colorChanged = Signal()
    thicknessChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._centers: list[QVector3D] = []
        self._radii: list[float] = []
        self._start_angles: list[float] = []
        self._end_angles: list[float] = []
        self._clockwises: list[bool] = []
        self._color = QColor("#000000")
        self._thickness = 1.0
    
    def get_centers(self):
        return self._centers
    
    def set_centers(self, value):
        self._centers = value
        self.centerChanged.emit()

    centers = Property(list, get_centers, set_centers, notify=centerChanged)

    def get_radii(self):
        return self._radii
    
    def set_radii(self, value):
        if self._radii == value:
            return
        self._radii = value
        self.radiusChanged.emit()

    radii = Property(list, get_radii, set_radii, notify=radiusChanged)

    def get_start_angles(self):
        return self._start_angles
    
    def set_start_angles(self, value):
        if self._start_angles == value:
            return
        self._start_angles = value
        self.startAngleChanged.emit()

    startAngles = Property(list, get_start_angles, set_start_angles, notify=startAngleChanged)

    def get_end_angles(self):
        return self._end_angles
    
    def set_end_angles(self, value):
        if self._end_angles == value:
            return
        self._end_angles = value
        self.endAngleChanged.emit()

    endAngles = Property(list, get_end_angles, set_end_angles, notify=endAngleChanged)

    def get_clockwises(self):
        return self._clockwises
    
    def set_clockwises(self, value):
        if self._clockwises == value:
            return
        self._clockwises = value
        self.clockwiseChanged.emit()

    clockwises = Property(list, get_clockwises, set_clockwises, notify=clockwiseChanged)

    def get_color(self):
        return self._color
    
    def set_color(self, value):
        if self._color == value:
            return
        self._color = value
        self.colorChanged.emit()

    color = Property(QColor, get_color, set_color, notify=colorChanged)

    def get_thickness(self):
        return self._thickness
    
    def set_thickness(self, value):
        if self._thickness == value:
            return
        self._thickness = value
        self.thicknessChanged.emit()

    thickness = Property(float, get_thickness, set_thickness, notify=thicknessChanged)

    def batch_count(self):
        return len(self._centers)
    
    def add_batch(self, centers: list[QVector3D], radii: list[float], start_angles: list[float], end_angles: list[float], clockwises: list[bool], color: QColor, thickness: float):
        self.clear()
        self._centers.extend(centers)
        self._radii.extend(radii)
        self._start_angles.extend(start_angles)
        self._end_angles.extend(end_angles)
        self._clockwises.extend(clockwises)
        self._color = color
        self._thickness = thickness
        self.centerChanged.emit()
        self.radiusChanged.emit()
        self.startAngleChanged.emit()
        self.endAngleChanged.emit()
        self.clockwiseChanged.emit()
        self.colorChanged.emit()
        self.thicknessChanged.emit()

    def clear(self):
        self._centers.clear()
        self._radii.clear()
        self._start_angles.clear()
        self._end_angles.clear()
        self._clockwises.clear()
        self.centerChanged.emit()
        self.radiusChanged.emit()
        self.startAngleChanged.emit()
        self.endAngleChanged.emit()
        self.clockwiseChanged.emit()
