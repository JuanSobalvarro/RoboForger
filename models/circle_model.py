from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Property, Signal


class CircleModel(QAbstractListModel):
    CenterXRole = Qt.UserRole + 1
    CenterYRole = Qt.UserRole + 2
    CenterZRole = Qt.UserRole + 3
    RadiusRole = Qt.UserRole + 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self._circles = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._circles)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._circles)):
            return None

        circle = self._circles[index.row()]

        if role == self.CenterXRole:
            return circle['center'][0]
        elif role == self.CenterYRole:
            return circle['center'][1]
        elif role == self.CenterZRole:
            return circle['center'][2]
        elif role == self.RadiusRole:
            return circle['radius']

        return None

    def roleNames(self):
        roles = dict()
        roles[self.CenterXRole] = b"center_x"
        roles[self.CenterYRole] = b"center_y"
        roles[self.CenterZRole] = b"center_z"
        roles[self.RadiusRole] = b"radius"
        return roles

    def setCircles(self, circles):
        self.beginResetModel()
        self._circles = circles
        self.endResetModel()

    circlesChanged = Signal()

    @Property('QVariantList', notify=circlesChanged)
    def circles(self):
        return self._circles

    @circles.setter
    def circles(self, value):
        if self._circles != value:
            self.setCircles(value)
            self.circlesChanged.emit()