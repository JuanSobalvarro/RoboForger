import QtQuick
import Components

Item {
    id: feedbackItem
    property int maxLines: 200

    Rectangle {
        id: consoleBackground
        anchors.fill: parent
        color: "black"
        border.color: "white"
        border.width: 1

        Scrollable {
            anchors.fill: parent
            anchors.margins: 1
            clip: true
            vScrollbar.backgroundColor: "#121212"
            vScrollbar.handleColor: "#CCC"
            vScrollbar.visibleOpacity: 0.7
            vScrollbar.autoHide: true
            vScrollbar.breadth: 20

            Column {
                id: logColumn
                width: parent.width
                spacing: 4

                Repeater {
                    id: logRepeater
                    model: logModel

                    Text {
                        text: model.text
                        color: "lime"
                        font.family: "monospace"
                        wrapMode: Text.Wrap
                        font.pixelSize: 14
                        width: logColumn.width - 20
                    }
                }
            }
        }
    }

    ListModel {
        id: logModel
    }

    Connections {
        target: appViewModel.consoleLogger
        function onMessageReceived(message) {
            const formatted = "> " + message
            logModel.append({ text: formatted })

            // Trim excess entries
            while (logModel.count > maxLines) {
                logModel.remove(0)
            }
        }
    }
}
