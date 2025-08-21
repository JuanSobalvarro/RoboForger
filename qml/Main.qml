import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import Components.Header
import Themes
import Utils
import TElements
import Sections


ApplicationWindow {
    id: root
    width: 1280
    height: 800
    flags: Qt.FramelessWindowHint | Qt.Window
    visible: true

    background: TRectangle {
        anchors.fill: parent
        color: ThemeManager.getColor("background")
    }

    header: Header {
        id: headerBar
        appWindow: root
        height: 40
    }

    GridLayout {
        id: mainGrid
        anchors.fill: parent
        columns: 4
        rows: 4

        Description {
            id: descriptionSections
            Layout.columnSpan: 1
            Layout.rowSpan: 2
            Layout.column: 0
            Layout.row: 0
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.maximumWidth: 290
            Layout.minimumWidth: mainGrid.width / 4
        }

        Parameters {
            Layout.columnSpan: 1
            Layout.rowSpan: 2
            Layout.column: 0
            Layout.row: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.topMargin: Scaler.margin1
            Layout.bottomMargin: 30
            Layout.maximumHeight: mainGrid.height * 2 / 3 - 20
            Layout.maximumWidth: 290
        }

        // robo config
        Robo {
            Layout.columnSpan: 1
            Layout.rowSpan: 3
            Layout.column: 1
            Layout.row: 0
            Layout.fillHeight: true
            Layout.maximumWidth: mainGrid.width * 3 / 8
            Layout.minimumWidth: mainGrid.width * 2 / 6
            // 360 width
        }

        Process {
            Layout.column: 1
            Layout.row: 3
            Layout.columnSpan: 1
            Layout.rowSpan: 1
            Layout.maximumWidth: mainGrid.width * 3 / 8
            Layout.minimumWidth: mainGrid.width * 2 / 6
            Layout.preferredHeight: mainGrid.height / 3
        }

        Preview {
            id: preview
            Layout.column: 2
            Layout.row: 0
            Layout.columnSpan: 1
            Layout.rowSpan: 3
            Layout.preferredHeight: mainGrid.height * 2 / 3
            // Layout.preferredWidth: mainGrid.height * 2 / 3
            Layout.fillWidth: true
            // Layout.bottomMargin: Scaler.margin1
        }

        Feedback {
            Layout.columnSpan: 1
            Layout.rowSpan: 1
            Layout.column: 2
            Layout.row: 3
            Layout.preferredWidth: mainGrid.height * 2 / 3
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.bottomMargin: 30
            Layout.rightMargin: 5
        }
    }

    // ThemeSwitch {
    //     anchors.bottom: parent.bottom
    //     anchors.right: parent.right
    // }


    QtObject {
        id: _shared  // Properties and functions exposed to child items

        readonly property var visibility: root.visibility

        function startSystemMove() {
            root.startSystemMove()
        }

        function showMinimized() {
            root.showMinimized()
        }

        function showMaximized() {
            root.showMaximized()
        }

        function showNormal() {
            root.showNormal()
        }

        function close() {
            root.close()
        }
    }
}