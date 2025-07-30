import QtQuick
import QtQuick.Controls

Item {
    id: feedbackItem

    Rectangle {
        anchors.fill: parent
        color: "black"
        border.color: "white"
        border.width: 1

        ScrollView {
            anchors.fill: parent
            clip: true

            TextArea {
                id: consoleOutput
                readOnly: true
                wrapMode: TextEdit.Wrap
                color: "lime"
                font.family: "monospace"
                // Make sure lines wrap to viewport width
                width: ScrollView.view.width
                background: Rectangle {
                    color: "black"
                }
            }
        }
    }

    Connections {
        target: appViewModel.consoleLogger
        function onMessageReceived(message) {
            consoleOutput.append(message + "\n")
            // auto-scroll to bottom
            consoleOutput.cursorPosition = consoleOutput.length
        }
    }
}
