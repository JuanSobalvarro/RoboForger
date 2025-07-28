from PySide6.QtCore import QAbstractListModel, Qt, Property, Signal


class ArcModel(QAbstractListModel):
    CenterXRole = Qt.UserRole + 1
    CenterYRole = Qt.UserRole + 2
    CenterZRole = Qt.UserRole + 3
    RadiusRole = Qt.UserRole + 4
    StartAngleRole = Qt.UserRole + 5
    EndAngleRole = Qt.UserRole + 6
    ClockwiseRole = Qt.UserRole + 7

    def __init__(self, parent=None):
        super().__init__(parent)
        self._arcs = []

    def rowCount(self, parent=None):
        return len(self._arcs)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._arcs)):
            return None

        arc = self._arcs[index.row()]

        if role == self.CenterXRole:
            return arc['center'][0]
        elif role == self.CenterYRole:
            return arc['center'][1]
        elif role == self.CenterZRole:
            return arc['center'][2]
        elif role == self.RadiusRole:
            return arc['radius']
        elif role == self.StartAngleRole:
            return arc['start_angle']
        elif role == self.EndAngleRole:
            return arc['end_angle']
        elif role == self.ClockwiseRole:
            return arc['clockwise']

        return None

    def roleNames(self):
        roles = dict()
        roles[self.CenterXRole] = b"center_x"
        roles[self.CenterYRole] = b"center_y"
        roles[self.CenterZRole] = b"center_z"
        roles[self.RadiusRole] = b"radius"
        roles[self.StartAngleRole] = b"start_angle"
        roles[self.EndAngleRole] = b"end_angle"
        roles[self.ClockwiseRole] = b"clockwise"
        return roles

    def setArcs(self, arcs):
        self.beginResetModel()
        self._arcs = arcs
        self.endResetModel()

    arcsChanged = Signal()

    @Property('QVariantList', notify=arcsChanged)
    def arcs(self):
        return self._arcs

    @arcs.setter
    def arcs(self, value):
        if self._arcs != value:
            self.setArcs(value)
            self.arcsChanged.emit()