import QtQuick
import QtQuick.Controls

Rectangle {
    color: "transparent"
    border.color: "transparent"
    radius: 0

    property int animation_duration: 200

    Behavior on color {
        ColorAnimation {
            duration: animation_duration
        }
    }
    Behavior on border.color {
        ColorAnimation {
            duration: animation_duration
        }
    }
}