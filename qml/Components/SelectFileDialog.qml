pragma Singleton
import QtQuick
import QtQuick.Dialogs

import ApplicationObjects


Item {
    id: root

    // File dialog for opening DXF files
    FileDialog {
        id: selectFileDialog
        title: "Select a DXF file"
        currentFolder: "~"
        nameFilters: ["DXF files (*.dxf)", "All files (*)"]
        onAccepted: {
            Orchestrator.dxfSelectFile(selectFileDialog.selectedFile);
        }
        onRejected: {
            Orchestrator.onFileDialogCancelled();
        }
    }

    // Public function to open the file dialog
    function openSelectFileDialog() {
        selectFileDialog.open();
    }
}