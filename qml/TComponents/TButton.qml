import QtQuick
import QtQuick.Controls


Button {
    icon.color: "transparent"

    property color bg_color: "white"
    property color border_color: "white"
    property string button_text: "Button"
    property color text_color: "black"
    property int radius: 4


    background: TRectangle {
        anchors.fill: parent
        color: bg_color
        border.color: border_color
        border.width: 1
        radius: parent.radius

        TText {
            text: button_text
            color: text_color
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pixelSize: 16
        }
    }

}