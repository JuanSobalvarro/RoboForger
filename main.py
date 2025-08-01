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

def run_gui_app():

    app = QApplication(sys.argv)
    darkPalette = QPalette()
    darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))  # Main window background
    app.setPalette(darkPalette)

    app.setWindowIcon(QIcon(os.path.join(ASSETS_DIR, 'img', 'icon.png')))

    logging.info("Starting RoboForger")

    engine = QQmlApplicationEngine()
    engine.addImportPath('qml')
    engine.addImportPath('qml/viewmodels') # Asegúrate de que QML pueda encontrar tu ViewModel

    # Crea una instancia de tu ViewModel y la expone a QML
    app_view_model = AppViewModel()
    engine.rootContext().setContextProperty("appViewModel", app_view_model)

    logging.info("ViewModels Loaded Successfully")

    engine.load('qml/App.qml')

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