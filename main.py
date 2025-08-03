import logging
import os
import sys
import argparse
import multiprocessing

from PySide6.QtGui import QIcon, QPalette, QColor
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from viewmodels.app_vm import AppViewModel

from ui import line_geometry, arc_geometry, circle_geometry

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')

import resources_rc

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, handling both development and
    PyInstaller-frozen environments.
    """
    if getattr(sys, 'frozen', False):
        # We are running as a PyInstaller-frozen executable.
        # The base path is the temporary directory where files are extracted.
        base_path = sys._MEIPASS
    else:
        # We are running in a regular Python environment.
        # The base path is the directory of the current script.
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

def run_gui_app():

    app = QApplication(sys.argv)
    darkPalette = QPalette()
    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))  # Main window background
    app.setPalette(darkPalette)

    icon_path = get_resource_path(os.path.join('assets', 'img', 'icon.png'))
    app.setWindowIcon(QIcon(icon_path))

    logging.info("Starting RoboForger")

    engine = QQmlApplicationEngine()
    qml_dir = get_resource_path('qml')
    engine.addImportPath(qml_dir)

    # Crea una instancia de tu ViewModel y la expone a QML
    app_view_model = AppViewModel()
    engine.rootContext().setContextProperty("appViewModel", app_view_model)

    logging.info("ViewModels Loaded Successfully")

    main_qml_path = get_resource_path(os.path.join('qml', 'App.qml'))
    engine.load(main_qml_path)

    if not engine.importPathList():
        logging.error("No import paths found")
        sys.exit(-1)

    if not engine.rootObjects():
        logging.error("No QML found")
        sys.exit(-1)

    logging.info("Application Started Successfully")
    sys.exit(app.exec())


def main():
    multiprocessing.freeze_support()
    run_gui_app()


if __name__ == "__main__":
    main()