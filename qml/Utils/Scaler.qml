pragma Singleton
import QtQuick 2.15

QtObject {
    // You can set this from outside once window is known
    property real baseUnit: 1

    // Font sizes
    readonly property real fontMainTitle: 30 * baseUnit
    readonly property real fontSubTitle: 20 * baseUnit
    readonly property real fontLabel: 16 * baseUnit
    readonly property real fontInput: 14 * baseUnit
    readonly property real fontButton: 16 * baseUnit
    readonly property real fontCheckbox: 18 * baseUnit

    // Component sizes
    readonly property real inputHeight: 40 * baseUnit
    readonly property real toggleButtonSize: 30 * baseUnit

    // Spacing & padding
    readonly property real sectionPadding: 25 * baseUnit
    readonly property real gridSpacing: 15 * baseUnit
}
