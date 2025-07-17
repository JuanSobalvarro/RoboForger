import QtQuick
import QtQuick.Layouts

import Themes
import TElements
import Utils
import Components

Item {
    id: processItem

    // No need for dxfFilePath property here anymore.
    // The ViewModel holds it and makes it available via appViewModel.dxfFilePath

    TRectangle {
        anchors.fill: parent
        color: "transparent"

        GridLayout {
            id: processGrid
            anchors.fill: parent
            columns: 2
            rows: 3

            TText {
                text: "Process DXF"
                font.pixelSize: Scaler.font3
                color: ThemeManager.getColor("text")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                Layout.fillWidth: true
                Layout.preferredHeight: Scaler.font3 * 2
                Layout.row: 0
                Layout.column: 0
                Layout.columnSpan: 2
                wrapMode: Text.WordWrap
            }

            TButton {
                text: "Load DXF"
                fontSize: Scaler.font4
                labelHorizontalAlignment: Text.AlignHCenter
                iconSource: "qrc:/assets/icons/dxf-file.svg"
                iconWidth: Scaler.iconSize2 // Use Scaler, not this.height - 2*margins
                iconHeight: Scaler.iconSize2 // Use Scaler
                iconColor: ThemeManager.getColor("text")
                borderWidth: 0
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height / 4
                Layout.margins: Scaler.margin2
                Layout.row: 1
                Layout.column: 0
                onClicked: {
                    // Call the new slot for selecting the file
                    if (appViewModel) { // No need to check isProcessing here, ViewModel handles it
                        appViewModel.selectDxfFile();
                    }
                }
                // Button is disabled if processing is active
                disabled: appViewModel.isProcessing
            }

            TButton {
                text: "Save Rapid"
                fontSize: Scaler.font4
                labelHorizontalAlignment: Text.AlignHCenter
                iconSource: "qrc:/assets/icons/arm.svg"
                iconWidth: Scaler.iconSize2
                iconHeight: Scaler.iconSize2
                iconColor: ThemeManager.getColor("text")
                borderWidth: 0
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height / 4
                Layout.margins: Scaler.margin2
                Layout.row: 1
                Layout.column: 1
                onClicked: {
                    if (appViewModel) { // No need to check isProcessing here, ViewModel handles it
                        appViewModel.saveRapidCode();
                    }
                }
                // Disabled if processing or if no DXF loaded (assuming saveRapidCode relies on dxfFilePath existence)
                disabled: appViewModel.isProcessing || appViewModel.dxfFilePath === ""
            }

            TButton {
                text: "Process"
                fontSize: Scaler.font4
                labelHorizontalAlignment: Text.AlignHCenter
                iconSource: "qrc:/assets/icons/draw.svg"
                iconWidth: Scaler.iconSize2
                iconHeight: Scaler.iconSize2
                iconColor: ThemeManager.getColor("text")
                borderWidth: 0
                Layout.preferredWidth: processGrid.width / 2
                Layout.preferredHeight: parent.height / 4
                Layout.margins: Scaler.margin2
                Layout.row: 2
                Layout.column: 0
                Layout.columnSpan: 2
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                onClicked: {
                    // Call the new slot to process the *already selected* file
                    if (appViewModel) { // No need to check isProcessing here, ViewModel handles it
                        appViewModel.processSelectedDxfFile();
                    }
                }
                // Visible only when NOT processing
                visible: !appViewModel.isProcessing
                // Disabled if processing or if no DXF file has been selected yet
                disabled: appViewModel.isProcessing || appViewModel.dxfFilePath === ""
            }
            Item {
                Layout.fillHeight: true
                Layout.preferredWidth: processGrid.width / 2
                Layout.margins: Scaler.margin2
                Layout.row: 2
                Layout.column: 0
                Layout.columnSpan: 2
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                TLoader { // Your custom busy indicator
                    anchors.centerIn: parent
                    running: appViewModel.isProcessing
                }

                visible: appViewModel.isProcessing
            }
        }
    }
}