// Components/TBusyIndicator.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes
import Themes
import Utils

Item {
    id: control

    property bool running: false
    property bool enabled: true
    property bool hovered: false

    implicitWidth: Scaler.loaderSize
    implicitHeight: Scaler.loaderSize

    Shape {
        id: arcShape
        anchors.centerIn: parent
        width: Scaler.loaderIconSize
        height: Scaler.loaderIconSize
        preferredRendererType: Shape.CurveRenderer

        opacity: control.running ? 1 : 0
        visible: control.running || opacity > 0

        Behavior on opacity { OpacityAnimator { duration: 250 } }

        rotation: 0
        transformOrigin: Item.Center

        ShapePath {
            id: animatedArc
            strokeColor: ThemeManager.getColor("primary")
            strokeWidth: Scaler.scale(4)
            fillColor: "transparent"
            capStyle: ShapePath.RoundCap

            property real currentStartAngle: 0
            property real currentSweepAngle: 0

            PathAngleArc {
                centerX: arcShape.width / 2
                centerY: arcShape.height / 2
                radiusX: (Math.min(arcShape.width, arcShape.height) / 2) - animatedArc.strokeWidth / 2
                radiusY: radiusX
                startAngle: animatedArc.currentStartAngle
                sweepAngle: animatedArc.currentSweepAngle
            }
        }

        SequentialAnimation {
            id: arcLengthAndPositionAnimation
            running: control.running
            loops: Animation.Infinite

            PropertyAnimation {
                target: animatedArc
                property: "currentSweepAngle"
                from: 20
                to: 300
                duration: 800
                easing.type: Easing.OutCubic
            }
            PropertyAnimation {
                target: animatedArc
                property: "currentStartAngle"
                from: 20
                to: 300
                duration: 800
                easing.type: Easing.OutCubic
            }

            PropertyAnimation {
                target: animatedArc
                property: "currentSweepAngle"
                from: 300
                to: 20
                duration: 1000
                easing.type: Easing.InCubic
            }
            PropertyAnimation {
                target: animatedArc
                property: "currentStartAngle"
                from: 300
                to: 360
                duration: 1000
                easing.type: Easing.InCubic
            }
        }

        RotationAnimation on rotation {
            id: globalRotationAnimation
            from: 0
            to: 360
            duration: 2000
            loops: Animation.Infinite
            running: control.running
            easing.type: Easing.Linear
        }
    }

    TText {
        id: forgingText
        text: "Forging" // Base text
        font.pixelSize: Scaler.font5
        color: ThemeManager.getColor("text")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: arcShape.bottom
        anchors.bottomMargin: Scaler.spacing2
        visible: control.running
    }

    // New: Timer for the "..." animation
    Timer {
        id: dotAnimationTimer
        interval: 300 // Time between each dot appearance (e.g., 300ms)
        repeat: true
        running: control.running && forgingText.visible // Only run if busy indicator is running and text is visible

        property int dotCount: 0

        onTriggered: {
            dotCount = (dotCount + 1) % 4; // Cycles 0, 1, 2, 3 (for "", ".", "..", "...")
            switch (dotCount) {
                case 0: forgingText.text = "Forging"; break;
                case 1: forgingText.text = "Forging."; break;
                case 2: forgingText.text = "Forging.."; break;
                case 3: forgingText.text = "Forging..."; break;
            }
        }
    }
}