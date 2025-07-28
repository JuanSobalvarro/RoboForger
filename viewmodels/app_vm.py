from PySide6.QtCore import QObject, Signal, Property, Slot, QTimer, QThreadPool
from PySide6.QtWidgets import QFileDialog

import logging
import os
from pathlib import Path
import threading
import sys # For atexit setup
import atexit # For cleanup on main thread exit
import time

# Importa tu lógica de backend de RoboForger
from RoboForger.forger.cad_parser import CADParser
from RoboForger.forger.converter import Converter
from RoboForger.drawing.draw import Draw
from RoboForger.utils import export_str2txt

from viewmodels.dxf_worker import DxfWorker
from viewmodels.file_dialog import FileDialogManager

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class AppViewModel(QObject):
    # -- SIGNALS -- #
    isProcessingChanged = Signal()
    processingFinished = Signal()
    fileDialogManagerChanged = Signal()
    dxfWorkerChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isProcessing = False

        self._dxf_worker = DxfWorker()
        self._dxf_worker.processingStarted.connect(self._on_processing_started)
        self._dxf_worker.processingFinished.connect(self._on_processing_finished)

        self._file_dialog_manager = FileDialogManager()
        self._file_dialog_manager.fileSelected.connect(self._on_dxf_file_selected_from_dialog)
        self._file_dialog_manager.fileSaved.connect(self._on_dxf_file_saved_from_dialog)
        self._file_dialog_manager.fileDialogCancelled.connect(self._on_dxf_file_dialog_cancelled)

    # -- PROPERTIES -- #
    @Property(QObject, notify=fileDialogManagerChanged)
    def fileDialogManager(self):
        return self._file_dialog_manager

    @Property(QObject, notify=dxfWorkerChanged)  # Necesitarás esta señal y propiedad
    def dxfWorker(self):
        return self._dxf_worker

    @Property(bool, notify=isProcessingChanged)
    def isProcessing(self):
        return self._isProcessing

    # -- SLOTS -- #
    @Slot()
    def startProcessing(self):
        self._dxf_worker.start()

    @Slot()
    def cancelProcessing(self):
        self._dxf_worker.cancel()

    @Slot()
    def selectDxfFile(self):
        """
        Opens a file dialog to select a DXF file.
        """
        self._file_dialog_manager.showOpenFileNameDialog(title="Select a DXF File",
                                                         filter="DXF Files (*.dxf);;All Files (*)",
                                                        default_dir=Path.home(),
                                                        selected_filter="DXF Files (*.dxf)")

    @Slot()
    def saveRapidCode(self):
        """
        Opens a file dialog to save the rapid code to a file.
        """
        try:
            self._dxf_worker.get_rapid_code()
        except Exception as e:
            logging.error(f"Error getting rapid code: {e}")
            return

        self._file_dialog_manager.showSaveFileNameDialog(title="Save Rapid Code",
                                                         filter="Text Files (*.txt);;All Files (*)",
                                                         default_dir=Path.home(),
                                                         selected_filter="Text Files (*.txt)")

    @Slot(str)
    def _on_dxf_file_selected_from_dialog(self, file_path: str):
        logging.info(f"DXF file selected: {file_path}")
        self._dxf_worker.load_file(file_path)

    @Slot(str)
    def _on_dxf_file_saved_from_dialog(self, file_path: str):
        logging.info(f"DXF file saved: {file_path}")
        self._dxf_worker.save_file(file_path)

    @Slot()
    def _on_dxf_file_dialog_cancelled(self):
        logging.info("DXF file dialog cancelled")

    def _on_processing_started(self):
        logging.info("Processing started")
        self._isProcessing = True
        self.isProcessingChanged.emit()

    def _on_processing_finished(self):
        logging.info("Processing finished")
        self._isProcessing = False
        self.isProcessingChanged.emit()
        self.processingFinished.emit()

