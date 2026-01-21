import os
from PySide6.QtWidgets import QApplication, QWidget
from typing import List

from RoboForger.app.mainwindow import RoboMainWindow


class RoboforgerApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.widgets: List[QWidget] = []

        # setup environment
        self.setup_environment()

        self.setup_main_window()

    def setup_environment(self):
        os.environ["QT3D_RENDERER"] = "opengl"

    def setup_main_window(self):
        self.main_window = RoboMainWindow()

        self.widgets.append(self.main_window)

    def run(self) -> int:
        # self.aboutQt()

        # show all widgets
        for widget in self.widgets:
            widget.show()

        return super().exec()