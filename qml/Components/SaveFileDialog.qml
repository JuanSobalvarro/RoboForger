pragma Singleton
import QtQuick
import QtQuick.Dialogs

import ApplicationObjects

Item {
    id: root

    // File dialog for saving the txt rapid code file
    FileDialog {
        id: saveFileDialog
        title: "Save Rapid Code file"
        currentFolder: "~"
        nameFilters: ["Rapid Code files (*.txt)", "All files (*)"]
        fileMode: FileDialog.SaveFile
        onAccepted: {
            Orchestrator.rapidSaveFile(saveFileDialog.selectedFile);
        }
        onRejected: {
            Orchestrator.onFileDialogCancelled();
        }
    }

    // Public function to open the save dialog
    function openSaveDialog() {
        saveFileDialog.open();
    }
}