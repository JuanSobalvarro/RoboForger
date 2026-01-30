from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QPlainTextEdit,
    QSizePolicy,
)
from PySide6.QtGui import QFont, QColor, QTextCursor
from PySide6.QtCore import QObject, Signal, Slot, Qt

import sys
import os
import threading
import logging


class ConsoleLogger(QObject):
    message_logged = Signal(str)

    def __init__(self):
        super().__init__()

        self._stdout = None
        self._stderr = None
        self._read = None
        self._write = None
        self._thread = None
        self._running = False

    def _handler(self):
        """Background thread loop to read from the pipe."""
        if self._read is None:
            return

        while self._running:
            try:
                line = self._read.readline()
                if not line:
                    break
                self.message_logged.emit(line.rstrip())
            except ValueError:
                break # Pipe closed

    def start(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr

        r, w = os.pipe()
        self._read = os.fdopen(r, 'r', encoding='utf-8')
        self._write = os.fdopen(w, 'w', 1, encoding='utf-8') # Line buffered

        sys.stdout = self._write
        sys.stderr = self._write

        logging.getLogger().handlers.clear()
        logging.basicConfig(
            stream=self._write, 
            level=logging.INFO, 
            format='[%(levelname)s] %(message)s'
        )

        self._running = True
        self._thread = threading.Thread(target=self._handler, daemon=True)
        self._thread.start()

        print("Console initialized...")

    def stop(self):
        self._running = False
        
        if self._stdout:
            sys.stdout = self._stdout
        if self._stderr:
            sys.stderr = self._stderr

        if self._write and not self._write.closed:
            self._write.close()
        if self._read and not self._read.closed:
            self._read.close()


class Console(QFrame):
    """
    Console widget to display log messages.
    """
    def __init__(self):
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Maximum
        )
        self.setMinimumHeight(120)
        # self.setMaximumHeight(260)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        background_frame = QFrame(self)
        background_frame.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e; 
                border: 1px solid #3e3e3e;
                border-radius: 4px;
            }
        """)
        inner_layout = QVBoxLayout(background_frame)
        inner_layout.setContentsMargins(4, 4, 4, 4)
        
        self.text_view = QPlainTextEdit()
        self.text_view.setReadOnly(True)
        self.text_view.setProperty("tag", "console")
        self.text_view.setMaximumBlockCount(1000) 
        
        inner_layout.addWidget(self.text_view)
        layout.addWidget(background_frame)
        self.setLayout(layout)

        self.logger = ConsoleLogger()
        self.logger.start()
        
        self.connect_signals()

    def connect_signals(self):
        self.logger.message_logged.connect(self.append_message)

    @Slot(str)
    def append_message(self, message: str):
        """
        Appends the text to the view and auto-scrolls.
        """
        
        # Colorize error messages roughly
        if "error" in message.lower() or "exception" in message.lower():
            message = f'<span style="color: #ff5555;">{message}</span>'
        elif "warning" in message.lower():
             message = f'<span style="color: #ffb86c;">{message}</span>'
        
        self.text_view.appendHtml(message)
        
        # Auto-scroll to bottom
        scrollbar = self.text_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def closeEvent(self, event):
        """Ensure we clean up the pipe hooks on exit"""
        self.logger.stop()
        super().closeEvent(event)