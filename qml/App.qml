import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Themes
import Utils
import TElements
import Sections

ApplicationWindow {
    id: appWindow
    width: 1080
    height: 720
    visible: true
    title: "RoboForger by JuSo"
    minimumWidth: 1080
    minimumHeight: 720
    // maximumWidth: 1080
    // maximumHeight: 720

    TRectangle {
        anchors.fill: parent
        radius: 0
        color: ThemeManager.getColor("background")
        // color: "red"

        GridLayout {
            id: mainGrid
            anchors.fill: parent
            columns: 3
            rows: 3

            Description {
                Layout.columnSpan: 1
                Layout.rowSpan: 1
                Layout.column: 0
                Layout.row: 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.maximumWidth: mainGrid.width / 4
            }

            Parameters {
                Layout.columnSpan: 1
                Layout.rowSpan: 2
                Layout.column: 0
                Layout.row: 1
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.topMargin: Scaler.margin1
                Layout.bottomMargin: Scaler.margin1
                Layout.maximumHeight: mainGrid.height * 2 / 3 - 20
                Layout.maximumWidth: mainGrid.width / 4
            }

            // robo config
            Robo {
                Layout.columnSpan: 1
                Layout.rowSpan: 1
                Layout.column: 1
                Layout.row: 0
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Process {
                Layout.column: 2
                Layout.row: 0
                Layout.columnSpan: 1
                Layout.rowSpan: 1
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Preview {
                id: preview
                Layout.column: 1
                Layout.row: 1
                Layout.columnSpan: 1
                Layout.rowSpan: 2
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Feedback {
                Layout.columnSpan: 1
                Layout.rowSpan: 1
                Layout.column: 2
                Layout.row: 1
                Layout.fillWidth: true
                Layout.fillHeight: true
            }
        }

        ThemeSwitch {
            anchors.bottom: parent.bottom
            anchors.right: parent.right
        }
    }

    onWidthChanged: {
        // Set scaler base unit
        Scaler.baseUnit = appWindow.width / 1080;
    }

    Component.onCompleted: {
        Scaler.baseUnit = 1;
    }
}
