import sys
import os
import threading
import logging
from PySide6.QtCore import QObject, Signal


class ConsoleLogger(QObject):
    messageReceived = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._stdout = None
        self._stderr = None
        self._r = None
        self._w = None
        self._thread = None

    def _handler(self):
        """Read from the pipe and emit every line."""
        while True:
            line = self._r.readline()
            if not line:  # Pipe closed
                break
            self.messageReceived.emit(line.rstrip())

    def start(self):
        # Save current stdout/stderr
        self._stdout = sys.stdout
        self._stderr = sys.stderr

        # Create pipe for redirection
        r, w = os.pipe()
        self._r, self._w = os.fdopen(r, 'r'), os.fdopen(w, 'w', 1)

        # Redirect stdout and stderr
        sys.stdout = self._w
        sys.stderr = self._w

        # Reconfigure logging to go to redirected stderr
        logging.getLogger().handlers.clear()
        logging.basicConfig(
            level=logging.INFO,
            stream=sys.stderr,
            format="%(levelname)s: %(message)s"
        )

        # Start thread that reads pipe
        self._thread = threading.Thread(target=self._handler, daemon=True)
        self._thread.start()

        print("ConsoleLogger started.")

    def stop(self):
        # Restore stdout/stderr
        sys.stdout = self._stdout
        sys.stderr = self._stderr

        if self._w:
            self._w.close()
        if self._thread:
            self._thread.join()
        if self._r:
            self._r.close()

        print("ConsoleLogger stopped.")
