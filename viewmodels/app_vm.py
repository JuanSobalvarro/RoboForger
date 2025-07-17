from PySide6.QtCore import QObject, Signal, Property, Slot, QTimer
from PySide6.QtWidgets import QFileDialog

import logging
import os
from pathlib import Path
import threading
import sys # For atexit setup
import atexit # For cleanup on main thread exit

# Importa tu lógica de backend de RoboForger
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
    dxfFilePathChanged = Signal()
    processingError = Signal(str) # For errors that need a dialog/toast in QML
    processingCancelled = Signal() # New signal for cancellation

    def __init__(self, parent=None):
        super().__init__(parent)
        self._figures_found = 0
        self._lines_found = 0
        self._arcs_found = 0
        self._is_processing = False
        self._console_output = ""
        self._dxf_file_path = ""
        self._current_file_name = ""
        self._rapid_code = ""

        # Threading control
        self._cancel_flag = threading.Event() # Event to signal cancellation
        self._processing_thread: threading.Thread = None # Reference to the worker thread

        # Redirect log output
        self._log_handler = ConsoleLogHandler(self)
        logging.getLogger().addHandler(self._log_handler)
        logging.getLogger().setLevel(logging.INFO)

        # Register cleanup for when the main application exits
        atexit.register(self._on_exit)

    # --- Properties ---
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

    @Property(str, notify=dxfFilePathChanged)
    def dxfFilePath(self):
        return self._dxf_file_path

    @dxfFilePath.setter
    def dxfFilePath(self, value):
        if self._dxf_file_path != value:
            self._dxf_file_path = value
            self.dxfFilePathChanged.emit()
            self._current_file_name = Path(value).stem if value else ""

    # --- Slots for UI interaction ---
    @Slot(str)
    def appendConsoleOutput(self, text):
        self.consoleOutput = self.consoleOutput + text + "\n"

    @Slot()
    def clearConsoleOutput(self):
        self.consoleOutput = ""

    @Slot()
    def selectDxfFile(self):
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
            self.dxfFilePath = file_path
        else:
            logging.info("No DXF file selected.")
            self.dxfFilePath = ""

    @Slot()
    def processSelectedDxfFile(self):
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

        # Reset cancellation flag for new processing
        self._cancel_flag.clear()
        self._processing_thread = threading.Thread(target=self._run_dxf_processing, args=(self.dxfFilePath,))
        self._processing_thread.daemon = True # Make thread a daemon to allow main program to exit
        self._processing_thread.start()

    @Slot()
    def cancelProcessing(self):
        """
        Signals the worker thread to stop processing.
        """
        if self.isProcessing and self._processing_thread and self._processing_thread.is_alive():
            logging.info("Cancellation requested.")
            self._cancel_flag.set() # Set the event to signal cancellation
        else:
            logging.warning("No active processing to cancel.")

    def _run_dxf_processing(self, file_path):
        """
        Actual DXF processing logic, runs in a separate thread.
        This function should periodically check `_cancel_flag.is_set()`.
        """
        try:
            # Check for cancellation before starting major steps
            if self._cancel_flag.is_set():
                logging.info("Processing cancelled before parsing.")
                self.processingCancelled.emit()
                return

            parser = CADParser(filepath=file_path, scale=1.0)
            lines = parser.get_lines()
            raw_arcs = parser.get_arcs()
            raw_circles = parser.get_circles()

            if self._cancel_flag.is_set():
                logging.info("Processing cancelled after parsing.")
                self.processingCancelled.emit()
                return

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

            if self._cancel_flag.is_set():
                logging.info("Processing cancelled after conversion.")
                self.processingCancelled.emit()
                return

            # Store processed data for saving Rapid Code
            self._processed_polylines = polylines
            self._processed_arcs = arcs
            self._processed_circles = circles

            draw = Draw(use_detector=True)
            draw.add_figures(self._processed_polylines)
            draw.add_figures(self._processed_arcs)
            draw.add_figures(self._processed_circles)

            self._rapid_code = draw.generate_rapid_code(use_offset=True)

            if self._cancel_flag.is_set():
                logging.info("Processing cancelled after Rapid Code generation.")
                self.processingCancelled.emit()
                return

            logging.info("DXF file processed successfully.")

        except Exception as e:
            # Ensure errors are logged and emitted even if cancelled mid-way
            if self._cancel_flag.is_set():
                 logging.warning(f"Error during cancelled processing: {e}")
                 # You might choose not to emit processingError if it was a user-initiated cancel
            else:
                logging.error(f"Error processing DXF file: {e}")
                self.processingError.emit(f"Error processing DXF: {e}")
        finally:
            self.isProcessing = False # Always set to false when thread finishes
            if self._cancel_flag.is_set():
                logging.info("Processing fully stopped due to cancellation.")
                self.processingCancelled.emit() # Re-emit for certainty or if not emitted before
            else:
                logging.info("Processing finished.")

    @Slot()
    def saveRapidCode(self):
        if self.isProcessing:
            logging.warning("Cannot save Rapid Code while processing is active.")
            self.processingError.emit("Cannot save Rapid Code while processing is active.")
            return

        if not hasattr(self, '_processed_polylines') or not self._processed_polylines:
            logging.warning("No DXF file processed yet or no figures found to save.")
            self.processingError.emit("No DXF file processed yet or no figures found to save.")
            return
        if not self._rapid_code: # Check if rapid code was actually generated
            logging.warning("No Rapid Code generated to save.")
            self.processingError.emit("No Rapid Code generated to save.")
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

    def _on_exit(self):
        """
        Called when the Python interpreter is shutting down.
        Ensures worker threads are terminated cleanly.
        """
        logging.info("AppViewModel: Application exiting. Signalling threads to stop.")
        self.cancelProcessing() # Signal cancellation
        if self._processing_thread and self._processing_thread.is_alive():
            self._processing_thread.join(timeout=1.0)
            if self._processing_thread.is_alive():
                logging.warning("AppViewModel: Worker thread did not terminate gracefully.")


class ConsoleLogHandler(logging.Handler):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        QTimer.singleShot(0, lambda: self.view_model.appendConsoleOutput(msg))
