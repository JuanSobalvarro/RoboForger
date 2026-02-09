from PySide6.QtCore import (
    Qt,
    Signal,
    Slot,
    QSize,
)
from PySide6.QtWidgets import (
    QWidget,
    QMenuBar,
    QDialog,
    QVBoxLayout,
    QLabel,
)
from PySide6.QtGui import (
    QImage,
    QPixmap,
)

from RoboForger.app.config import GlobalConfig
from RoboForger.utils import get_resource_path

import webbrowser

class MenuBar(QMenuBar):
    """
    A menu bar for the application.
    """
    def __init__(self, shared_config: GlobalConfig, parent=None):
        super().__init__(parent)
        
        self.shared_config = shared_config
        self.setup_menus()

    def setup_menus(self):
        # File menu
        config_menu = self.addMenu("Config")

        help_menu = self.addMenu("Help")
        help_menu.addAction("GitHub Repository", lambda: webbrowser.open("https://github.com/JuanSobalvarro/RoboForger"))

        about_action = self.addAction("About", self.show_about_dialog)

    def show_about_dialog(self):
        # print("Show about dialog")

        dialog = QDialog(self)
        dialog.setWindowTitle("About RoboForger")
        layout = QVBoxLayout(dialog)

        icon = QImage(get_resource_path("img/icon.png"))
        pixmap = icon.scaled(QSize(128, 128), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(pixmap))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)

        about_text = QLabel("RoboForger v2.1.0\nCreated by Juan Sobalvarro\n\n\nThis project was created for educational purposes and is licensed under the MIT License.\n" \
        "I hope this program will help you automatizing, validating and optimizing your work!,\n"
        "if you have any suggestion just contact me, check my github and give a star :D")
        about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(about_text)
        dialog.setLayout(layout)
        dialog.exec()