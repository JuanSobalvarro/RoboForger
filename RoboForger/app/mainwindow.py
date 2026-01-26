from PySide6.QtWidgets import (
    QMainWindow,
    QGridLayout,
    QWidget,
    QSizePolicy,
)
from PySide6.QtCore import (
    QSize,
    Signal,
)

from RoboForger.app.configuration import ConfigurationPanel
from RoboForger.app.preview import Preview
from RoboForger.app.console import Console


class RoboMainWindow(QMainWindow):
    
    load_file_request = Signal()
    process_file_request = Signal()
    save_file_request = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RoboForger")
        # Initial size
        self.setGeometry(100, 100, 1200, 800) 

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QGridLayout(central_widget)
        
        # widgets
        
        self.config_panel = ConfigurationPanel()
        layout.addWidget(self.config_panel, 0, 0, 2, 1)

        self.preview = Preview()
        layout.addWidget(self.preview, 0, 1)

        self.console = Console()
        layout.addWidget(self.console, 1, 1)

        # SET MINIMUM SIZE CONSTRAINTS 
        min_preview_width = int(self.width() * 2 / 3) 
        self.preview.setMinimumWidth(min_preview_width)

        min_preview_height = int(self.height() * 2 / 3)
        self.preview.setMinimumHeight(min_preview_height)

        # SET MAXIMUM SIZE CONSTRAINTS
        self.preview.setMaximumSize(QSize(int(self.width() * 2 / 3), int(self.height() * 2 / 3)))
        
        # CONFIGURE STRETCH FACTORS (Proportions) 
        
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)

        self.setLayout(layout)

        self.connect_signals()

    def connect_signals(self):
        self.config_panel.load_file_request.connect(self.load_file_request)
        self.config_panel.process_file_request.connect(self.process_file_request)
        self.config_panel.save_file_request.connect(self.save_file_request)
