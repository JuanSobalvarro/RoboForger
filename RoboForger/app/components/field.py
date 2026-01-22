"""
A Field is a UI component that contains a label and an input area (like a text box, dropdown, etc.)

It can be selected as an up, down, left or right label around the input area.
"""
from PySide6.QtWidgets import (
    QWidget, 
    QLabel,
    QLineEdit,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
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

    def __init__(self, label_text: str, input_widget: QWidget, default: str | bool | int | float = "", label_position: LabelPosition = LabelPosition.LEFT, label_anchor: LabelAnchor = LabelAnchor.CENTER, input_width: int = 70):
        """
        A Field is a UI component that contains a label and an input area (like a text box, dropdown, etc.)

        It can be selected as an up, down, left or right label around the input area.
        """
        super().__init__()

        self.label_text = label_text
        self.label_position = label_position
        self.label_anchor = label_anchor
        self.input_widget = self.validate_input_widget(input_widget)
        self.input_widget.setFixedWidth(input_width)
        self.default = default

        self.label = Label(self.label_text, self)

        self.show_border = True # debugging purposes

        self.setup_ui()

        self.set_default()

        self.connect_signals()

    def set_default(self):
        """
        Sets the default value to the input widget
        """
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
        """
        This method validates if the input widget is acceptable since we need to know which one is to send the signal
        Accepted:
        - QLineEdit
        - QComboBox
        - QCheckBox
        - QSpinBox
        """

        if not isinstance(widget, QWidget):
            raise TypeError("Input widget must be a QWidget or its subclass.")
        
        if not isinstance(widget, (QLineEdit, QComboBox, QCheckBox, QSpinBox)):
            raise TypeError("Input widget must be one of the following types: QLineEdit, QComboBox, QCheckBox, QSpinBox."
                            f" Got {type(widget)} instead.")

        return widget

    def setup_ui(self):
        layout = None
        if self.label_position in (LabelPosition.LEFT, LabelPosition.RIGHT):
            layout = QHBoxLayout(self)
        else:
            layout = QVBoxLayout(self)

        if self.label_position == LabelPosition.LEFT:
            layout.addWidget(self.label)
            layout.addWidget(self.input_widget)
        elif self.label_position == LabelPosition.RIGHT:
            layout.addWidget(self.input_widget)
            layout.addWidget(self.label)
        elif self.label_position == LabelPosition.UP:
            layout.addWidget(self.label)
            layout.addWidget(self.input_widget)
        elif self.label_position == LabelPosition.DOWN:
            layout.addWidget(self.input_widget)
            layout.addWidget(self.label)

        # anchor
        if self.label_anchor == LabelAnchor.TOP:
            layout.setAlignment(self.label, Qt.AlignmentFlag.AlignTop)
        elif self.label_anchor == LabelAnchor.BOTTOM:
            layout.setAlignment(self.label, Qt.AlignmentFlag.AlignBottom)
        elif self.label_anchor == LabelAnchor.LEFT:
            layout.setAlignment(self.label, Qt.AlignmentFlag.AlignLeft)
        elif self.label_anchor == LabelAnchor.RIGHT:
            layout.setAlignment(self.label, Qt.AlignmentFlag.AlignRight)
        elif self.label_anchor == LabelAnchor.CENTER:
            layout.setAlignment(self.label, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def connect_signals(self):
        # remember we are connecting the input widget TO this class signal
        if isinstance(self.input_widget, QLineEdit):
            self.input_widget.textChanged.connect(lambda val: self.value_changed.emit(val)) # this means connect that value to a lambda val that emits to this class signal
        elif isinstance(self.input_widget, QComboBox):
            self.input_widget.currentIndexChanged.connect(lambda: self.value_changed.emit(self.value))
        elif isinstance(self.input_widget, QCheckBox):
            self.input_widget.stateChanged.connect(lambda val: self.value_changed.emit(bool(val)))
        elif isinstance(self.input_widget, QSpinBox):
            self.input_widget.valueChanged.connect(lambda val: self.value_changed.emit(val))

    @property
    def value(self):
        """
        A property to get the value from the input widget
        """
        if isinstance(self.input_widget, QLineEdit):
            return self.input_widget.text()
        elif isinstance(self.input_widget, QComboBox):
            return self.input_widget.currentText()
        elif isinstance(self.input_widget, QCheckBox):
            return self.input_widget.isChecked()
        elif isinstance(self.input_widget, QSpinBox):
            return self.input_widget.value()
        else:
            return None
