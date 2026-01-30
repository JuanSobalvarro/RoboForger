from PySide6.QtWidgets import (
    QLabel, 
    QWidget,
)
from PySide6.QtGui import (
    QColor,
    QFont,
)

from enum import Enum


# enum for headers, normal text, etc.
class LabelTag(Enum):
    HEADER = 0
    SUBHEADER = 1
    NORMAL = 2
    SMALL = 3


class LabelAnchor(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class Label(QLabel):
    def __init__(self, text: str, parent: QWidget | None = None, color: QColor = QColor("#FFFFFF"), tag: LabelTag = LabelTag.NORMAL, stylesheet: str = ""):
        """
        Constructor for the custom Label class.
        
        :param self: Description
        :param text: Text to display
        :type text: str
        :param parent: Parent widget, can be None
        :type parent: QWidget | None
        :param color: Text color
        :type color: QColor
        :param tag: Label tag for styling (header, normal, etc.)
        :type tag: LabelTag
        :param stylesheet: Override stylesheet
        :type stylesheet: str
        """
        super().__init__(text, parent)

        self.color: QColor = color
        self.tag: LabelTag = tag
        self.custom_stylesheet: str = stylesheet

        self.setProperty("tag", tag.name.lower())
