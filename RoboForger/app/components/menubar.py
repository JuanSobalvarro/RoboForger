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

        self.actions_map = {} 
        
        self.labels_map = {
            "chord_error": "Chord Error",
            "grid_size": "Grid Size",
            "grid_step": "Grid Step",
            "show_limit_square": "Show Limit Square"
        }

        self.setup_menus()

        self.shared_config.value_changed.connect(self.update_menu_action)

    def setup_menus(self):
        # File menu
        self._setup_config_menu()

        help_menu = self.addMenu("Help")
        help_menu.addAction("GitHub Repository", lambda: webbrowser.open("https://github.com/JuanSobalvarro/RoboForger"))
        help_menu.addAction("Shortcuts, Hints, Controllers", self.show_shortcuts_dialog)

        about_action = self.addAction("About", self.show_about_dialog)

    def update_menu_action(self, key: str, value: object):
        action = self.actions_map.get(key)
        if action:
            label = self.labels_map.get(key, key)
            action.setText(f"{label}: {value}")

    def _setup_config_menu(self):
        config_menu = self.addMenu("Configuration")
        config_menu.setToolTip("Configure processing parameters, this config is shared across the app and will affect all processing operations. Also it will be saved and loaded on app restart")

        def add_tracked_action(key, initial_value):
            label = self.labels_map.get(key, key)
            action = config_menu.addAction(
                f"{label}: {initial_value}", 
                lambda: self.shared_config.show_param_dialog(key)
            )
            self.actions_map[key] = action

        add_tracked_action("chord_error", self.shared_config.chord_error)
        add_tracked_action("grid_size", self.shared_config.grid_size)
        add_tracked_action("grid_step", self.shared_config.grid_step)
        add_tracked_action("show_limit_square", self.shared_config.show_limit_square)

        config_menu.addSeparator()
        config_menu.addAction("Reset to Defaults", self.shared_config.reset_to_defaults)

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

    def show_shortcuts_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Shortcuts")
        layout = QVBoxLayout(dialog)

        shortcuts_text = QLabel(
            "On Preview:\n"
            "- Left Click: FP Camera\n"
            "- WASD: Move FP Camera\n"
            "- R/F: Move Up/Down FP Camera\n"
            "- Shift: Speed up FP Camera\n"
            "- U: Toggle Render Stats\n"
        )
        shortcuts_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(shortcuts_text)
        dialog.setLayout(layout)
        dialog.exec()