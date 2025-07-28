import QtQuick
import QtQuick.Layouts

import Themes
import TElements
import Utils
import Components

Item {
    id: processItem

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
                iconWidth: Scaler.iconSize2
                iconHeight: Scaler.iconSize2
                iconColor: ThemeManager.getColor("text")
                borderWidth: 0
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height / 4
                Layout.margins: Scaler.margin2
                Layout.row: 1
                Layout.column: 0
                onClicked: {
                    if (appViewModel) {
                        appViewModel.selectDxfFile();
                    }
                }
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
                    if (appViewModel) {
                        appViewModel.saveRapidCode();
                    }
                }
                disabled: appViewModel.isProcessing || appViewModel.dxfFilePath === ""
            }

            Item {
                Layout.fillHeight: true
                Layout.fillWidth: true // Important to allow content to fill
                Layout.margins: Scaler.margin2
                Layout.row: 2
                Layout.column: 0
                Layout.columnSpan: 2
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                // "Process" button (visible when NOT processing)
                TButton {
                    anchors.fill: parent // Fill this parent Item
                    text: "Process"
                    fontSize: Scaler.font4
                    labelHorizontalAlignment: Text.AlignHCenter
                    iconSource: "qrc:/assets/icons/draw.svg"
                    iconWidth: Scaler.iconSize2
                    iconHeight: Scaler.iconSize2
                    iconColor: ThemeManager.getColor("text")
                    borderWidth: 0
                    onClicked: {
                        if (appViewModel) {
                            appViewModel.startProcessing();
                        }
                    }
                    visible: !appViewModel.isProcessing
                    disabled: appViewModel.isProcessing || appViewModel.dxfFilePath === ""
                }

                // RowLayout to hold both TLoader and Cancel button when processing
                ColumnLayout {
                    anchors.fill: parent // Fill the container Item
                    spacing: Scaler.spacing1 // Space between loader and button
                    visible: appViewModel.isProcessing // Show only when processing
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter // Center contents within the row

                    // Loader (now directly inside the RowLayout)
                    TLoader {
                        running: appViewModel.isProcessing // Still controlled by ViewModel
                        Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter // Center vertically within the RowLayout
                        Layout.preferredWidth: Scaler.loaderSize * 0.7 // Make it a bit smaller to fit
                        Layout.preferredHeight: Scaler.loaderSize * 0.7
                    }

                    // "Cancel" button (now directly inside the RowLayout)
                    TButton {
                        iconSource: "qrc:/assets/icons/cancel.svg"
                        iconWidth: Scaler.iconSize6
                        iconHeight: Scaler.iconSize6
                        iconColor: ThemeManager.getColor("error")
                        backgroundColor: "transparent"
                        borderWidth: 0
                        Layout.topMargin: Scaler.margin2
                        Layout.preferredHeight: Scaler.iconSize6 + Scaler.spacing3  // Adjust height for better visibility
                        Layout.preferredWidth: Scaler.iconSize6 + Scaler.spacing3 // Adjust to allocate space
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVBottom
                        onClicked: {
                            if (appViewModel) {
                                appViewModel.cancelProcessing();
                            }
                        }
                        disabled: !appViewModel.isProcessing
                    }
                }
            }
        }
    }
}