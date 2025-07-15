import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
// import QtQuick.Controls.Material
import QtQuick.Controls.FluentWinUI3
import Themes
import Utils
import TElements

Item {
    property string label: ""
    property string placeholder: ""
    property alias text: input.text
    property alias inputField: input

    implicitHeight: Scaler.inputHeight + Scaler.gridSpacing

    RowLayout {
        anchors.fill: parent
        spacing: Scaler.gridSpacing

        TText {
            Layout.fillWidth: true
            text: label
            font.pixelSize: Scaler.fontLabel
            color: ThemeManager.getColor("text")
            verticalAlignment: Text.AlignVCenter
        }

        TInputField {
            id: input
            Layout.preferredWidth: parent.width * 0.7
            Layout.preferredHeight: Scaler.inputHeight
            placeholderText: placeholder
            font.pixelSize: Scaler.fontInput
            color: ThemeManager.getColor("text")
        }
    }
}
