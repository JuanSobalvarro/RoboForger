import os
import logging

from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtWidgets import QFileDialog

# path as string
DEFAULT_DIR = os.path.expanduser("~")

print(f"Default directory for file dialogs: {DEFAULT_DIR}")


class FileDialogManager(QObject):

    fileSelected = Signal(str)
    fileSaved = Signal(str)
    fileDialogCancelled = Signal()
    dialogError = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._file_path = ""

        logging.info("FileDialogManager initialized")

    def get_current_file_path(self):
        """
        Returns the currently selected file path.
        :return: The file path as a string.
        """
        return self._file_path

    @Slot(str, str, str, str, result=bool)
    def showOpenFileNameDialog(self, title="Open File", filter="All Files (*.*)", default_dir=DEFAULT_DIR, selected_filter=""):
        """
        Opens a file dialog to select a file.
        :param title: Title of the dialog.
        :param filter: Filter for the file types.
        :param default_dir: Default directory to open the dialog in.
        :param selected_filter: Initially selected filter.
        :return: True if a file was selected, False otherwise.
        """
        try:
            logging.info("Opening file dialog")
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(None,
                                                       caption=title,
                                                       dir=f"{default_dir}",
                                                       filter=filter,
                                                       selectedFilter=selected_filter)
            if file_path:
                self._file_path = file_path
                logging.info(f"File selected: {file_path}")
                self.fileSelected.emit(file_path)
                return True
            else:
                logging.info("File dialog cancelled")
                self.fileDialogCancelled.emit()
                return False
        except Exception as e:
            logging.error(f"Error opening file dialog: {e}")
            self.dialogError.emit(str(e))
            return False

    @Slot(str, str, str, str, result=bool)
    def showSaveFileNameDialog(self, title="Save File", filter="All Files (*.*)", default_dir=DEFAULT_DIR, selected_filter=""):
        """
        Opens a file dialog to save a file.
        :param title: Title of the dialog.
        :param filter: Filter for the file types.
        :param default_dir: Default directory to open the dialog in.
        :param selected_filter: Initially selected filter.
        :return: True if a file was selected, False otherwise.
        """
        try:
            logging.info("Opening save file dialog")
            file_path, _ = QFileDialog.getSaveFileName(None,
                                                       caption=title,
                                                       dir=f"{default_dir}",
                                                       filter=filter,
                                                       selectedFilter=selected_filter)
            if file_path:
                self._file_path = file_path
                logging.info(f"File saved as: {file_path}")
                self.fileSaved.emit(file_path)
                return True
            else:
                logging.info("Save file dialog cancelled")
                self.fileDialogCancelled.emit()
                return False
        except Exception as e:
            logging.error(f"Error opening save file dialog: {e}")
            self.dialogError.emit(str(e))
            return False