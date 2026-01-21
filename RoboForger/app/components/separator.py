from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel


class LineSeparator(QWidget):
    def __init__(self, orientation: str = 'horizontal'):
        super().__init__()

        self.orientation = orientation.lower()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self) if self.orientation == 'vertical' else QHBoxLayout(self)
        line = QFrame(self)
        if self.orientation == 'vertical':
            line.setFrameShape(QFrame.Shape.VLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
        else:
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)

        layout.addWidget(line)