from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DInput import Qt3DInput
from PySide6.Qt3DLogic import Qt3DLogic
from PySide6.QtCore import (
    Qt,
    Signal,
    Slot,
    QEvent,
    QObject,
    QPoint,
)
from PySide6.QtGui import (
    QKeyEvent,
    QQuaternion,
    QVector3D,
    QColor,
)

from RoboForger.app.models.line import Line, Polyline
from RoboForger.app.models.arc import Arc
from RoboForger.app.models.circle import Circle

from typing import Any


class WASDCameraController(Qt3DExtras.QAbstractCameraController):
    """
    A custom camera controller that inherits from QAbstractCameraController.
    It uses a native QKeyboardHandler to bypass Widget focus issues.
    """
    def __init__(self, base_speed: float, camera: Qt3DRender.QCamera, 
                 keyboard_device: Qt3DInput.QKeyboardDevice, 
                 mouse_device: Qt3DInput.QMouseDevice,
                 parent=None):
        super().__init__(parent)
        
        self.setCamera(camera)
        self.setLinearSpeed(base_speed)
        self.setLookSpeed(180.0)
        
        self.turbo_multiplier = 4.0
        self.zoom_sensitivity = 2.0
        self.look_sensitivity = 0.2

        self.turbo_active = False

        self.yaw = 0.0
        self.pitch = 0.0

        self.keys_pressed = set()

        # mouse state
        self.left_mouse_pressed = False
        self.last_mouse_pos = QPoint(0, 0)

        # We manually handle the keyboard to implement WASD logic
        self.keyboard_handler = Qt3DInput.QKeyboardHandler(self)
        self.keyboard_handler.setSourceDevice(keyboard_device)
        self.keyboard_handler.setFocus(True)

        # remember always using lambdas to connect to avoid PySide signal issues (C++ related signature mismatches)
        self.keyboard_handler.pressed.connect(lambda e: self.on_key_pressed(e))
        self.keyboard_handler.released.connect(lambda e: self.on_key_released(e))
        self.addComponent(self.keyboard_handler)

        self.mouse_handler = Qt3DInput.QMouseHandler(self)
        self.mouse_handler.setSourceDevice(mouse_device)

        # connect mouse events
        self.mouse_handler.positionChanged.connect(lambda e: self.on_mouse_move(e))
        self.mouse_handler.pressed.connect(lambda e: self.on_mouse_pressed(e))
        self.mouse_handler.released.connect(lambda e: self.on_mouse_released(e))
        self.mouse_handler.wheel.connect(lambda e: self.on_mouse_wheel(e))
        self.addComponent(self.mouse_handler)
        

    def on_key_pressed(self, event: Qt3DInput.QKeyEvent):
        self.keys_pressed.add(event.key())

    def on_key_released(self, event: Qt3DInput.QKeyEvent):
        if event.key() == Qt.Key.Key_Shift:
            self.turbo_active = False
        self.keys_pressed.discard(event.key())

    def on_mouse_pressed(self, event: Qt3DInput.QMouseEvent):
        if event.button() == Qt3DInput.QMouseEvent.Buttons.LeftButton:
            self.left_mouse_pressed = True
            self.last_mouse_pos = self.get_mouse_event_pos(event)
    
    def on_mouse_released(self, event: Qt3DInput.QMouseEvent):
        if event.button() == Qt3DInput.QMouseEvent.Buttons.LeftButton:
            self.left_mouse_pressed = False

    def on_mouse_wheel(self, event: Qt3DInput.QWheelEvent):
        delta = event.angleDelta().y() / 120  # Most mouse wheels give 120 units per notch
        zoom_amount = delta * self.zoom_sensitivity

        view_vector = self.camera().viewVector()
        displacement = view_vector * zoom_amount

        if self.turbo_active:
            displacement *= self.turbo_multiplier

        new_position = self.camera().position() + displacement
        new_view_center = self.camera().viewCenter() + displacement

        self.camera().setPosition(new_position)
        self.camera().setViewCenter(new_view_center)

    def on_mouse_move(self, event: Qt3DInput.QMouseEvent):
        if not self.left_mouse_pressed:
            return

        current_pos = self.get_mouse_event_pos(event)
        delta = current_pos - self.last_mouse_pos
        self.last_mouse_pos = current_pos

        self.yaw   -= delta.x() * self.look_sensitivity
        self.pitch -= delta.y() * self.look_sensitivity

        self.pitch = max(-89.0, min(89.0, self.pitch))
        # self.pitch = self.pitch % 360.0

        yaw_q   = QQuaternion.fromAxisAndAngle(QVector3D(0, 1, 0), self.yaw)
        pitch_q = QQuaternion.fromAxisAndAngle(QVector3D(1, 0, 0), self.pitch)

        orientation = yaw_q * pitch_q
        forward = orientation.rotatedVector(QVector3D(0, 0, -1))

        pos = self.camera().position()
        self.camera().setViewCenter(pos + forward)


    def get_mouse_event_pos(self, event: Qt3DInput.QMouseEvent) -> QPoint:
        return QPoint(event.x(), event.y())

    def moveCamera(self, state: Qt3DExtras.QAbstractCameraController.InputState, delta_time: float):

        # if self.keys_pressed:
        #     print(f"DEBUG: Keys currently pressed: {[key for key in self.keys_pressed]}")

        move_vector = QVector3D()

        view_vector = self.camera().viewVector()
        up_vector = self.camera().upVector()
        # right vector is cross product of view and up
        right_vector = QVector3D.crossProduct(view_vector, up_vector)

        # key related movement

        if Qt.Key.Key_W in self.keys_pressed:
            move_vector += view_vector
        if Qt.Key.Key_S in self.keys_pressed:
            move_vector -= view_vector
        if Qt.Key.Key_A in self.keys_pressed:
            move_vector -= right_vector
        if Qt.Key.Key_D in self.keys_pressed:
            move_vector += right_vector
        if Qt.Key.Key_Q in self.keys_pressed:
            move_vector += up_vector
        if Qt.Key.Key_E in self.keys_pressed:
            move_vector -= up_vector
        if Qt.Key.Key_Shift in self.keys_pressed:
            self.turbo_active = True

        if not move_vector.isNull():
            move_vector.normalize()
            if self.turbo_active:
                move_vector *= self.turbo_multiplier
            displacement = move_vector * self.linearSpeed() * delta_time
            new_position = self.camera().position() + displacement
            new_view_center = self.camera().viewCenter() + displacement

            self.camera().setPosition(new_position)
            self.camera().setViewCenter(new_view_center)


