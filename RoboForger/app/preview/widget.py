from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DRender import Qt3DRender
from PySide6.Qt3DInput import Qt3DInput
from PySide6.Qt3DLogic import Qt3DLogic
from PySide6.Qt3DExtras import Qt3DExtras


class Widget3D(QWidget):
    """
    Qt3D host widget that:
    - does NOT create a camera
    - does NOT create a root entity
    - allows Qt widgets to overlay cleanly
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # ---- Qt3D Window (offscreen-friendly) ----
        self._view = Qt3DExtras.Qt3DWindow()
        self._view.defaultFrameGraph().setClearColor(QColor(20, 20, 20))

        # Container allows stacking Qt widgets on top
        self._container = QWidget.createWindowContainer(self._view, self)
        self._container.setFocusPolicy(Qt.StrongFocus)
        self._container.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._container)

        # ---- Qt3D engine parts (NO defaults created) ----
        self._root_entity: Qt3DCore.QEntity | None = None
        self._camera: Qt3DRender.QCamera | None = None

        # ---- Input + logic ----
        self._input = Qt3DInput.QInputSettings()
        self._input.setEventSource(self._view)

        self._frame_action = Qt3DLogic.QFrameAction()
        self._frame_action.triggered.connect(self.update)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_root_entity(self, root: Qt3DCore.QEntity):
        """
        REQUIRED: Set the root entity before showing the widget.
        """
        if root is None:
            raise ValueError("Root entity cannot be None")

        self._root_entity = root
        self._root_entity.addComponent(self._input)
        self._root_entity.addComponent(self._frame_action)

        self._view.setRootEntity(self._root_entity)

    def set_camera(self, camera: Qt3DRender.QCamera):
        """
        REQUIRED: Provide a camera explicitly.
        """
        if camera is None:
            raise ValueError("Camera cannot be None")

        self._camera = camera
        self._view.setCamera(self._camera)

    def camera(self) -> Qt3DRender.QCamera:
        return self._camera

    def root_entity(self) -> Qt3DCore.QEntity:
        return self._root_entity
