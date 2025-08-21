from PySide6.QtCore import Qt, QModelIndex, Signal, Property
from .line_model import LineModel

class BSplineModel(LineModel):
    DegreeRole = Qt.UserRole + 7
    ClosedRole = Qt.UserRole + 8
    KnotsRole = Qt.UserRole + 9
    WeightsRole = Qt.UserRole + 10
    ControlPointsRole = Qt.UserRole + 11
    FitPointsRole = Qt.UserRole + 12

    def __init__(self, parent=None):
        super().__init__(parent)
        self._splines = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._splines)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._splines)):
            return None

        spline = self._splines[index.row()]

        if role == self.DegreeRole:
            return spline['degree']
        elif role == self.ClosedRole:
            return spline['closed']
        elif role == self.KnotsRole:
            return spline['knots']
        elif role == self.WeightsRole:
            return spline['weights']
        elif role == self.ControlPointsRole:
            return spline['control_points']
        elif role == self.FitPointsRole:
            return spline['fit_points']

        return None

    def setSplines(self, splines):
        self.beginResetModel()
        self._splines = splines
        # We also need to set the lines internally since that is what we really access
        lines = []
        for spline in splines:
            lines.extend(spline['control_points'])
        self.endResetModel()

    splinesChanged = Signal()

    @Property('QVariantList', notify=splinesChanged)
    def splines(self):
        return self._splines

    @splines.setter
    def splines(self, value):
        self.setSplines(value)