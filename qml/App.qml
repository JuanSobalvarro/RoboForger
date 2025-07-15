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

    TRectangle {
        anchors.fill: parent
        radius: 0
        color: ThemeManager.getColor("background")
        // color: "red"

        GridLayout {
            id: grid
            anchors.fill: parent
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            columns: 3
            rows: 3


            Description {
                Layout.columnSpan: 1
                Layout.rowSpan: 1
                Layout.column: 0
                Layout.row: 0
                Layout.fillWidth: true
                Layout.fillHeight: true
                width: parent.width / 4
            }

            Parameters {
                Layout.columnSpan: 1
                Layout.rowSpan: 2
                Layout.column: 0
                Layout.row: 1
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.bottomMargin: 20
            }

            Process {
                height: parent.height / 2
                width: parent.width / 3
                Layout.column: 1
                Layout.row: 0
                Layout.columnSpan: 2
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
                width: parent.width / 3
                height: parent.height / 2
            }

            Feedback {
                Layout.columnSpan: 1
                Layout.rowSpan: 1
                Layout.column: 2
                Layout.row: 1
                Layout.fillWidth: true
                Layout.fillHeight: true
                width: parent.width / 3
                height: parent.height / 2
            }
        }

        ThemeSwitch {
            anchors.bottom: parent.bottom
            anchors.right: parent.right
        }
    }
}
