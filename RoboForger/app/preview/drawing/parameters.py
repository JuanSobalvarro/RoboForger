from PySide6.QtCore import QObject, Signal

from RoboForger.forger import ForgerParameters


class ProcessingParameters(QObject):
    parameter_changed = Signal(str, object)
    parameters_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._model = ForgerParameters()
        self._data = self._model.to_dict()

    def set(self, key: str, value):
        if key not in self._data:
            raise KeyError(f"Unknown parameter: {key}. Current parameters: {list(self._data.keys())}")

        if self._data[key] == value:
            return

        self._validate(key, value)

        self._data[key] = value
        setattr(self._model, key, value)

        self.parameter_changed.emit(key, value)
        self.parameters_changed.emit()

    def set_tuple_item(self, key: str, index: int, value):
        tpl = list(self._data[key])
        tpl[index] = value
        self.set(key, tuple(tpl))

    def get(self, key: str):
        return self._data[key]

    def snapshot(self) -> dict:
        return dict(self._data)

    def backend_parameters(self) -> ForgerParameters:
        return self._model

    def _validate(self, key, value):
        if key.endswith("_velocity") and value <= 0:
            raise ValueError("Velocity must be positive")

        if key == "float_precision" and value < 0:
            raise ValueError("Precision must be >= 0")

    def set_workspace_limit(self, bound: int, axis: int, value: float):
        """
        bound: 0 = inferior, 1 = superior
        axis:  0 = x, 1 = y, 2 = z
        """
        limits = list(self._data["workspace_limits"])
        vec = list(limits[bound])
        vec[axis] = value
        limits[bound] = tuple(vec)

        self.set("workspace_limits", tuple(limits))