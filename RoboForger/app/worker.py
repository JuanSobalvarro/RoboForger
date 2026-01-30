from PySide6.QtWidgets import (
    QFileDialog,
)
from PySide6.QtCore import (
    QObject,
    Signal,
    Slot,
)

from RoboForger.forger import Forger

import multiprocessing
import threading
import logging
from math import isnan


def _processing_function(file_path: str, result_queue: multiprocessing.Queue, params: dict):
    """
    Run the full pipeline inside a separate process using Forger and return the RAPID code.
    Any exception is put back into the queue to be handled in the UI thread.
    """
    try:
        forger = Forger(
            resource_dir=params["resource_dir"],
            origin=params["origin"],
            zero=params["zero"],
            pre_scale=params["scale"],
            float_precision=params["float_precision"],
            lifting=params["lifting"],
            tool_name=params["tool_name"],
            global_velocity=params["lines_velocity"],
            polyline_velocity=params["lines_velocity"],
            arc_velocity=params["arcs_velocity"],
            circle_velocity=params["circles_velocity"],
            spline_velocity=params.get("splines_velocity", params["lines_velocity"]),
            workspace_limits=(params["inferior_limit"], params["superior_limit"]),
            use_intelligent_traces=params["use_detector"],
            use_offset_programming=params["use_offset"],
        )

        # Full pipeline
        forger.parse_figures(file_path)
        forger.convert_figures()
        forger.generate_rapid_code()

        result_queue.put({
            "rapid_code": forger.get_rapid_code(),
        })
    except Exception as e:
        # Send the exception object so the monitor can emit processingError
        result_queue.put(e)


class ProcessWorker(QObject):
    """
    Orchestrator class manage the application logic and interactions between components.

    The only logic we use are:
    - Load CAD File
    - Process File
    - Save to RAPID code
    """
    processStart = Signal()
    processFinish = Signal()
    processError = Signal(str)

    fileLoaded = Signal()

    def __init__(self, resource_dir: str, parent=None):
        super().__init__(parent)

        # forger instance (preview for figures)
        self._forger = Forger(resource_dir=resource_dir)
        # process/threading
        self._process: multiprocessing.Process | None = None
        self._result_queue: multiprocessing.Queue | None = None
        self._is_running: bool = False

        # current file path
        self._selected_file_path: str | None = None
        self._save_path: str | None = None

        self._rapid_code: str = ""

    @Slot()
    def load_file(self):
        """
        Load a DXF file for processing.
        """
        print("Loading CAD file...")
        # open file dialog 
        file_dialog = QFileDialog()
        # filter for DWG and DXF files
        file_dialog.setNameFilter("CAD Files (*.dxf *.dwg)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self._selected_file_path = file_path
        else:
            logging.log(level=logging.INFO, msg="File dialog cancelled or no file selected.")
            return  # User cancelled the dialog
        
        if not self._selected_file_path:
            logging.log(level=logging.WARNING, msg="No file selected after dialog.")
            return

        try:
            self._forger.parse_figures(self._selected_file_path)
        except Exception as e:
            self.processError.emit(f"Failed loading file: {e}")
            return
    
        self.fileLoaded.emit()

    @Slot(dict)
    def start_processing(self, params: dict):
        """
        Starts the processing in a separate process.
        """
        try:
            if self._is_running:
                print("Processing is already running.")
                return
            if not self._selected_file_path:
                # print("No file selected. Please load a DXF file before starting processing.")
                # print("No file selected. Please load a CAD file(DXF, DWG) before starting processing.")
                self.processError.emit("No file selected. Please load a CAD file(DXF, DWG) before starting processing.")
                return
            # if not self._validate_parameters():
            #     print("Invalid parameters. Please check your settings.")
            #     return

            self._is_running = True
            self.processStart.emit()
            logging.log(level=logging.INFO, msg="Starting processing...")

            self._result_queue = multiprocessing.Queue()
            params = self._forger.parameters_dict()

            self._process = multiprocessing.Process(
                target=_processing_function,
                name="DxfProcessingWorker",
                args=(self._selected_file_path, self._result_queue, params),
            )
            self._process.start()

            # Monitor results from a lightweight thread
            threading.Thread(target=self._monitor_process, daemon=True).start()

        except Exception as e:
            self._is_running = False
            self.processError.emit(f"Exception starting processing: {str(e)}")

    @Slot()
    def save_rapid_code(self):
        """
        Save the generated RAPID code to a file.
        """
        if not self._rapid_code:
            print("No RAPID code to save. Please process a file first.")
            return

        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setNameFilter("RAPID Files (*.mod *.prg)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                save_path = selected_files[0]
                self._save_path = save_path
        else:
            logging.log(level=logging.INFO, msg="Save file dialog cancelled or no file selected.")
            return  # User cancelled the dialog

        if not self._save_path:
            logging.log(level=logging.WARNING, msg="No save path selected after dialog.")
            return

        try:
            with open(self._save_path, 'w') as f:
                f.write(self._rapid_code)
        except Exception as e:
            self.processError.emit(f"Failed saving RAPID code: {e}")

    def _monitor_process(self):
        try:
            result = self._result_queue.get()
            if isinstance(result, Exception):
                self._rapid_code = ""
                self.processError.emit(f"Exception during processing: {str(result)}")
            else:
                self._rapid_code = result.get("rapid_code", "")
                logging.log(level=logging.INFO, msg="Processing finished successfully.")
                self.processFinish.emit()
        except Exception as e:
            self._rapid_code = ""
            self.processError.emit(f"Exception during monitoring: {str(e)}")
        finally:
            try:
                if self._process:
                    self._process.join()
            finally:
                self._is_running = False



