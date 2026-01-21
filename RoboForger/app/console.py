from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

class Console(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.setLayout(layout)