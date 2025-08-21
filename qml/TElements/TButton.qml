// TComponents/TButton.qml
import QtQuick
import QtQuick.Layouts
import Themes
import Utils
import Components

Item {
    id: root

    // text
    property string text: ""
    property color textColor: ThemeManager.getColor("text")
    property real fontSize: Scaler.font4
    property alias labelWordWrap: label.wrapMode
    property var labelHorizontalAlignment: Text.AlignHCenter
    property var labelVerticalAlignment: Text.AlignVCenter

    // icon
    property url iconSource: ""
    property color iconColor: ThemeManager.getColor("text") // Default icon color from theme
    property real iconWidth: 0
    property real iconHeight: 0
    property alias iconMipmap: rawSvg.mipmap // Alias for mipmap property of the icon
    property alias iconSmooth: rawSvg.smooth // Alias for smooth property of the icon
    property real iconMargins: 0

    // appearance
    property color backgroundColor: ThemeManager.getColor("primary") // Alias this property
    property color hoverColor: ThemeManager.getColor("selection_1") // New: for hover effect
    property color pressedColor: ThemeManager.getColor("selection_2") // New: for pressed effect
    property color disabledColor: ThemeManager.getColor("background2") // New: for disabled background
    property color disabledTextColor: ThemeManager.getColor("text_disabled") // New: for disabled text color
    property color disabledIconColor: ThemeManager.getColor("text_disabled") // New: for disabled icon color
    property real cornerRadius: Scaler.radius3 // Use Scaler for radius
    property real borderWidth: Scaler.buttonBorderWidth
    property bool animated: true
    property real visualScale: 1.0

    // NEW: Disabled property
    property bool disabled: false

    signal clicked()

    readonly property bool isHovered: controlMouseArea.containsMouse && !root.disabled
    readonly property bool isPressed: controlMouseArea.pressed && !root.disabled

    scale: visualScale
    transformOrigin: Item.Center // Center the scaling transformation

    implicitWidth: contentLayout.implicitWidth + Scaler.buttonPadding * 2
    implicitHeight: Scaler.buttonHeight

    TRectangle {
        id: backgroundRect
        anchors.fill: parent
        radius: root.cornerRadius

        color: root.disabled ? root.disabledColor : (root.isPressed ? root.pressedColor : (root.isHovered ? root.hoverColor : root.backgroundColor))
        border.width: root.borderWidth
        border.color: ThemeManager.getColor("input_border") // Keep a consistent border color or make it configurable/themed
        Behavior on color { ColorAnimation { duration: 100 } }
    }

    RowLayout {
        id: contentLayout
        anchors.fill: parent
        spacing: 0

        MonoColorSVG {
            id: rawSvg
            source: root.iconSource
            color: root.disabled ? root.disabledIconColor : root.iconColor // Apply disabled color
            visible: root.iconSource !== ""
            Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
            Layout.preferredWidth: root.iconWidth
            Layout.preferredHeight: root.iconHeight
            Layout.leftMargin: root.text !== "" ? Scaler.margin2 : 0
            mipmap: root.iconMipmap
            smooth: root.iconSmooth
        }

        TText {
            id: label
            visible: root.text !== ""
            text: root.text
            font.pixelSize: root.fontSize
            color: root.disabled ? root.disabledTextColor : root.textColor // Apply disabled color
            Layout.fillWidth: true
            Layout.rightMargin: Scaler.margin1
            horizontalAlignment: root.labelHorizontalAlignment
            verticalAlignment: root.labelVerticalAlignment
        }
    }

    MouseArea {
        id: controlMouseArea
        anchors.fill: parent
        // Disable MouseArea interactivity when root.disabled is true
        enabled: !root.disabled

        // Change cursor based on disabled state
        cursorShape: root.disabled ? Qt.ArrowCursor : Qt.PointingHandCursor

        onClicked: {
            // Only animate and emit signal if not disabled
            if (!root.disabled) {
                if (root.animated) {
                    scaleAnimation.stop();
                    root.visualScale = 1.0;
                    scaleAnimation.start();
                }
                root.clicked()
            }
        }
    }

    SequentialAnimation {
        id: scaleAnimation
        NumberAnimation {
            target: root
            property: "visualScale"
            from: 1.0
            to: 0.95
            duration: 100
            easing.type: Easing.OutCubic
        }
        NumberAnimation {
            target: root
            property: "visualScale"
            from: 0.95
            to: 1.0
            duration: 100
            easing.type: Easing.OutCubic
        }
    }
}