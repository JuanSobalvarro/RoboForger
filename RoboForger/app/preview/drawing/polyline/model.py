from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QObject, Property, Signal, QPersistentModelIndex
from PySide6.QtGui import QVector3D, QColor
from PySide6.QtCore import QByteArray


class PolylineListModel(QAbstractListModel):

    PointsRole = Qt.ItemDataRole.UserRole + 1
    ColorRole = Qt.ItemDataRole.UserRole + 2
    ThicknessRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items: list[dict] = []

    def roleNames(self):
        return {
            self.PointsRole: QByteArray(b"points"),
            self.ColorRole: QByteArray(b"color"),
            self.ThicknessRole: QByteArray(b"thickness"),
        }

    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:
        return len(self._items)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]

        if role == self.PointsRole:
            return item["points"]
        if role == self.ColorRole:
            return item["color"]
        if role == self.ThicknessRole:
            return item["thickness"]

        return None

    def clear(self):
        self.beginResetModel()
        self._items.clear()
        self.endResetModel()

    def add_polyline(self, points, color, thickness):
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append({
            "points": points,
            "color": color,
            "thickness": thickness,
        })
        self.endInsertRows()

    def all_points(self) -> list[list[QVector3D]]:
        return [item["points"] for item in self._items]

    def all_colors(self):
        return {item["color"] for item in self._items}

    def all_thicknesses(self):
        return {item["thickness"] for item in self._items}
    
    def update_color(self, color: QColor):
        for index in range(len(self._items)):
            self._items[index]["color"] = color
            model_index = self.index(index)
            self.dataChanged.emit(model_index, model_index, [self.ColorRole])


class PolylineBatchModel(QObject):
    """
    Currently not used
    """

    pointsChanged = Signal()
    colorChanged = Signal()
    thicknessChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._points: list[list[QVector3D]] = []
        self._color = QColor("#000000")
        self._thickness = 1.0

    def get_points(self):
        return self._points

    def set_points(self, value):
        self._points = value
        self.pointsChanged.emit()

    points = Property(list, get_points, set_points, notify=pointsChanged)

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

    def add_batch(self, batched_points: list[list[QVector3D]], color: QColor, thickness: float):
        self.clear()
        self._points.extend(batched_points)
        self._color = color
        self._thickness = thickness
        self.pointsChanged.emit()
        self.colorChanged.emit()
        self.thicknessChanged.emit()

    def clear(self):
        self._points.clear()
        self.pointsChanged.emit()

    def batch_count(self) -> int:
        return len(self._points)