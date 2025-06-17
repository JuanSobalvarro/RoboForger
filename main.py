import logging
import os
import sys
import argparse

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')


def run_gui_app():
    os.environ["QT_QUICK_CONTROLS_CONF"] = "qtquickcontrols2.conf"

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(ASSETS_DIR, 'img', 'icon.png')))

    logging.info("Starting RoboForger")

    engine = QQmlApplicationEngine()
    engine.addImportPath('qml')

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
    run_gui_app()


if __name__ == "__main__":
    main()
