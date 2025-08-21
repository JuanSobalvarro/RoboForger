# Copyright
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from pathlib import Path

from PySide6.QtCore import Property, QObject, Signal, Slot, QUrl
from PySide6.QtQml import QmlElement, QmlSingleton

from roboforger_app.pyobjects.dxf_worker import DxfWorker
from roboforger_app.pyobjects.console_logger import ConsoleLogger


QML_IMPORT_NAME = "ApplicationObjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlSingleton
class Orchestrator(QObject):
    # -- SIGNALS -- #
    isProcessingChanged = Signal()
    processingFinished = Signal()
    dxfWorkerChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isProcessing = False

        self._console_logger = ConsoleLogger()
        self._console_logger.start()

        self._dxf_worker = DxfWorker()
        self._dxf_worker.processingStarted.connect(self._on_processing_started)
        self._dxf_worker.processingFinished.connect(self._on_processing_finished)

    # -- PROPERTIES -- #
    @Property(QObject, constant=True)
    def consoleLogger(self):
        """
        Exposes the console logger to QML for real-time logging.
        """
        return self._console_logger

    @Property(QObject, notify=dxfWorkerChanged)  # Necesitarás esta señal y propiedad
    def dxfWorker(self):
        return self._dxf_worker

    @Property(bool, notify=isProcessingChanged)
    def isProcessing(self):
        return self._isProcessing
    
    @Property(str, constant=True)
    def testProperty(self):
        return "Hello from Orchestrator!"

    # -- SLOTS -- #
    @Slot()
    def startProcessing(self):
        self._dxf_worker.start()

    @Slot()
    def cancelProcessing(self):
        self._dxf_worker.cancel()

    @Slot(str)
    def dxfSelectFile(self, file_path: str):
        """
        Slot to be called from QML when a DXF file is selected.
        """
        logging.info(f"DXF file selected: {file_path}")

        # Convert the file from resource format (file:///path/to/file.dxf)
        if file_path.startswith("file:///"):
            file_path = Path(file_path[8:])
        else:
            file_path = Path(file_path)
        self._dxf_worker.load_file(file_path)

    @Slot(str)
    def rapidSaveFile(self, file_path: str):
        """
        Slot to be called from QML when the rapid code file is saved.
        """
        if file_path.startswith("file:///"):
            file_path = Path(file_path[8:])
        else:
            file_path = Path(file_path)
        self._dxf_worker.save_file(file_path)

    @Slot()
    def onFileDialogCancelled(self):
        logging.info("File dialog cancelled")

    def _on_processing_started(self):
        logging.info("Processing started")
        self._isProcessing = True
        self.isProcessingChanged.emit()

    def _on_processing_finished(self):
        logging.info("Processing finished")
        self._isProcessing = False
        self.isProcessingChanged.emit()
        self.processingFinished.emit()

