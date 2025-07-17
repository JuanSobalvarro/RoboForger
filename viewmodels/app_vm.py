from PySide6.QtCore import QObject, Signal, Property, Slot, QTimer
from PySide6.QtWidgets import QFileDialog

import logging
import os
from pathlib import Path
import threading

from RoboForger.forger.cad_parser import CADParser
from RoboForger.forger.converter import Converter
from RoboForger.drawing.draw import Draw
from RoboForger.utils import export_str2txt

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class AppViewModel(QObject):
    # Signals for QML property changes
    figuresFoundChanged = Signal()
    linesFoundChanged = Signal()
    arcsFoundChanged = Signal()
    isProcessingChanged = Signal()
    consoleOutputChanged = Signal()
    # New signal for loaded file path (useful for UI feedback)
    dxfFilePathChanged = Signal()
    # New signal for errors that need a dialog/toast in QML
    processingError = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._figures_found = 0
        self._lines_found = 0
        self._arcs_found = 0
        self._is_processing = False
        self._console_output = ""
        self._dxf_file_path = "" # To store the path of the last loaded DXF
        self._current_file_name = "" # Store the name for saving
        self._rapid_code = "" # To store the generated Rapid Code

        # Redirect log output to our ViewModel
        self._log_handler = ConsoleLogHandler(self)
        logging.getLogger().addHandler(self._log_handler)
        logging.getLogger().setLevel(logging.INFO)

    # Properties for feedback
    @Property(int, notify=figuresFoundChanged)
    def figuresFound(self):
        return self._figures_found

    @figuresFound.setter
    def figuresFound(self, value):
        if self._figures_found != value:
            self._figures_found = value
            self.figuresFoundChanged.emit()

    @Property(int, notify=linesFoundChanged)
    def linesFound(self):
        return self._lines_found

    @linesFound.setter
    def linesFound(self, value):
        if self._lines_found != value:
            self._lines_found = value
            self.linesFoundChanged.emit()

    @Property(int, notify=arcsFoundChanged)
    def arcsFound(self):
        return self._arcs_found

    @arcsFound.setter
    def arcsFound(self, value):
        if self._arcs_found != value:
            self._arcs_found = value
            self.arcsFoundChanged.emit()

    @Property(bool, notify=isProcessingChanged)
    def isProcessing(self):
        return self._is_processing

    @isProcessing.setter
    def isProcessing(self, value):
        if self._is_processing != value:
            self._is_processing = value
            self.isProcessingChanged.emit()

    @Property(str, notify=consoleOutputChanged)
    def consoleOutput(self):
        return self._console_output

    @consoleOutput.setter
    def consoleOutput(self, value):
        if self._console_output != value:
            self._console_output = value
            self.consoleOutputChanged.emit()

    # New property to hold the selected DXF file path
    @Property(str, notify=dxfFilePathChanged)
    def dxfFilePath(self):
        return self._dxf_file_path

    @dxfFilePath.setter
    def dxfFilePath(self, value):
        if self._dxf_file_path != value:
            self._dxf_file_path = value
            self.dxfFilePathChanged.emit()
            # Also update the current file name for saving purposes
            self._current_file_name = Path(value).stem if value else ""

    @Slot(str)
    def appendConsoleOutput(self, text):
        self.consoleOutput = self.consoleOutput + text + "\n"

    @Slot()
    def clearConsoleOutput(self):
        self.consoleOutput = ""

    @Slot()
    def selectDxfFile(self):
        """
        Opens a file dialog to select a DXF file and stores its path.
        This method must be called from the main (GUI) thread.
        """
        if self.isProcessing:
            logging.warning("Cannot select new DXF while processing is active.")
            self.processingError.emit("Cannot select new DXF while processing is active.")
            return

        logging.info("Opening file dialog for DXF...")
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Select DXF File", "", "DXF Files (*.dxf)"
        )
        if file_path:
            logging.info(f"Selected file: {file_path}")
            self.dxfFilePath = file_path # Update the ViewModel property
        else:
            logging.info("No DXF file selected.")
            self.dxfFilePath = "" # Clear path if cancelled

    @Slot()
    def processSelectedDxfFile(self):
        """
        Initiates the processing of the currently selected DXF file.
        This slot is called by the "Process" button in QML.
        """
        if not self.dxfFilePath:
            logging.warning("No DXF file selected to process.")
            self.processingError.emit("No DXF file selected to process.")
            return
        if self.isProcessing:
            logging.warning("Already processing a file. Please wait.")
            self.processingError.emit("Already processing a file. Please wait.")
            return

        self.clearConsoleOutput()
        self.isProcessing = True
        self.figuresFound = 0
        self.linesFound = 0
        self.arcsFound = 0
        logging.info(f"Starting processing of {Path(self.dxfFilePath).name}...")

        threading.Thread(target=self._run_dxf_processing, args=(self.dxfFilePath,)).start()

    def _run_dxf_processing(self, file_path):
        """
        Actual DXF processing logic, runs in a separate thread.
        """
        try:
            parser = CADParser(filepath=file_path, scale=1.0)
            lines = parser.get_lines()
            raw_arcs = parser.get_arcs()
            raw_circles = parser.get_circles()

            converter = Converter(float_precision=4)
            polylines = converter.convert_lines_to_polylines(lines)
            arcs = converter.convert_arcs(raw_arcs)
            circles = converter.convert_circles(raw_circles)

            self.figuresFound = len(polylines) + len(arcs) + len(circles)
            self.linesFound = len(polylines)
            self.arcsFound = len(arcs)

            logging.info(f"Detected Polylines: {len(polylines)}")
            logging.info(f"Detected Arcs: {len(arcs)}")
            logging.info(f"Detected Circles: {len(circles)}")

            # Store processed data for saving Rapid Code
            self._processed_polylines = polylines
            self._processed_arcs = arcs
            self._processed_circles = circles

            draw = Draw(use_detector=True)
            draw.add_figures(self._processed_polylines)
            draw.add_figures(self._processed_arcs)
            draw.add_figures(self._processed_circles)

            self._rapid_code = draw.generate_rapid_code(use_offset=True)

            logging.info("DXF file processed successfully.")

        except Exception as e:
            logging.error(f"Error processing DXF file: {e}")
            self.processingError.emit(f"Error processing DXF: {e}") # Emit error to QML
        finally:
            self.isProcessing = False
            logging.info("Processing finished.")

    @Slot()
    def saveRapidCode(self):
        """
        Opens a file dialog to save Rapid Code generated from processed DXF.
        This method must be called from the main (GUI) thread.
        """
        if self.isProcessing:
            logging.warning("Cannot save Rapid Code while processing is active.")
            self.processingError.emit("Cannot save Rapid Code while processing is active.")
            return

        # Check if processing has occurred and there's data to save
        if not hasattr(self, '_processed_polylines') or not self._processed_polylines:
            logging.warning("No DXF file processed yet or no figures found to save.")
            self.processingError.emit("No DXF file processed yet or no figures found to save.")
            return

        logging.info("Opening file dialog to save Rapid Code...")
        file_dialog = QFileDialog()
        default_file_name = f"{self._current_file_name}_rapid_code.txt" if self._current_file_name else "rapid_code.txt"

        file_path, _ = file_dialog.getSaveFileName(
            None, "Save Rapid Code", default_file_name, "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            logging.info(f"Saving Rapid Code to: {file_path}")
            try:

                export_str2txt(self._rapid_code, filepath=file_path)
                logging.info("Rapid Code saved successfully.")
            except Exception as e:
                logging.error(f"Error saving Rapid Code: {e}")
                self.processingError.emit(f"Error saving Rapid Code: {e}")
        else:
            logging.info("Save Rapid Code cancelled.")


class ConsoleLogHandler(logging.Handler):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        QTimer.singleShot(0, lambda: self.view_model.appendConsoleOutput(msg))