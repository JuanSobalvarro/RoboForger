from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Property, Signal


class LineModel(QAbstractListModel):
    StartXRole = Qt.UserRole + 1
    StartYRole = Qt.UserRole + 2
    StartZRole = Qt.UserRole + 3
    EndXRole = Qt.UserRole + 4
    EndYRole = Qt.UserRole + 5
    EndZRole = Qt.UserRole + 6

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lines = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._lines)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._lines)):
            return None

        line = self._lines[index.row()]

        if role == self.StartXRole:
            return line['start'][0]
        elif role == self.StartYRole:
            return line['start'][1]
        elif role == self.StartZRole:
            return line['start'][2]
        elif role == self.EndXRole:
            return line['end'][0]
        elif role == self.EndYRole:
            return line['end'][1]
        elif role == self.EndZRole:
            return line['end'][2]

        return None

    def roleNames(self):
        roles = dict()
        roles[self.StartXRole] = b"start_x"
        roles[self.StartYRole] = b"start_y"
        roles[self.StartZRole] = b"start_z"
        roles[self.EndXRole] = b"end_x"
        roles[self.EndYRole] = b"end_y"
        roles[self.EndZRole] = b"end_z"
        return roles

    def setLines(self, lines):
        self.beginResetModel()
        self._lines = lines
        self.endResetModel()

    linesChanged = Signal()

    @Property('QVariantList', notify=linesChanged)
    def lines(self):
        return self._lines

    @lines.setter
    def lines(self, value):
        self.setLines(value)
        self.linesChanged.emit()
