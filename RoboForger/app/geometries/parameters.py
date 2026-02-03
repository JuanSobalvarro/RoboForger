from PySide6.QtCore import QObject


class ProcessingParameters(QObject):
    def __init__(self):
        super().__init__()
        self._data = {
            "scale": 1.0,
            "float_precision": 3,
            "lines_velocity": 100.0,
            "arcs_velocity": 80.0,
            "circles_velocity": 80.0,
            "lifting": 5.0,
            "use_detector": False,
            "use_offset": False,
            "tool_name": "",
            "origin": (0, 0, 0),
            "zero": (0, 0, 0),
            "inferior_limit": (-100, -100, -100),
            "superior_limit": (100, 100, 100),
        }

    def update(self, key, value):
        # print(f"Updating parameter: {key} to value: {value}")
        self._data[key] = value
    
    def update_tuple(self, key, index, value):
        lst = list(self._data[key])
        lst[index] = value
        self._data[key] = tuple(lst)

    def snapshot(self) -> dict:
        # IMPORTANT: return a COPY
        return dict(self._data)
