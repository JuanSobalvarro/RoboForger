# TODO: Complete this component, it is not being used yet
from PySide6.QtWidgets import (
    QWidget, 
    QPushButton, 
    QHBoxLayout, 
    QColorDialog
)
from PySide6.QtGui import QColor

DEFAULT_COLOR = "#000000"

class ColorSelector(QWidget):
    def __init__(self, widget, parent=None):
        super().__init__(parent)

        self.current_color = QColor(DEFAULT_COLOR)

    # def init_ui(self):
    #     layout = QHBoxLayout()
    #     self.color_button = QPushButton("Select Color")
    #     self.color_button.clicked.connect(self.open_color_dialog)
    #     layout.addWidget(self.color_button)
    #     self.setLayout(layout)