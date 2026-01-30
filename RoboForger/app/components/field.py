from PySide6.QtWidgets import (
    QWidget, 
    QFrame,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import (
    Signal,
    Qt,
)

from RoboForger.app.components.label import Label
from enum import Enum

class LabelPosition(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class LabelAnchor(Enum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    CENTER = 4

class Field(QWidget):
    value_changed = Signal(object)

    def __init__(
        self,
        label_text: str,
        input_widget: QWidget,
        default: str | bool | int | float = "",
        label_position: LabelPosition = LabelPosition.LEFT,
        label_anchor: LabelAnchor = LabelAnchor.CENTER,
        preferred_input_width: int = 90,
    ):
        super().__init__()

        self.label_text = label_text
        self.label_position = label_position
        self.label_anchor = label_anchor
        self.default = default
        self.preferred_input_width = preferred_input_width

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.background_frame = QFrame(self)
        self.background_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_layout.addWidget(self.background_frame)

        self.input_widget = self.validate_input_widget(input_widget)
        self.input_widget.setParent(self.background_frame)

        self.input_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self.input_widget.setMinimumWidth(self.preferred_input_width)
        self.input_widget.setMaximumWidth(9999)

        self.label = Label(self.label_text, self.background_frame)

        self.label.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed
        )

        self.setup_ui()
        self.set_default()
        self.connect_signals()

    def setup_ui(self):
        if self.label_position in (LabelPosition.LEFT, LabelPosition.RIGHT):
            layout = QHBoxLayout(self.background_frame)
        else:
            layout = QVBoxLayout(self.background_frame)

        layout.setContentsMargins(4, 2, 4, 2)
        layout.setSpacing(6)

        if self.label_position == LabelPosition.LEFT:
            layout.addWidget(self.label)
            layout.addWidget(self.input_widget, 1)
        elif self.label_position == LabelPosition.RIGHT:
            layout.addWidget(self.input_widget, 1)
            layout.addWidget(self.label)
        elif self.label_position == LabelPosition.UP:
            layout.addWidget(self.label)
            layout.addWidget(self.input_widget)
        elif self.label_position == LabelPosition.DOWN:
            layout.addWidget(self.input_widget)
            layout.addWidget(self.label)

        alignment_map = {
            LabelAnchor.TOP: Qt.AlignmentFlag.AlignTop,
            LabelAnchor.BOTTOM: Qt.AlignmentFlag.AlignBottom,
            LabelAnchor.LEFT: Qt.AlignmentFlag.AlignLeft,
            LabelAnchor.RIGHT: Qt.AlignmentFlag.AlignRight,
            LabelAnchor.CENTER: Qt.AlignmentFlag.AlignCenter,
        }

        layout.setAlignment(
            self.label,
            alignment_map.get(self.label_anchor, Qt.AlignmentFlag.AlignCenter)
        )

    def set_default(self):
        if isinstance(self.input_widget, QLineEdit):
            self.input_widget.setText(str(self.default))
        elif isinstance(self.input_widget, QComboBox):
            index = self.input_widget.findText(str(self.default))
            if index != -1:
                self.input_widget.setCurrentIndex(index)
        elif isinstance(self.input_widget, QCheckBox):
            self.input_widget.setChecked(bool(self.default))
        elif isinstance(self.input_widget, QSpinBox):
            self.input_widget.setValue(int(self.default))

    def validate_input_widget(self, widget: QWidget) -> QWidget:
        if not isinstance(widget, QWidget):
            raise TypeError("Input widget must be a QWidget.")
        if not isinstance(widget, (QLineEdit, QComboBox, QCheckBox, QSpinBox)):
            raise TypeError(f"Unsupported widget type: {type(widget)}")
        return widget

    def connect_signals(self):
        if isinstance(self.input_widget, QLineEdit):
            self.input_widget.textChanged.connect(self.value_changed.emit)
        elif isinstance(self.input_widget, QComboBox):
            self.input_widget.currentIndexChanged.connect(lambda: self.value_changed.emit(self.value))
        elif isinstance(self.input_widget, QCheckBox):
            self.input_widget.stateChanged.connect(lambda val: self.value_changed.emit(bool(val)))
        elif isinstance(self.input_widget, QSpinBox):
            self.input_widget.valueChanged.connect(self.value_changed.emit)

    @property
    def value(self):
        if isinstance(self.input_widget, QLineEdit):
            return self.input_widget.text()
        elif isinstance(self.input_widget, QComboBox):
            return self.input_widget.currentText()
        elif isinstance(self.input_widget, QCheckBox):
            return self.input_widget.isChecked()
        elif isinstance(self.input_widget, QSpinBox):
            return self.input_widget.value()
        return None