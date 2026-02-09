from PySide6.QtCore import (
    Qt,
    QObject,
    Signal,
    Slot,
)

from RoboForger.utils import get_resource_path

import json
from pathlib import Path


CONFIG_PATH = get_resource_path("config.json")
DEFAULT_CONFIG_PATH = get_resource_path("default_config.json")


class GlobalConfig(QObject):
    """
    A singleton class to hold global configuration and state for the application.
    """
    # Signals to notify about configuration changes
    chord_error_changed = Signal(float)
    show_limit_square_changed = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._chord_error = 0.1
        self._show_limit_square = True
    
    @property
    def chord_error(self) -> float:
        return self._chord_error
    
    @chord_error.setter
    def chord_error(self, value: float):
        if self._chord_error != value:
            self._chord_error = value
            self.chord_error_changed.emit(value)

    @property
    def show_limit_square(self) -> bool:
        return self._show_limit_square
    
    @show_limit_square.setter
    def show_limit_square(self, value: bool):
        if self._show_limit_square != value:
            self._show_limit_square = value
            self.show_limit_square_changed.emit(value)

    def to_dict(self) -> dict:
        return {
            "chord_error": self.chord_error,
            "show_limit_square": self.show_limit_square,
        }
    
    def from_dict(self, data: dict):
        self.chord_error = data.get("chord_error", self.chord_error)
        self.show_limit_square = data.get("show_limit_square", self.show_limit_square)
    
    def load(self):
        path = Path(CONFIG_PATH)
        if not path.exists():
            path = Path(DEFAULT_CONFIG_PATH)

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.from_dict(json.load(f))
        except Exception as e:
            print(f"Config load failed: {e}")

    def save(self):
        Path(CONFIG_PATH).parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)
