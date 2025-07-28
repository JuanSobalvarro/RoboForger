import logging
import time
import os
import multiprocessing
import threading

from PySide6.QtCore import QObject, Signal, Property

from RoboForger.forger.cad_parser import CADParser

from models.line_model import LineModel
from models.arc_model import ArcModel
from models.circle_model import CircleModel


# from RoboForger.drawing.draw import Draw

def processing_function(file_path, *args, **kwargs):
    """
    Simulates a long-running processing function.
    This function is intended to be run in a separate thread.
    """
    print("Simulating long running operation...")
    print(f"File path: {file_path}")
    print(f"Arguments: {args}")
    print(f"Keyword Arguments: {kwargs}")
    time.sleep(10)  # Simulate a delay
    print("Processing completed.")

class DxfWorker(QObject):
    """
    Worker class for handling DXF file operations.
    """
    processingStarted = Signal()
    processingFinished = Signal()
    processingError = Signal()
    fileLoaded = Signal()
    linesChanged = Signal()
    arcsChanged = Signal()
    circlesChanged = Signal()

    # parameters signals
    scaleChanged = Signal(float)
    floatPrecisionChanged = Signal(int)
    linesVelocityChanged = Signal(int)
    arcsVelocityChanged = Signal(int)
    circlesVelocityChanged = Signal(int)
    useDetectorChanged = Signal(bool)
    useOffsetChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._process: multiprocessing.Process = None

        self._selected_file_path = ""
        self._save_path = ""

        # Models
        self._line_model = LineModel()
        self._arc_model = ArcModel()
        self._circle_model = CircleModel()

        # DXF PARAMETERS
        self._scale: float = None
        self._float_precision: int = None
        self._lines_velocity: int = None
        self._arcs_velocity: int = None
        self._circles_velocity: int = None
        self._use_detector: bool = False
        self._use_offset: bool = False

        # figures
        self._raw_lines = []
        self._raw_arcs = []
        self._raw_circles = []

        self._lines = []
        self._arcs = []
        self._circles = []

        self._rapid_code: str = None

        self._is_running = False

    # -- PROPERTIES -- #
    @Property(QObject, notify=fileLoaded)
    def lineModel(self):
        return self._line_model

    @Property(QObject, notify=fileLoaded)
    def arcModel(self):
        return self._arc_model

    @Property(QObject, notify=fileLoaded)
    def circleModel(self):
        return self._circle_model

    @Property(float, notify=scaleChanged)
    def scale(self):
        if self._scale is None:
            # return nan if is None
            return float('nan')
        return self._scale

    @scale.setter
    def scale(self, value):
        # if value <= 0:
            # raise ValueError("Scale must be a positive number.")
            # return
        self._scale = value

    @Property(int, notify=floatPrecisionChanged)
    def floatPrecision(self):
        return self._float_precision

    @floatPrecision.setter
    def floatPrecision(self, value):
        # if value < 0:
        #     raise ValueError("Float precision must be a non-negative integer.")
        self._float_precision = value

    @Property(int, notify=linesVelocityChanged)
    def linesVelocity(self):
        return self._lines_velocity

    @linesVelocity.setter
    def linesVelocity(self, value):
        # if value <= 0:
            # raise ValueError("Lines velocity must be a positive integer.")
        self._lines_velocity = value

    @Property(int, notify=arcsVelocityChanged)
    def arcsVelocity(self):
        return self._arcs_velocity

    @arcsVelocity.setter
    def arcsVelocity(self, value):
        # if value <= 0:
            # raise ValueError("Arcs velocity must be a positive integer.")
        self._arcs_velocity = value

    @Property(int, notify=circlesVelocityChanged)
    def circlesVelocity(self):
        return self._circles_velocity

    @circlesVelocity.setter
    def circlesVelocity(self, value):
        # if value <= 0:
            # raise ValueError("Circles velocity must be a positive integer.")
        self._circles_velocity = value

    @Property(bool, notify=useDetectorChanged)
    def useDetector(self):
        return self._use_detector

    @useDetector.setter
    def useDetector(self, value):
        # if not isinstance(value, bool):
            # raise ValueError("useDetector must be a boolean value.")
        self._use_detector = value

    @Property(bool, notify=useOffsetChanged)
    def useOffset(self):
        return self._use_offset

    @useOffset.setter
    def useOffset(self, value):
        # if not isinstance(value, bool):
            # raise ValueError("useOffset must be a boolean value.")
        self._use_offset = value

    def is_running(self):
        """
        Check if the worker process is currently running.
        """
        return self._is_running

    def get_rapid_code(self):
        """
        Returns the generated RAPID code.
        """
        if not self._rapid_code or self._rapid_code == "":
            raise ValueError("No RAPID code generated yet. Please run the processing first.")
        return self._rapid_code

    def load_file(self, file_path):
        if not file_path:
            raise ValueError("File path cannot be empty.")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        self._selected_file_path = file_path

        parser = CADParser(filepath=self._selected_file_path, scale=self._scale)
        self._raw_lines = parser.get_lines()
        self._raw_arcs = parser.get_arcs()
        self._raw_circles = parser.get_circles()

        figures_parsed = parser.get_figures_parsed()

        self._lines = figures_parsed.get("lines", [])
        self._line_model.setLines(self._lines)
        self._arcs = figures_parsed.get("arcs", [])
        self._arc_model.setArcs(self._arcs)
        self._circles = figures_parsed.get("circles", [])
        self._circle_model.setCircles(self._circles)

        logging.info(f"Found {len(self._lines)} lines, {len(self._arcs)} arcs, and {len(self._circles)} circles in the file.")

        self.fileLoaded.emit()

    def save_file(self, file_path):
        if not file_path:
            raise ValueError("File path cannot be empty.")

        if not os.path.exists(os.path.dirname(file_path)):
            raise FileNotFoundError(f"The directory {os.path.dirname(file_path)} does not exist.")

        self._save_path = file_path

        if not file_path.endswith(".txt"):
            file_path += ".txt"

        with open(file_path, "w") as file:
            file.write(self._rapid_code)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error saving file at {file_path}. Please check the path and permissions.")

        print(f"File saved successfully at {file_path}")


    def start(self):
        try:
            if self._is_running:
                return

            # Before starting a new process ensure that the parameters are right
            if not self._validate_parameters():
                # raise ValueError("Invalid parameters. Please check scale, velocities, and other settings.")
                return


            self._is_running = True
            self.processingStarted.emit()

            self._process = multiprocessing.Process(
                target=processing_function,
                name="DxfProcessingWorker",
                args=("example.dxf", "arg1", "arg2"),
                kwargs={"key1": "value1", "key2": "value2"}
            )
            self._process.start()

            threading.Thread(target=self._monitor_process, daemon=True).start()
        except Exception as e:
            self._is_running = False
            self.processingError.emit(str(e))
            print(f"Error starting processing: {e}")

    def _validate_parameters(self):

        if self._scale is None or self._scale <= 0:
            print("Invalid scale value. It must be a positive number.")
            return False

        if self._float_precision is None or self._float_precision < 0:
            print("Invalid float precision value. It must be a non-negative integer.")
            return False

        if self._lines_velocity is None or self._lines_velocity <= 0:
            print("Invalid lines velocity value. It must be a positive integer.")
            return False

        if self._arcs_velocity is None or self._arcs_velocity <= 0:
            print("Invalid arcs velocity value. It must be a positive integer.")
            return False

        if self._circles_velocity is None or self._circles_velocity <= 0:
            print("Invalid circles velocity value. It must be a positive integer.")
            return False

        if not isinstance(self._use_detector, bool):
            print("Invalid useDetector value. It must be a boolean.")
            return False

        if not isinstance(self._use_offset, bool):
            print("Invalid useOffset value. It must be a boolean.")
            return False

        return True

    def _monitor_process(self):
        """
        Monitor the process and emit signals when it finishes.
        """
        self._process.join()
        self._is_running = False
        self.processingFinished.emit()

    def cancel(self):
        if self._process and self._process.is_alive():
            self._process.terminate()
            self._process.join()
            self._is_running = False
            self.processingFinished.emit()
            print("Processing cancelled.")

    # -- SLOTS -- #