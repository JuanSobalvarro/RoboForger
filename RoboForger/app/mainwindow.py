from PySide6.QtWidgets import (
    QMainWindow,
    QGridLayout,
    QWidget,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QFrame,
    QMenuBar,
    QVBoxLayout,
    QDialog,
    QLabel,
)
from PySide6.QtGui import (
    QImage,
    QPixmap,
    QVector3D,
)
from PySide6.QtCore import (
    QSize,
    Signal,
    Qt,
)

from RoboForger.app.configuration import ConfigurationPanel
from RoboForger.app.preview.preview import Preview
from RoboForger.app.console import Console
from RoboForger.app.config import GlobalConfig
from RoboForger.app.preview.drawing.parameters import ProcessingParameters
from RoboForger.app.components.menubar import MenuBar
from RoboForger.utils import get_resource_path

import webbrowser

class RoboMainWindow(QMainWindow):

    load_file_request = Signal()
    process_file_request = Signal()
    save_file_request = Signal()

    def __init__(self, parameters: ProcessingParameters, global_config: GlobalConfig, parent=None):
        super().__init__(parent)

        self.parameters = parameters
        self.global_config = global_config

        self.resize(1200, 700)
        self.setWindowTitle("RoboForger")

        # configure window toolbar 
        self.menubar = MenuBar(self.global_config, self)
        self.setMenuBar(self.menubar)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_splitter = QSplitter(Qt.Orientation.Horizontal, central_widget)

        self.config_panel = ConfigurationPanel(self.parameters)
        self.config_panel.setMinimumWidth(280)
        # self.config_panel.setMaximumWidth(420)

        right_splitter = QSplitter(Qt.Orientation.Vertical, central_widget)
        # TODO: Customize directly the splitter handle so the hover is not captured by the separator line

        self.preview = Preview(global_config=self.global_config)
        self.load_limits()
        self.separator_line = QFrame()
        self.separator_line.setFixedHeight(2)   # visual + grab area
        self.separator_line.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.separator_line.setProperty("tag", "separator_collapsible")
        self.console = Console()

        right_splitter.addWidget(self.preview)
        right_splitter.addWidget(self.separator_line)
        right_splitter.addWidget(self.console)

        # Initial proportions (preview dominant)
        right_splitter.setStretchFactor(0, 3)
        right_splitter.setStretchFactor(1, 1)

        main_splitter.addWidget(self.config_panel)
        main_splitter.addWidget(right_splitter)

        main_splitter.setStretchFactor(0, 0)
        main_splitter.setStretchFactor(1, 1)

        # Layout wrapper
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(main_splitter)

        self.connect_signals()

    def load_limits(self):

        tuple_limits = self.parameters.get("workspace_limits")
        origin = self.parameters.get("origin")
        vector1 = QVector3D(*tuple_limits[0])
        vector2 = QVector3D(*tuple_limits[1])

        # now we need to adjust the limits by the origin, since the preview is centered at the origin
        vector1 += QVector3D(*origin)
        vector2 += QVector3D(*origin)

        self.preview.load_limits(vector1, vector2)


    def connect_signals(self):
        self.config_panel.load_file_request.connect(self.load_file_request)
        self.config_panel.process_file_request.connect(self.process_file_request)
        self.config_panel.save_file_request.connect(self.save_file_request)

        self.parameters.parameter_changed.connect(self.load_limits)
