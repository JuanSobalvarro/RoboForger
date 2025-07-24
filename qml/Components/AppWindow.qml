import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Components
import Themes
import Utils
import TElements
import Sections


ApplicationWindow {
    id: appWindow
    width: 1080
    height: 720
    visible: true
    minimumWidth: 1080
    minimumHeight: 720
    maximumWidth: 1080
    maximumHeight: 720
    // flags: Qt.Window | Qt.FramelessWindowHint
    title: "RoboForger"
    color: "#01000000"
    opacity: 1

    property int taskbarHeight: 40 // Height of the taskbar, adjust as needed

    default property alias content: contentContainer.data

    // Save original values
    property real originalY: appWindow.y
    property real originalScale: 1

    // Container for the whole content - animatable item
    Item {
        id: contentContainer
        anchors.fill: parent
        scale: 1

        // ...
    }

    ParallelAnimation {
        id: minimizeAnim
        // PropertyAnimation { target: contentContainer; property: "opacity"; from: 1; to: 0.0; duration: 1000 }
        PropertyAnimation { target: contentContainer; property: "scale"; to: 0.0; duration: 2000; easing.type: Easing.InOutQuad }
        PropertyAnimation { target: appWindow; property: "y"; to: appWindow.screen.height - taskbarHeight; duration: 2000; easing.type: Easing.InOutQuad }
        onStopped: {
            appWindow.showMinimized()
            contentContainer.opacity = 1
            contentContainer.scale = originalScale
            appWindow.y = originalY
        }
    }

    ParallelAnimation {
        id: closeAnim
        PropertyAnimation { target: contentContainer; property: "opacity"; from: 1; to: 0.0; duration: 180 }
        PropertyAnimation { target: contentContainer; property: "scale"; to: 0.0; duration: 180; easing.type: Easing.InOutQuad }
        // PropertyAnimation { target: appWindow; property: "y"; to: appWindow.height - taskbarHeight; duration: 180; easing.type: Easing.InOutQuad }
        onStopped: {
            appWindow.close()
            contentContainer.opacity = 1
            contentContainer.scale = originalScale
            appWindow.y = originalY
        }
    }

    // Fade-in animation on content
    SequentialAnimation {
        id: fadeInAnim
        PropertyAnimation { target: appWindow; property: "opacity"; from: 0; to: 1; duration: 200 }
    }

    Component.onCompleted: {
        originalY = appWindow.y
        originalScale = contentContainer.scale
        Scaler.baseUnit = 1;
        fadeInAnim.start()
    }

    onWidthChanged: {
        // Set scaler base unit
        Scaler.baseUnit = appWindow.width / 1080;
    }

    function minimizeAni() {
        minimizeAnim.start()
    }

    function closeAni() {
        // Close animation logic can be added here
        closeAnim.start();
    }
}