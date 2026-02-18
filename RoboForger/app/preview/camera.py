from PySide6.QtCore import QPoint
from PySide6.QtGui import QVector3D, QQuaternion, Qt
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DInput import Qt3DInput


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
        if Qt.Key.Key_E in self.keys_pressed:
            move_vector += up_vector
        if Qt.Key.Key_Q in self.keys_pressed:
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
