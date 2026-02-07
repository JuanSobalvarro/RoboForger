from PySide6.QtWidgets import QScrollArea, QFrame
from PySide6.QtCore import Qt

import os
import sys


def make_scrollable(widget, scroll_horizontally: bool = True, scroll_vertically: bool = True) -> QScrollArea:
    scroll = QScrollArea()
    scroll.setWidget(widget)
    scroll.setWidgetResizable(True)

    scroll.setFrameShape(QFrame.Shape.NoFrame)

    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded if scroll_horizontally else Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded if scroll_vertically else Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    
    return scroll
