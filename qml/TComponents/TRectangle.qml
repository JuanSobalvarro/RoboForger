import QtQuick
import QtQuick.Controls

Rectangle {
    color: "transparent"
    border.color: "transparent"
    radius: 4

    Behavior on color {
        ColorAnimation {
            duration: 200
        }
    }
}