import os
import sys
from PySide6.QtWidgets import QApplication, QWidget, QDialog, QVBoxLayout
from PySide6.QtGui import QIcon
from typing import List

from RoboForger.app.components.label import Label
from RoboForger.app.mainwindow import RoboMainWindow
from RoboForger.app.worker import ProcessWorker
from RoboForger.app.models.parameters import ProcessingParameters


class RoboforgerApp(QApplication):
    def __init__(self, argv, resource_dir):
        super().__init__(argv)

        self.widgets: List[QWidget] = []
        self._resource_dir = resource_dir

        self.setApplicationName("RoboForger")
        self.setWindowIcon(QIcon(os.path.join(resource_dir, "icon.ico")))

        # setup environment
        self.setup_environment()

        self.load_stylesheet([
            "main.qss",
            "labels.qss",
        ])

        self._process_worker = ProcessWorker(resource_dir=resource_dir)
        self._parameters = ProcessingParameters()

        self.setup_main_window()

        # default maximized
        self.main_window.showMaximized()

        self.connect_signals()

    def setup_environment(self):
        os.environ["QT3D_RENDERER"] = "opengl"

    def load_stylesheet(self, filenames: List[str] = []):
        stylesheet_dir = os.path.join(self._resource_dir, "styles")
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
        self.main_window = RoboMainWindow()

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
            lambda: self._process_worker.start_processing(self._parameters.snapshot())
        )
        self.main_window.save_file_request.connect(self._process_worker.save_rapid_code)

        # connect parameters
        self.main_window.config_panel.left_panel.on_scale_factor_changed.connect(
            lambda val: self._parameters.update("scale_factor", val)
        )
        self.main_window.config_panel.left_panel.on_float_precision_changed.connect(
            lambda val: self._parameters.update("float_precision", val)
        )
        self.main_window.config_panel.left_panel.on_polyline_velocity_changed.connect(
            lambda val: self._parameters.update("lines_velocity", val)
        )
        self.main_window.config_panel.left_panel.on_arc_velocity_changed.connect(
            lambda val: self._parameters.update("arcs_velocity", val)
        )
        self.main_window.config_panel.left_panel.on_circle_velocity_changed.connect(
            lambda val: self._parameters.update("circles_velocity", val)
        )
        self.main_window.config_panel.left_panel.on_lifting_height_changed.connect(
            lambda val: self._parameters.update("lifting", val)
        )
        self.main_window.config_panel.left_panel.on_auto_trace_changed.connect(
            lambda val: self._parameters.update("use_detector", val)
        )
        self.main_window.config_panel.left_panel.on_offset_programming_changed.connect(
            lambda val: self._parameters.update("use_offset", val)
        )

        self.main_window.config_panel.right_panel.on_tool_name_changed.connect(
            lambda val: self._parameters.update("tool_name", val)
        )
        self.main_window.config_panel.right_panel.on_origin_x_changed.connect(
            lambda val: self._parameters.update_tuple("origin", 0, val)
        )
        self.main_window.config_panel.right_panel.on_origin_y_changed.connect(
            lambda val: self._parameters.update_tuple("origin", 1, val)
        )
        self.main_window.config_panel.right_panel.on_origin_z_changed.connect(
            lambda val: self._parameters.update_tuple("origin", 2, val)
        )
        self.main_window.config_panel.right_panel.on_zero_x_changed.connect(
            lambda val: self._parameters.update_tuple("zero", 0, val)
        )
        self.main_window.config_panel.right_panel.on_zero_y_changed.connect(
            lambda val: self._parameters.update_tuple("zero", 1, val)
        )
        self.main_window.config_panel.right_panel.on_zero_z_changed.connect(
            lambda val: self._parameters.update_tuple("zero", 2, val)
        )
        self.main_window.config_panel.right_panel.on_inferior_limit_x_changed.connect(
            lambda val: self._parameters.update_tuple("inferior_limit", 0, val)
        )
        self.main_window.config_panel.right_panel.on_inferior_limit_y_changed.connect(
            lambda val: self._parameters.update_tuple("inferior_limit", 1, val)
        )
        self.main_window.config_panel.right_panel.on_inferior_limit_z_changed.connect(
            lambda val: self._parameters.update_tuple("inferior_limit", 2, val)
        )
        self.main_window.config_panel.right_panel.on_superior_limit_x_changed.connect(
            lambda val: self._parameters.update_tuple("superior_limit", 0, val)
        )
        self.main_window.config_panel.right_panel.on_superior_limit_y_changed.connect(
            lambda val: self._parameters.update_tuple("superior_limit", 1, val)
        )
        self.main_window.config_panel.right_panel.on_superior_limit_z_changed.connect(
            lambda val: self._parameters.update_tuple("superior_limit", 2, val)
        )

    def run(self) -> int:
        # self.aboutQt()

        # show all widgets
        for widget in self.widgets:
            widget.show()

        return super().exec()
