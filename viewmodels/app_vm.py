from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtWidgets import QFileDialog

import logging
import os
from pathlib import Path
import threading

# Importa tu lógica de backend de RoboForger
from RoboForger.forger.cad_parser import CADParser
from RoboForger.forger.converter import Converter
from RoboForger.drawing.draw import Draw
from RoboForger.utils import export_str2txt  # Asegúrate de que esta función exista y funcione


class AppViewModel(QObject):
    # Señales para notificar cambios en las propiedades de QML
    figuresFoundChanged = Signal()
    linesFoundChanged = Signal()
    arcsFoundChanged = Signal()
    isProcessingChanged = Signal()
    consoleOutputChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._figures_found = 0
        self._lines_found = 0
        self._arcs_found = 0
        self._is_processing = False
        self._console_output = ""  # Para la salida de la consola

        # Redirigir la salida del log a nuestro ViewModel
        self._log_handler = ConsoleLogHandler(self)
        logging.getLogger().addHandler(self._log_handler)
        logging.getLogger().setLevel(logging.INFO)  # Ajusta el nivel de log según necesites

    # Propiedades para la retroalimentación
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

    # Propiedad para el estado de procesamiento (para TLoader)
    @Property(bool, notify=isProcessingChanged)
    def isProcessing(self):
        return self._is_processing

    @isProcessing.setter
    def isProcessing(self, value):
        if self._is_processing != value:
            self._is_processing = value
            self.isProcessingChanged.emit()

    # Propiedad para la salida de la consola
    @Property(str, notify=consoleOutputChanged)
    def consoleOutput(self):
        return self._console_output

    @consoleOutput.setter
    def consoleOutput(self, value):
        if self._console_output != value:
            self._console_output = value
            self.consoleOutputChanged.emit()

    @Slot(str)
    def appendConsoleOutput(self, text):
        self.consoleOutput = self.consoleOutput + text + "\n"

    @Slot()
    def clearConsoleOutput(self):
        self.consoleOutput = ""

    @Slot()
    def addDxfFile(self):
        logging.info("Opening file dialog for DXF...")
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Select DXF File", "", "DXF Files (*.dxf)"
        )
        if file_path:
            logging.info(f"Selected file: {file_path}")
            self.processDxfFile(file_path)
        else:
            logging.info("No DXF file selected.")

    @Slot(str)
    def processDxfFile(self, file_path):
        if self.isProcessing:
            logging.warning("Already processing a file. Please wait.")
            return

        self.clearConsoleOutput()
        self.isProcessing = True
        self.figuresFound = 0
        self.linesFound = 0
        self.arcsFound = 0
        logging.info(f"Starting processing of {Path(file_path).name}...")

        # Ejecutar la lógica en un hilo separado para no bloquear la UI
        # Para aplicaciones más robustas, considera QThreadPool o QRunnable
        threading.Thread(target=self._run_dxf_processing, args=(file_path,)).start()

    def _run_dxf_processing(self, file_path):
        try:
            parser = CADParser(filepath=file_path, scale=1.0)
            lines = parser.get_lines()
            raw_arcs = parser.get_arcs()
            raw_circles = parser.get_circles()

            converter = Converter(float_precision=4)
            polylines = converter.convert_lines_to_polylines(lines)
            arcs = converter.convert_arcs(raw_arcs)
            circles = converter.convert_circles(raw_circles)

            # Actualizar las propiedades QML
            self.figuresFound = len(polylines) + len(arcs) + len(circles)
            self.linesFound = len(polylines)
            self.arcsFound = len(arcs)

            logging.info(f"Detected Polylines: {len(polylines)}")
            logging.info(f"Detected Arcs: {len(arcs)}")
            logging.info(f"Detected Circles: {len(circles)}")

            # Aquí puedes almacenar los datos procesados si necesitas acceder a ellos
            # para la función de guardar Rapid Code. Por ejemplo:
            self._processed_polylines = polylines
            self._processed_arcs = arcs
            self._processed_circles = circles
            self._current_file_name = Path(file_path).stem

            logging.info("DXF file processed successfully.")

        except Exception as e:
            logging.error(f"Error processing DXF file: {e}")
        finally:
            self.isProcessing = False
            logging.info("Processing finished.")

    @Slot()
    def saveRapidCode(self):
        if not hasattr(self, '_processed_polylines') or not self._processed_polylines:
            logging.warning("No DXF file processed yet or no figures found to save.")
            return

        logging.info("Opening file dialog to save Rapid Code...")
        file_dialog = QFileDialog()
        default_file_name = f"{self._current_file_name}_rapid_code.txt" if hasattr(self,
                                                                                   '_current_file_name') else "rapid_code.txt"
        file_path, _ = file_dialog.getSaveFileName(
            None, "Save Rapid Code", default_file_name, "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            logging.info(f"Saving Rapid Code to: {file_path}")
            try:
                draw = Draw(use_detector=True)
                draw.add_figures(self._processed_polylines)
                draw.add_figures(self._processed_arcs)
                draw.add_figures(self._processed_circles)

                rapid_code = draw.generate_rapid_code(use_offset=True)
                export_str2txt(rapid_code, filepath=file_path)
                logging.info("Rapid Code saved successfully.")
            except Exception as e:
                logging.error(f"Error saving Rapid Code: {e}")
        else:
            logging.info("Save Rapid Code cancelled.")


# Clase para redirigir la salida del logger a nuestro ViewModel
class ConsoleLogHandler(logging.Handler):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))  # Formato simple

    def emit(self, record):
        msg = self.format(record)
        self.view_model.appendConsoleOutput(msg)