from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
)

class Console(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        background_frame = QFrame(self)
        background_frame.setStyleSheet("background-color: #111111; border: 1px solid #333333;")
        layout.addWidget(background_frame)

        self.setLayout(layout)