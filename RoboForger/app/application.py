import os
import sys
from PySide6.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout
from PySide6.QtGui import QIcon
from typing import List

from RoboForger.app.components.label import Label
from RoboForger.app.mainwindow import RoboMainWindow
from RoboForger.app.worker import ProcessWorker
from RoboForger.app.preview.drawing.parameters import ProcessingParameters
from RoboForger.utils import get_resource_path
from RoboForger.app.config import GlobalConfig


class RoboforgerApp(QApplication):
    def __init__(self, argv, resource_dir):
        super().__init__(argv)

        self.widgets: List[QWidget] = []
        self._resource_dir = resource_dir

        self._global_config = GlobalConfig(self)

        self.setApplicationName("RoboForger")
        self.setWindowIcon(QIcon(get_resource_path("icon.ico")))

        # setup environment
        self.setup_environment()

        self.load_stylesheet([
            "main.qss",
            "labels.qss",
            "menubar.qss",
        ])

        self._parameters = ProcessingParameters() # singleton for processing parameters, shared across the app
        self._process_worker = ProcessWorker(parameters=self._parameters,)

        self.setup_main_window()

        # default maximized
        self.main_window.showMaximized()

        self.connect_signals()

    def setup_environment(self):
        pass
        # os.environ["QT3D_RENDERER"] = "opengl"

    def load_stylesheet(self, filenames: List[str] = []):
        stylesheet_dir = get_resource_path("styles")
        stylesheet = ""
        for file in filenames:
            try:
                with open(os.path.join(stylesheet_dir, file), 'r') as f:
                    stylesheet_str = f.read()
                    stylesheet += stylesheet_str + "\n"
            except Exception as e:
                print(f"Failed to load stylesheet: {e}")
                sys.exit(1)

        self.setStyleSheet(stylesheet)

    def setup_main_window(self):
        self.main_window = RoboMainWindow(self._parameters, self._global_config)

        self.widgets.append(self.main_window)
    
    def show_error_message(self, message: str):
        error_dialog = QDialog()
        error_dialog.setWindowTitle("Error")

        layout = QVBoxLayout()

        error = Label(message)
        layout.addWidget(error)

        error_dialog.setLayout(layout)

        error_dialog.exec()

    def connect_signals(self):
        self._process_worker.processError.connect(self.show_error_message)

        self._process_worker.fileLoaded.connect(
            lambda: self.main_window.preview.load_figures(
                self._process_worker._forger.get_figures()
            )
        )

        self.main_window.load_file_request.connect(self._process_worker.load_file)
        self.main_window.process_file_request.connect(
            lambda: self._process_worker.start_processing()
        )
        self.main_window.save_file_request.connect(self._process_worker.save_rapid_code)

    def run(self) -> int:
        # self.aboutQt()

        # show all widgets
        for widget in self.widgets:
            widget.show()

        return super().exec()
