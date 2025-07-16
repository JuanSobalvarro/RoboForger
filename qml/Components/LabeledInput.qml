import QtQuick
import QtQuick.Layouts
import Themes
import Utils
import TElements

Item {
    property string label: ""
    property string placeholder: ""
    property alias text: input.text
    property alias inputField: input

    property int spacing: Scaler.spacing3

    implicitHeight: rootLayout.implicitHeight
    implicitWidth: rootLayout.implicitWidth

    RowLayout {
        id: rootLayout
        anchors.fill: parent
        spacing: spacing

        TText {
            // Layout.fillWidth: true
            text: label
            font.pixelSize: Scaler.font6
            color: ThemeManager.getColor("text")
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
        }

        TInputField {
            id: input
            // Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: Scaler.scale(30)
            Layout.minimumWidth: Scaler.minInputWidth
            Layout.alignment: Qt.AlignRight
            placeholderText: placeholder
            font.pixelSize: Scaler.font8
            color: ThemeManager.getColor("text")
        }
    }
}
