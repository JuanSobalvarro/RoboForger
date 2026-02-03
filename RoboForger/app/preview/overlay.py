from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class PreviewOverlay(QWidget):
    """
    Transparent HUD overlay displayed on top of the 3D preview.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Let mouse events pass through unless explicitly handled
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setStyleSheet("background: transparent;")

        self._build_ui()

    def _build_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)

        hud_style = """
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 160);
                padding: 6px;
                border-radius: 4px;
                font-family: Consolas;
                font-size: 12px;
            }
            QPushButton {
                background-color: rgba(40, 40, 40, 200);
                color: white;
                border: 1px solid #666;
                padding: 6px 10px;
                border-radius: 4px;
                font-family: Consolas;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgba(70, 70, 70, 220);
            }
        """
        self.setStyleSheet(hud_style)

        # ─── Top-Left: Reset Camera ────────────────────────────────
        self.btn_reset_camera = QPushButton("Reset View")
        self.btn_reset_camera.setCursor(Qt.CursorShape.PointingHandCursor)

        layout.addWidget(
            self.btn_reset_camera,
            0, 0,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        # ─── Top-Right: Camera Coordinates ─────────────────────────
        self.lbl_camera_pos = QLabel("X: 0.0  Y: 0.0  Z: 0.0")
        layout.addWidget(
            self.lbl_camera_pos,
            0, 2,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )

        # ─── Bottom-Left: Stats ───────────────────────────────────
        self.lbl_stats = QLabel(
            "Polylines: 0\n"
            "Arcs:      0\n"
            "Circles:   0\n"
            "Splines:   0"
        )
        layout.addWidget(
            self.lbl_stats,
            2, 0,
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        )

        # ─── Bottom-Right: Disclaimer ─────────────────────────────
        self.lbl_disclaimer = QLabel(
            "VISUALIZATION ONLY\n"
            "Not for precise measurement"
        )
        self.lbl_disclaimer.setStyleSheet("""
            QLabel {
                color: #ff5555;
                background-color: rgba(0, 0, 0, 180);
                font-weight: bold;
            }
        """)
        self.lbl_disclaimer.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom
        )

        layout.addWidget(
            self.lbl_disclaimer,
            2, 2,
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight
        )

        # Stretch so corners stay pinned
        layout.setColumnStretch(1, 1)
        layout.setRowStretch(1, 1)

    # ───────────────────── Public API ─────────────────────

    def set_camera_position(self, x: float, y: float, z: float):
        self.lbl_camera_pos.setText(
            f"X: {x:.1f}  Y: {y:.1f}  Z: {z:.1f}"
        )

    def set_stats(self, polylines: int, arcs: int, circles: int, splines: int = 0):
        self.lbl_stats.setText(
            f"Polylines: {polylines}\n"
            f"Arcs:      {arcs}\n"
            f"Circles:   {circles}\n"
            f"Splines:   {splines}"
        )
