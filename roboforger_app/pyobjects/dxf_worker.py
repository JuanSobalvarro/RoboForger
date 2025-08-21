# dxf_worker.py
from math import isnan
import os
import multiprocessing
import threading
from pathlib import Path
import logging

from PySide6.QtCore import QObject, Signal, Property, Slot

# Domain classes (your existing modules)
from RoboForger import Forger  # adjust import path if your Forger lives elsewhere
from .models.line_model import LineModel
from .models.arc_model import ArcModel
from .models.circle_model import CircleModel
from .models.bspline_model import BSplineModel


# ---------------------------
# Background process function
# ---------------------------
def _processing_function(file_path: str, result_queue: multiprocessing.Queue, params: dict):
    """
    Run the full pipeline inside a separate process using Forger and return the RAPID code.
    Any exception is put back into the queue to be handled in the UI thread.
    """
    try:
        forger = Forger(
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


class DxfWorker(QObject):
    """
    QML-facing worker that orchestrates background processing and exposes properties/signals.
    All CAD/geometry/rapid logic is handled by Forger.
    """

    # --- Lifecycle / processing signals ---
    processingStarted = Signal()
    processingFinished = Signal()
    processingError = Signal(str)

    fileLoaded = Signal()
    fileSaved = Signal()

    # --- Figures changed signals (for models) ---
    linesChanged = Signal()
    arcsChanged = Signal()
    circlesChanged = Signal()
    splinesChanged = Signal()

    # --- Parameter change signals for QML bindings (keep names compatible) ---
    scaleChanged = Signal(float)
    floatPrecisionChanged = Signal(int)
    linesVelocityChanged = Signal(int)
    arcsVelocityChanged = Signal(int)
    circlesVelocityChanged = Signal(int)
    liftingChanged = Signal(float)
    useDetectorChanged = Signal(bool)
    useOffsetChanged = Signal(bool)

    toolNameChanged = Signal(str)

    inferiorLimitXChanged = Signal(float)
    inferiorLimitYChanged = Signal(float)
    inferiorLimitZChanged = Signal(float)

    superiorLimitXChanged = Signal(float)
    superiorLimitYChanged = Signal(float)
    superiorLimitZChanged = Signal(float)

    originXChanged = Signal(float)
    originYChanged = Signal(float)
    originZChanged = Signal(float)

    zeroXChanged = Signal(float)
    zeroYChanged = Signal(float)
    zeroZChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        # process/thread orchestration
        self._process: multiprocessing.Process | None = None
        self._result_queue: multiprocessing.Queue | None = None
        self._is_running: bool = False

        # file paths
        self._selected_file_path: str = ""
        self._save_path: str = ""

        # Models for QML preview
        self._line_model = LineModel()
        self._arc_model = ArcModel()
        self._circle_model = CircleModel()
        self._bspline_model = BSplineModel()

        # Parameters (defaults consistent with your Forger.reset_default + your previous worker)
        self._scale: float = 1.0
        self._float_precision: int = 4
        self._lines_velocity: int = 1000
        self._arcs_velocity: int = 1000
        self._circles_velocity: int = 1000
        self._splines_velocity: int = 1000
        self._lifting: float = 50.0
        self._use_detector: bool = True
        self._use_offset: bool = True

        self._tool_name: str = "tool0"

        self._inferior_limit: tuple[float, float, float] = (-810.0, -810.0, -100.0)
        self._superior_limit: tuple[float, float, float] = (810.0, 810.0, 800.0)
        self._origin: tuple[float, float, float] = (450.0, 0.0, 450.0)
        self._zero: tuple[float, float, float] = (0.0, 0.0, 0.0)

        # Figures (preview copies)
        self._polylines = []
        self._arcs = []
        self._circles = []
        self._splines = []

        self._rapid_code: str | None = None

        # A local Forger for preview / synchronous steps (kept separate from the process Forger)
        self._forger_preview: Forger | None = None

    # ---------- Expose QML models ----------
    @Property(QObject, notify=fileLoaded)
    def lineModel(self):
        return self._line_model

    @Property(QObject, notify=fileLoaded)
    def arcModel(self):
        return self._arc_model

    @Property(QObject, notify=fileLoaded)
    def circleModel(self):
        return self._circle_model

    @Property(QObject, notify=fileLoaded)
    def bsplineModel(self):
        return self._bspline_model

    # ---------- Simple state exposures ----------
    @Property(bool, constant=True)
    def isRunning(self):
        return self._is_running

    @Property(str, constant=True)
    def rapidCode(self):
        return self._rapid_code or ""

    # ---------- Parameter Properties (QML-friendly) ----------
    @Property(float, notify=scaleChanged)
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = float(value)
        self.scaleChanged.emit(self._scale)

    @Property(int, notify=floatPrecisionChanged)
    def floatPrecision(self):
        return self._float_precision

    @floatPrecision.setter
    def floatPrecision(self, value: int):
        self._float_precision = int(value)
        self.floatPrecisionChanged.emit(self._float_precision)

    @Property(int, notify=linesVelocityChanged)
    def linesVelocity(self):
        return self._lines_velocity

    @linesVelocity.setter
    def linesVelocity(self, value: int):
        self._lines_velocity = int(value)
        self.linesVelocityChanged.emit(self._lines_velocity)

    @Property(int, notify=arcsVelocityChanged)
    def arcsVelocity(self):
        return self._arcs_velocity

    @arcsVelocity.setter
    def arcsVelocity(self, value: int):
        self._arcs_velocity = int(value)
        self.arcsVelocityChanged.emit(self._arcs_velocity)

    @Property(int, notify=circlesVelocityChanged)
    def circlesVelocity(self):
        return self._circles_velocity

    @circlesVelocity.setter
    def circlesVelocity(self, value: int):
        self._circles_velocity = int(value)
        self.circlesVelocityChanged.emit(self._circles_velocity)

    @Property(float, notify=liftingChanged)
    def lifting(self):
        return self._lifting

    @lifting.setter
    def lifting(self, value: float):
        self._lifting = float(value)
        self.liftingChanged.emit(self._lifting)

    @Property(bool, notify=useDetectorChanged)
    def useDetector(self):
        return self._use_detector

    @useDetector.setter
    def useDetector(self, value: bool):
        self._use_detector = bool(value)
        self.useDetectorChanged.emit(self._use_detector)

    @Property(bool, notify=useOffsetChanged)
    def useOffset(self):
        return self._use_offset

    @useOffset.setter
    def useOffset(self, value: bool):
        self._use_offset = bool(value)
        self.useOffsetChanged.emit(self._use_offset)

    @Property(str, notify=toolNameChanged)
    def toolName(self):
        return self._tool_name

    @toolName.setter
    def toolName(self, value: str):
        if not value:
            print("Tool name cannot be empty.")
        self._tool_name = str(value)
        self.toolNameChanged.emit(self._tool_name)

    # --- Limits, origin, zero split into components for QML bindings ---

    @Property(float, notify=inferiorLimitXChanged)
    def inferiorLimitX(self):
        return self._inferior_limit[0]

    @inferiorLimitX.setter
    def inferiorLimitX(self, value: float):
        self._inferior_limit = (float(value), self._inferior_limit[1], self._inferior_limit[2])
        self.inferiorLimitXChanged.emit(self._inferior_limit[0])

    @Property(float, notify=inferiorLimitYChanged)
    def inferiorLimitY(self):
        return self._inferior_limit[1]

    @inferiorLimitY.setter
    def inferiorLimitY(self, value: float):
        self._inferior_limit = (self._inferior_limit[0], float(value), self._inferior_limit[2])
        self.inferiorLimitYChanged.emit(self._inferior_limit[1])

    @Property(float, notify=inferiorLimitZChanged)
    def inferiorLimitZ(self):
        return self._inferior_limit[2]

    @inferiorLimitZ.setter
    def inferiorLimitZ(self, value: float):
        self._inferior_limit = (self._inferior_limit[0], self._inferior_limit[1], float(value))
        self.inferiorLimitZChanged.emit(self._inferior_limit[2])

    @Property(float, notify=superiorLimitXChanged)
    def superiorLimitX(self):
        return self._superior_limit[0]

    @superiorLimitX.setter
    def superiorLimitX(self, value: float):
        self._superior_limit = (float(value), self._superior_limit[1], self._superior_limit[2])
        self.superiorLimitXChanged.emit(self._superior_limit[0])

    @Property(float, notify=superiorLimitYChanged)
    def superiorLimitY(self):
        return self._superior_limit[1]

    @superiorLimitY.setter
    def superiorLimitY(self, value: float):
        self._superior_limit = (self._superior_limit[0], float(value), self._superior_limit[2])
        self.superiorLimitYChanged.emit(self._superior_limit[1])

    @Property(float, notify=superiorLimitZChanged)
    def superiorLimitZ(self):
        return self._superior_limit[2]

    @superiorLimitZ.setter
    def superiorLimitZ(self, value: float):
        self._superior_limit = (self._superior_limit[0], self._superior_limit[1], float(value))
        self.superiorLimitZChanged.emit(self._superior_limit[2])

    @Property(float, notify=originXChanged)
    def originX(self):
        return self._origin[0]

    @originX.setter
    def originX(self, value: float):
        x = float(value)
        if x < self._inferior_limit[0] or x > self._superior_limit[0]:
            print("Origin X out of limits.")
        self._origin = (x, self._origin[1], self._origin[2])
        self.originXChanged.emit(x)

    @Property(float, notify=originYChanged)
    def originY(self):
        return self._origin[1]

    @originY.setter
    def originY(self, value: float):
        y = float(value)
        if y < self._inferior_limit[1] or y > self._superior_limit[1]:
            print("Origin Y out of limits.")
        self._origin = (self._origin[0], y, self._origin[2])
        self.originYChanged.emit(y)

    @Property(float, notify=originZChanged)
    def originZ(self):
        return self._origin[2]

    @originZ.setter
    def originZ(self, value: float):
        z = float(value)
        if z < self._inferior_limit[2] or z > self._superior_limit[2]:
            print("Origin Z out of limits.")
            return
        self._origin = (self._origin[0], self._origin[1], z)
        self.originZChanged.emit(z)

    @Property(float, notify=zeroXChanged)
    def zeroX(self):
        return self._zero[0]

    @zeroX.setter
    def zeroX(self, value: float):
        x = float(value)
        if x < self._inferior_limit[0] or x > self._superior_limit[0]:
            print("Zero X out of limits.")
            return
        self._zero = (x, self._zero[1], self._zero[2])
        self.zeroXChanged.emit(x)

    @Property(float, notify=zeroYChanged)
    def zeroY(self):
        return self._zero[1]

    @zeroY.setter
    def zeroY(self, value: float):
        y = float(value)
        if y < self._inferior_limit[1] or y > self._superior_limit[1]:
            print("Zero Y out of limits.")
            return
        self._zero = (self._zero[0], y, self._zero[2])
        self.zeroYChanged.emit(y)

    @Property(float, notify=zeroZChanged)
    def zeroZ(self):
        return self._zero[2]

    @zeroZ.setter
    def zeroZ(self, value: float):
        z = float(value)
        if z < self._inferior_limit[2] or z > self._superior_limit[2]:
            print("Zero Z out of limits.")
            return
        self._zero = (self._zero[0], self._zero[1], z)
        self.zeroZChanged.emit(z)

    # -----------------------------
    # Public API callable from QML
    # -----------------------------
    @Slot(str)
    def load_file(self, file_path: str):
        """
        Parses and converts figures synchronously (fast) to update preview models.
        """
        try:
            if not file_path:
                print("File path cannot be empty.")
                return
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")

            self._selected_file_path = file_path

            if not self._validate_parameters():
                print("Cannot load file")
                return

            # Create/refresh preview Forger with current params
            self._forger_preview = Forger(
                origin=self._origin,
                zero=self._zero,
                pre_scale=self._scale,
                float_precision=self._float_precision,
                lifting=self._lifting,
                tool_name=self._tool_name,
                global_velocity=self._lines_velocity,
                polyline_velocity=self._lines_velocity,
                arc_velocity=self._arcs_velocity,
                circle_velocity=self._circles_velocity,
                spline_velocity=self._splines_velocity,
                workspace_limits=(self._inferior_limit, self._superior_limit),
                use_intelligent_traces=self._use_detector,
                use_offset_programming=self._use_offset,
            )

            # Parse and convert for preview
            self._forger_preview.parse_figures(file_path)
            self._forger_preview.convert_figures()

            figures = self._forger_preview.get_figures()
            self._polylines = figures.get("polylines", [])
            self._arcs = figures.get("arcs", [])
            self._circles = figures.get("circles", [])
            # self._splines = figures.get("splines", [])

            # Push to models
            self._line_model.setLines(self._polylines)
            self._arc_model.setArcs(self._arcs)
            self._circle_model.setCircles(self._circles)
            self._bspline_model.setLines(self._splines)

            logging.info(
                f"Preview loaded: {len(self._polylines)} polylines, "
                f"{len(self._arcs)} arcs, {len(self._circles)} circles, {len(self._splines)} splines."
            )

            # Notify QML
            self.linesChanged.emit()
            self.arcsChanged.emit()
            self.circlesChanged.emit()
            self.splinesChanged.emit()
            self.fileLoaded.emit()

        except Exception as e:
            self.processingError.emit(str(e))

    @Slot()
    def start(self):
        """
        Start full RAPID code generation in a process using the current parameters.
        """
        try:
            if self._is_running:
                print("Processing is already running.")
                return
            if not self._selected_file_path:
                # print("No file selected. Please load a DXF file before starting processing.")
                print("No file selected. Please load a DXF file before starting processing.")
                return
            if not self._validate_parameters():
                print("Invalid parameters. Please check your settings.")
                return

            self._is_running = True
            self.processingStarted.emit()

            self._result_queue = multiprocessing.Queue()
            params = self._parameters_as_kwargs()

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
            self.processingError.emit(str(e))

    def _monitor_process(self):
        try:
            result = self._result_queue.get()
            if isinstance(result, Exception):
                self._rapid_code = None
                self.processingError.emit(str(result))
            else:
                self._rapid_code = result.get("rapid_code", "")
                self.processingFinished.emit()
        except Exception as e:
            self._rapid_code = None
            self.processingError.emit(str(e))
        finally:
            try:
                if self._process:
                    self._process.join()
            finally:
                self._is_running = False

    @Slot()
    def cancel(self):
        """
        Terminate the background process if running.
        """
        if self._process and self._process.is_alive():
            self._process.terminate()
            self._process.join()
            self._is_running = False
            self.processingFinished.emit()

    @Slot(str)
    def save_file(self, file_path: str):
        """
        Save generated RAPID code to a text file.
        """
        try:
            if not self._rapid_code:
                print("No RAPID code generated yet. Please run processing first.")
            if not file_path:
                print("File path cannot be empty.")
            target = Path(file_path)
            if target.parent and not target.parent.exists():
                raise FileNotFoundError(f"The directory {target.parent} does not exist.")

            with open(target, "w", encoding="utf-8") as f:
                f.write(self._rapid_code)

            self.fileSaved.emit()
        except Exception as e:
            self.processingError.emit(str(e))

    # -----------------------------
    # Helpers
    # -----------------------------
    def _validate_parameters(self) -> bool:
        ok = True

        def bad(msg):
            nonlocal ok
            print(msg)
            ok = False

        if self._scale is None or self._scale <= 0:
            bad("Invalid scale value. It must be a positive number.")

        if self._float_precision is None or self._float_precision < 0:
            bad("Invalid float precision value. It must be a non-negative integer.")

        for name, v in [("lines velocity", self._lines_velocity),
                        ("arcs velocity", self._arcs_velocity),
                        ("circles velocity", self._circles_velocity),
                        ("splines velocity", self._splines_velocity)]:
            if v is None or v <= 0:
                bad(f"Invalid {name}. It must be a positive integer.")

        if not isinstance(self._use_detector, bool):
            bad("Invalid useDetector value. It must be a boolean.")

        if not isinstance(self._use_offset, bool):
            bad("Invalid useOffset value. It must be a boolean.")

        if not all(isinstance(x, float) for x in self._inferior_limit):
            bad("Invalid inferior limit. It must be a tuple of three floats.")

        if not all(isinstance(x, float) for x in self._superior_limit):
            bad("Invalid superior limit. It must be a tuple of three floats.")

        if not all(isinstance(x, float) for x in self._origin):
            bad("Invalid origin. It must be a tuple of three floats.")

        if not all(isinstance(x, float) for x in self._zero):
            bad("Invalid zero. It must be a tuple of three floats.")

        # Check for nan
        if any(isinstance(x, float) and isnan(x) for x in self._inferior_limit):
            bad("Invalid inferior limit. It must be a tuple of three floats.")

        if any(isinstance(x, float) and isnan(x) for x in self._superior_limit):
            bad("Invalid superior limit. It must be a tuple of three floats.")

        if any(isinstance(x, float) and isnan(x) for x in self._origin):
            bad("Invalid origin. It must be a tuple of three floats.")

        if any(isinstance(x, float) and isnan(x) for x in self._zero):
            bad("Invalid zero. It must be a tuple of three floats.")

        return ok

    def _parameters_as_kwargs(self) -> dict:
        return {
            "scale": self._scale,
            "float_precision": self._float_precision,
            "lines_velocity": self._lines_velocity,
            "arcs_velocity": self._arcs_velocity,
            "circles_velocity": self._circles_velocity,
            "splines_velocity": self._splines_velocity,
            "use_detector": self._use_detector,
            "use_offset": self._use_offset,
            "inferior_limit": self._inferior_limit,
            "superior_limit": self._superior_limit,
            "origin": self._origin,
            "zero": self._zero,
            "lifting": self._lifting,
            "tool_name": self._tool_name,
        }
