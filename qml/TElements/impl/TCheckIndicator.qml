import QtQuick

import Themes
import Components

Rectangle {
    id: indicatorItem
    implicitWidth: 24
    implicitHeight: 24
    color: "transparent"
    // if not checked it will show the first and third color border, if checked it will show second color
    border.color: !control.enabled ? ThemeManager.getColor("text")
        : checkState !== Qt.Unchecked ? ThemeManager.getColor("checkbox_fill") : ThemeManager.getColor("checkbox_border")
    border.width: checkState !== Qt.Unchecked ? width / 2 : 2
    radius: 2

    property Item control
    property int checkState: control.checkState
    property int animation_duration: 100

    Behavior on border.width {
        NumberAnimation {
            duration: animation_duration
            easing.type: Easing.OutCubic
        }
    }

    Behavior on border.color {
        ColorAnimation {
            duration: animation_duration
            easing.type: Easing.OutCubic
        }
    }

    // TODO: This needs to be transparent
    MonoColorSVG {
        anchors.fill: parent
        anchors.margins: 2
        color: ThemeManager.getColor("text")
        source: "qrc:/assets/icons/check.svg"
        scale: indicatorItem.checkState === Qt.Checked ? 1 : 0
        Behavior on scale { NumberAnimation { duration: animation_duration } }
    }

    // idk what this is for, but it was in the original code
    // Rectangle {
    //     x: (parent.width - width) / 2
    //     y: (parent.height - height) / 2
    //     width: 12
    //     height: 3
    //
    //     scale: indicatorItem.checkState === Qt.PartiallyChecked ? 1 : 0
    //     Behavior on scale { NumberAnimation { duration: animation_duration } }
    // }

    states: [
        State {
            name: "checked"
            when: indicatorItem.checkState === Qt.Checked
        },
        State {
            name: "partiallychecked"
            when: indicatorItem.checkState === Qt.PartiallyChecked
        }
    ]

    transitions: Transition {
        SequentialAnimation {
            NumberAnimation {
                target: indicatorItem
                property: "scale"
                // Go down 2 pixels in size.
                to: 1 - 2 / indicatorItem.width
                duration: 120
            }
            NumberAnimation {
                target: indicatorItem
                property: "scale"
                to: 1
                duration: 120
            }
        }
    }
}
