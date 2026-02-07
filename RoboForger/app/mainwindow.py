from PySide6.QtWidgets import (
    QMainWindow,
    QGridLayout,
    QWidget,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QFrame,
    QToolBar,
)
from PySide6.QtCore import (
    QSize,
    Signal,
    Qt,
)

from RoboForger.app.configuration import ConfigurationPanel
from RoboForger.app.preview.preview import Preview
from RoboForger.app.console import Console


class RoboMainWindow(QMainWindow):

    load_file_request = Signal()
    process_file_request = Signal()
    save_file_request = Signal()

    def __init__(self):
        super().__init__()

        self.resize(1200, 700)
        self.setWindowTitle("RoboForger")

        # configure window toolbar 
        self.load_toolbar()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_splitter = QSplitter(Qt.Orientation.Horizontal, central_widget)

        self.config_panel = ConfigurationPanel()
        self.config_panel.setMinimumWidth(280)
        # self.config_panel.setMaximumWidth(420)

        right_splitter = QSplitter(Qt.Orientation.Vertical, central_widget)
        # TODO: Customize directly the splitter handle so the hover is not captured by the separator line

        self.preview = Preview()
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

    def load_toolbar(self):
        toolbar = QToolBar("Main Toolbar", self)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMaximumSize(QSize(16777215, 20))
        toolbar.setMinimumSize(QSize(0, 20))
        toolbar.setMovable(False)

        # help menu
        # toolbar.addAction("Help", self.show_help_message)


        self.addToolBar(toolbar)

    def connect_signals(self):
        self.config_panel.load_file_request.connect(self.load_file_request)
        self.config_panel.process_file_request.connect(self.process_file_request)
        self.config_panel.save_file_request.connect(self.save_file_request)
