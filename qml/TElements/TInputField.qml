/*
    * TInputField.qml
    * A simple input field component for use in QML applications.
 */

import QtQuick
import QtQuick.Templates as T

import Themes

T.TextField {
    id: control

    implicitWidth: implicitBackgroundWidth + leftInset + rightInset
                   || Math.max(contentWidth, placeholder.implicitWidth) + leftPadding + rightPadding
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             contentHeight + topPadding + bottomPadding,
                             placeholder.implicitHeight + topPadding + bottomPadding)

    readonly property string __currentState: [
        !enabled && "disabled",
        activeFocus && "focused",
        enabled && !activeFocus && hovered && "hovered",
    ].filter(Boolean).join("_") || "normal"

    color: ThemeManager.getColor("input_background")
    selectionColor: ThemeManager.getColor("input_background_sel")
    selectedTextColor: control.palette.highlightedText
    placeholderTextColor: ThemeManager.getColor("input_placeholder")
    verticalAlignment: Text.AlignVCenter

    leftPadding: 10

    property alias borderColor: background.border.color
    property alias borderWidth: background.border.width
    property alias radius: background.radius


    TText {
        id: placeholder
        x: control.leftPadding
        y: control.topPadding
        width: control.width - (control.leftPadding + control.rightPadding)
        height: control.height - (control.topPadding + control.bottomPadding)

        text: control.placeholderText
        font: control.font
        color: control.placeholderTextColor
        verticalAlignment: control.verticalAlignment
        horizontalAlignment: control.horizontalAlignment
        visible: !control.length && !control.preeditText && (!control.activeFocus || control.horizontalAlignment !== Qt.AlignHCenter)
        elide: Text.ElideRight
        renderType: control.renderType
    }

    background: TRectangle {
        id: background
        anchors.fill: parent
        radius: 6

        border.color: {
            switch (control.__currentState) {
                case "focused": return ThemeManager.getColor("primary");
                case "hovered": return ThemeManager.getColor("selection_2");
                case "disabled": return ThemeManager.getColor("input_border_disabled");
                default: return ThemeManager.getColor("input_border");
            }
        }

        border.width: 2

        color: {
            switch (control.__currentState) {
                case "disabled": return ThemeManager.getColor("input_background_disabled");
                default: return ThemeManager.getColor("input_background");
            }
        }
    }
}
