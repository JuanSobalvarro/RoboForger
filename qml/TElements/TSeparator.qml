// TElements/TSeparator.qml
import QtQuick

Item {
    id: separator

    // Enum workaround: use int and define constants manually
    property int orientation: Qt.Horizontal // Use 0 = Horizontal, 1 = Vertical
    property real thickness: 1
    property color color: "#666666"

    width: orientation === Qt.Vertical ? thickness : parent ? parent.width : 100
    height: orientation === Qt.Horizontal ? thickness : parent ? parent.height : 100

    Rectangle {
        anchors.fill: parent
        color: separator.color
    }

    Behavior on color {
        ColorAnimation {
            duration: 200
        }
    }
}
