pragma Singleton
import QtQuick 2.15

QtObject {
    // You can set this from outside once window is known
    property real baseUnit: 1.0

    function scale(value) {
        return value * baseUnit
    }

    // Font sizes
    readonly property real font1: scale(28) // Main title
    readonly property real font2: scale(24) // Sub title
    readonly property real font3: scale(20) // Section title
    readonly property real font4: scale(18) // Normal texts
    readonly property real font5: scale(16) // Small texts
    readonly property real font6: scale(14) // Smaller texts
    readonly property real font7: scale(12) // Tiny texts
    readonly property real font8: scale(10) // Extra small texts
    readonly property real font9: scale(8)  // Micro texts

    // Grid Spacing
    readonly property real spacing1: scale(16) // Main spacing
    readonly property real spacing2: scale(12) // Section spacing
    readonly property real spacing3: scale(8)  // Small spacing
    readonly property real spacing4: scale(4)  // Tiny spacing
    readonly property real spacing5: scale(2)  // Extra small spacing

    // Margins
    readonly property real margin1: scale(16) // Main margin
    readonly property real margin2: scale(12) // Section margin
    readonly property real margin3: scale(8)  // Small margin
    readonly property real margin4: scale(4)  // Tiny margin
    readonly property real margin5: scale(2)  // Extra small margin

    // Radius
    readonly property real radius1: scale(16) // Main radius
    readonly property real radius2: scale(12) // Section radius
    readonly property real radius3: scale(8)  // Small radius
    readonly property real radius4: scale(4)  // Tiny radius
    readonly property real radius5: scale(2)  // Extra small radius

    // Input
    readonly property real minInputWidth: scale(100) // Minimum width for inputs
    readonly property real minInputHeight: scale(10) // Minimum height for inputs

    // Checkbox size
    readonly property real checkboxIndicatorSize1: scale(24)
    readonly property real checkboxIndicatorSize2: scale(20)
    readonly property real checkboxIndicatorSize3: scale(16)

    // Button sizes
    readonly property real iconSize1: scale(48)
    readonly property real iconSize2: scale(36)
    readonly property real iconSize3: scale(24)
    readonly property real iconSize4: scale(20) // Standard icon size
    readonly property real iconSize5: scale(16)
    readonly property real iconSize6: scale(12) // Small icon size
    readonly property real iconSize7: scale(8)  // Extra small icon size
    readonly property real buttonHeight: scale(40) // Standard button height
    readonly property real buttonBorderWidth: scale(1) // Standard button width

    // Loader Size
    readonly property real loaderSize: scale(48) // Standard loader size
    readonly property real loaderIconSize: scale(36) // Standard loader icon size

    // Header height
    readonly property real headerHeight: scale(16) // Standard header height
}