class Preview(QWidget):
    def __init__(self, grid_size: int = 200, grid_step: int = 10, parent=None):
        """
        A 3D preview widget using Qt3D.

        Coordinate system:
        - X, Y plane = ground
        - Z = up (robotics convention)
        """
        super().__init__(parent)

        self.grid_size = grid_size
        self.grid_step = grid_step

        self.view = Qt3DExtras.Qt3DWindow()
        self.view.defaultFrameGraph().setClearColor(QColor("#101010"))

        self.container = self.createWindowContainer(self.view)
        # self.container.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # self.container.setSizePolicy(
        #     QSizePolicy.Policy.Expanding,
        #     QSizePolicy.Policy.Expanding
        # )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.container)

        self.setLayout(layout)

        self.setMinimumSize(200, 200)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # === Scene Root ===
        self.root_entity = Qt3DCore.QEntity()
        self.view.setRootEntity(self.root_entity)

        # === Camera ===
        self.camera = self.view.camera()
        self.camera.lens().setPerspectiveProjection(
            45.0,
            16.0 / 9.0,   # updated dynamically later
            0.1,
            5000.0
        )

        self.camera.setPosition(QVector3D(0, 0, 200))
        self.camera.setViewCenter(QVector3D(0, 0, 0))

        # === Input ===
        self.input_settings = Qt3DInput.QInputSettings(self.root_entity)
        self.input_settings.setEventSource(self.view)
        self.root_entity.addComponent(self.input_settings)

        self.keyboard_device = Qt3DInput.QKeyboardDevice(self.root_entity)
        self.mouse_device = Qt3DInput.QMouseDevice(self.root_entity)

        self.wasd_controller = WASDCameraController(
            150.0,
            self.camera,
            self.keyboard_device,
            self.mouse_device,
            self.root_entity
        )

        self.grid_entities: list[Qt3DCore.QEntity] = []
        self.lines = []
        self.arcs = []
        self.circles = []

        self.add_axis_and_grid()

    def clear_figures(self):
        for line in self.lines:
            line.setParent(None)
        self.lines.clear()

        for arc in self.arcs:
            arc.setParent(None)
        self.arcs.clear()

        for circle in self.circles:
            circle.setParent(None)
        self.circles.clear()

    @Slot(dict)
    def load_figures(self, figures: dict[str, list[dict[str, Any]]]):
        """
        This is highly coupled with the Forger data structures.

        Forger provides "RAW FIGURES" which is a dict of lists of raw entities.
        Take a look at forger.py for more details.
        """
        print("Loading figures into preview...")
        # clear previous entities
        self.clear_figures()

        raw_lines: list[dict] = figures.get("lines", [])
        raw_arcs: list[dict] = figures.get("arcs", [])
        raw_circles: list[dict] = figures.get("circles", [])

        for line in raw_lines:
            self.lines.append(
                Line(
                    QVector3D(*line["start"]),
                    QVector3D(*line["end"]),
                    QColor("#ffff00"),
                    0.2,
                    self.root_entity,
                )
            )

        print(f"Loaded {len(self.lines)} lines.")

        for arc in raw_arcs:
            center = arc["center"]
            radius = arc["radius"]
            start_angle = arc["start_angle"]
            end_angle = arc["end_angle"]
            clockwise = arc["clockwise"]
            self.arcs.append(
                Arc(QVector3D(*center), float(radius), float(start_angle), float(end_angle), bool(clockwise), QColor("#0000ff"), 0.2, self.root_entity)
            )

        print(f"Loaded {len(self.arcs)} arcs.")

        for circle in raw_circles:
            center = circle["center"]
            radius = circle["radius"]
            self.circles.append(
                Circle(QVector3D(*center), float(radius), QColor("#00ff00"), 0.2, self.root_entity)
            )

        print(f"Loaded {len(self.circles)} circles.")

    def add_axis_and_grid(self):
        self._create_grid()

        # x axis
        x_start = QVector3D(-self.grid_size, 0, 0)
        x_end = QVector3D(self.grid_size, 0, 0)
        x_axis = Line(x_start, x_end, QColor("#ff0000"), 0.1, self.root_entity)
        self.grid_entities.append(x_axis)
        # y axis
        y_start = QVector3D(0, -self.grid_size, 0)
        y_end = QVector3D(0, self.grid_size, 0)
        y_axis = Line(y_start, y_end, QColor("#00ff00"), 0.1, self.root_entity)
        self.grid_entities.append(y_axis)
        # z axis
        z_start = QVector3D(0, 0, -self.grid_size)
        z_end = QVector3D(0, 0, self.grid_size)
        z_axis = Line(z_start, z_end, QColor("#0000ff"), 0.1, self.root_entity)
        self.grid_entities.append(z_axis)

    def _create_grid(self):
        grid_color = QColor("#ffffff")
        thickness = 0.05
        
        for i in range(-self.grid_size, self.grid_size + 1, self.grid_step):
            # horizontal line
            start_h = QVector3D(-self.grid_size, i, 0)
            end_h = QVector3D(self.grid_size, i, 0)

            line_h = Line(start_h, end_h, grid_color, thickness, self.root_entity)
            
            self.grid_entities.append(line_h)

            # vertical line
            start_v = QVector3D(i, -self.grid_size, 0)
            end_v = QVector3D(i, self.grid_size, 0)
            
            line_v = Line(start_v, end_v, grid_color, thickness, self.root_entity)
            
            self.grid_entities.append(line_v)
