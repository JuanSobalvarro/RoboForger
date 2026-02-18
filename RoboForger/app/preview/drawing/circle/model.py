from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Slot, Signal, QByteArray, QPersistentModelIndex
from PySide6.QtGui import QVector3D, QColor


class CircleListModel(QAbstractListModel):
    # Custom Roles to pass data to QML
    CenterRole = Qt.ItemDataRole.UserRole + 1
    RadiusRole = Qt.ItemDataRole.UserRole + 2
    ColorRole = Qt.ItemDataRole.UserRole + 3
    ThicknessRole = Qt.ItemDataRole.UserRole + 4

    def __init__(self, parent=None):
        super().__init__(parent)
        # Each item is a dict: {'center': QVector3D, 'radius': float, 'color': QColor, 'thickness': float}
        self._items = []

    def roleNames(self):
        return {
            CircleListModel.CenterRole: QByteArray(b"center"),
            CircleListModel.RadiusRole: QByteArray(b"radius"),
            CircleListModel.ColorRole: QByteArray(b"color"),
            CircleListModel.ThicknessRole: QByteArray(b"thickness")
        }
    
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()):
        return len(self._items)
    
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._items):
            return None
        
        item = self._items[index.row()]
        
        if role == CircleListModel.CenterRole:
            return item['center']
        elif role == CircleListModel.RadiusRole:
            return item['radius']
        elif role == CircleListModel.ColorRole:
            return item['color']
        elif role == CircleListModel.ThicknessRole:
            return item['thickness']
        
    def add_circle(self, center: QVector3D, radius: float, color: QColor, thickness: float):
        self.beginInsertRows(QModelIndex(), len(self._items), len(self._items))
        self._items.append({
            'center': center,
            'radius': radius,
            'color': color,
            'thickness': thickness
        })
        self.endInsertRows()

    def clear(self):
        self.beginResetModel()
        self._items.clear()
        self.endResetModel()