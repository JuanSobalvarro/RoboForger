from PySide6.QtCore import (
    Qt,
    QObject,
    Signal,
    Slot,
)
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QCheckBox,
    QSpinBox,
    QPushButton,
)
from PySide6.QtGui import (
    QColor,
)

from RoboForger.utils import get_resource_path

from RoboForger.app.components.field import Field

import json
from pathlib import Path


CONFIG_PATH = get_resource_path("config.json")
DEFAULT_CONFIG_PATH = get_resource_path("default_config.json")


class GlobalConfig(QObject):
    """
    A singleton class to hold global configuration and state for the application.
    """
    value_changed = Signal(str, object) # signal to notify about any value change, with key and new value

    chord_error_changed = Signal(float)
    show_limit_square_changed = Signal(bool)
    grid_size_changed = Signal(int)
    grid_step_changed = Signal(int)
    polyline_color_changed = Signal(QColor)
    arc_color_changed = Signal(QColor)
    circle_color_changed = Signal(QColor)
    x_axis_color_changed = Signal(QColor)
    y_axis_color_changed = Signal(QColor)
    z_axis_color_changed = Signal(QColor)
    grid_color_changed = Signal(QColor)
    limits_color_changed = Signal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._chord_error = 0.1
        self._show_limit_square = True
        self._grid_size = 1000
        self._grid_step = 50

        self._polyline_color = QColor("#0000ff")
        self._arc_color = QColor("#00ff00")
        self._circle_color = QColor("#ffff00")

        self._x_axis_color = QColor("#ff0000")
        self._y_axis_color = QColor("#00ff00")
        self._z_axis_color = QColor("#0000ff")

        self._grid_color = QColor("#888888")
        
        self._limits_color = QColor("#ff00ff")
    
    @property
    def chord_error(self) -> float:
        return self._chord_error
    
    @chord_error.setter
    def chord_error(self, value: float):
        if self._chord_error != value:
            self._chord_error = value
            self.chord_error_changed.emit(value)
            self.value_changed.emit("chord_error", value)

    @property
    def show_limit_square(self) -> bool:
        return self._show_limit_square
    
    @show_limit_square.setter
    def show_limit_square(self, value: bool):
        if self._show_limit_square != value:
            self._show_limit_square = value
            self.show_limit_square_changed.emit(value)
            self.value_changed.emit("show_limit_square", value)

    @property
    def grid_size(self) -> int:
        return self._grid_size
    
    @grid_size.setter
    def grid_size(self, value: int):
        if self._grid_size != value:
            self._grid_size = value
            self.grid_size_changed.emit(value)
            self.value_changed.emit("grid_size", value)

    @property
    def grid_step(self) -> int:
        return self._grid_step
    
    @grid_step.setter
    def grid_step(self, value: int):
        if self._grid_step != value:
            self._grid_step = value
            self.grid_step_changed.emit(value)
            self.value_changed.emit("grid_step", value)

    @property
    def polyline_color(self) -> QColor:
        return self._polyline_color
    
    @polyline_color.setter
    def polyline_color(self, value: QColor):
        if self._polyline_color != value:
            self._polyline_color = value
            self.polyline_color_changed.emit(value)
            self.value_changed.emit("polyline_color", value)

    @property
    def arc_color(self) -> QColor:
        return self._arc_color
    
    @arc_color.setter
    def arc_color(self, value: QColor):
        if self._arc_color != value:
            self._arc_color = value
            self.arc_color_changed.emit(value)
            self.value_changed.emit("arc_color", value)

    @property
    def circle_color(self) -> QColor:
        return self._circle_color
    
    @circle_color.setter
    def circle_color(self, value: QColor):
        if self._circle_color != value:
            self._circle_color = value
            self.circle_color_changed.emit(value)
            self.value_changed.emit("circle_color", value)

    @property
    def x_axis_color(self) -> QColor:
        return self._x_axis_color
    
    @x_axis_color.setter
    def x_axis_color(self, value: QColor):
        if self._x_axis_color != value:
            self._x_axis_color = value
            self.x_axis_color_changed.emit(value)
            self.value_changed.emit("x_axis_color", value)

    @property
    def y_axis_color(self) -> QColor:
        return self._y_axis_color
    
    @y_axis_color.setter
    def y_axis_color(self, value: QColor):
        if self._y_axis_color != value:
            self._y_axis_color = value
            self.y_axis_color_changed.emit(value)
            self.value_changed.emit("y_axis_color", value)
    
    @property
    def z_axis_color(self) -> QColor:
        return self._z_axis_color
    
    @z_axis_color.setter
    def z_axis_color(self, value: QColor):
        if self._z_axis_color != value:
            self._z_axis_color = value
            self.z_axis_color_changed.emit(value)
            self.value_changed.emit("z_axis_color", value)

    @property
    def grid_color(self) -> QColor:
        return self._grid_color
    
    @grid_color.setter
    def grid_color(self, value: QColor):
        if self._grid_color != value:
            self._grid_color = value
            self.grid_color_changed.emit(value)
            self.value_changed.emit("grid_color", value)

    @property
    def limits_color(self) -> QColor:
        return self._limits_color
    
    @limits_color.setter
    def limits_color(self, value: QColor):
        if self._limits_color != value:
            self._limits_color = value
            self.limits_color_changed.emit(value)
            self.value_changed.emit("limits_color", value)

    def to_dict(self) -> dict:
        return {
            "chord_error": self.chord_error,
            "show_limit_square": self.show_limit_square,
            "grid_size": self._grid_size,
            "grid_step": self._grid_step,
        }
    
    def from_dict(self, data: dict):
        # why not using _? because we want to trigger the signals so we call the setters
        self.chord_error = data.get("chord_error", self.chord_error)
        self.show_limit_square = data.get("show_limit_square", self.show_limit_square)
        self.grid_size = data.get("grid_size", self.grid_size)
        self.grid_step = data.get("grid_step", self.grid_step)
    
    def load(self, filepath: str):
        """
        Load from config file, if path is given it means to load from that path, else
        load from default config path, if that fails load from hardcoded defaults.
        """
        
        path = Path(filepath)

        if not path.exists():
            print(f"Config file not found at {path}, trying default config path")
            path = Path(DEFAULT_CONFIG_PATH)
            if not path.exists():
                raise FileNotFoundError(f"Default config file not found at {path}. Couldnt load configuration.")

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.from_dict(json.load(f))
        except Exception as e:
            print(f"Config load failed: {e}")

    def save(self):
        Path(CONFIG_PATH).parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    def get_params_widgets(self) -> dict[str, Field]:

        return {
            "chord_error": Field(
                label_text="Chord Error",
                input_widget=QLineEdit(str(self.chord_error)),
                default=str(self.chord_error),
            ),
            "show_limit_square": Field(
                label_text="Show Limit Square",
                input_widget=QCheckBox(),
                default=self.show_limit_square,
            ),
            "grid_size": Field(
                label_text="Grid Size",
                input_widget=QSpinBox(minimum=100, maximum=10000),
                default=self.grid_size,
            ),
            "grid_step": Field(
                label_text="Grid Step",
                input_widget=QSpinBox(minimum=1, maximum=1000),
                default=self.grid_step,
            ),
            # "polyline_color": Field(
        }

    def reset_to_defaults(self):
        self.load(DEFAULT_CONFIG_PATH)
    
    def show_param_dialog(self, param: str):
        if param not in self.get_params_widgets():
            return
        
        field = self.get_params_widgets()[param]
        dialog = QWidget()
        dialog.setWindowTitle(f"Edit {field.label_text}")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(field.label_text))
        layout.addWidget(field.input_widget)
        save_button = QPushButton("Save")
        layout.addWidget(save_button)
        dialog.setLayout(layout)

        def on_save():
            value = None
            if isinstance(field.input_widget, QLineEdit):
                value = field.input_widget.text()
                try:
                    value = float(value)
                except ValueError:
                    print("Invalid input, expected a number")
                    return
            elif isinstance(field.input_widget, QCheckBox):
                value = field.input_widget.isChecked()
            elif isinstance(field.input_widget, QSpinBox):
                value = field.input_widget.value()
            setattr(self, param, value)
            dialog.close()

        save_button.clicked.connect(on_save)
        dialog.show()