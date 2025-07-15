import QtQuick
import QtQuick.Controls


Text {
    color: "transparent"

    Behavior on color {
        ColorAnimation {
            duration: 200
        }
    }
}