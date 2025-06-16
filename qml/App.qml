import QtQuick
import QtQuick.Controls
import Themes

ApplicationWindow {
    id: appWindow
    width: 1080
    height: 720
    visible: true
    title: "RoboForger by JuSo"

    // Main content of the application
    Rectangle {
        anchors.fill: parent
        color: ThemeManager.getColor("background")

        Text {
            text: "Hello, nichan!!!"
            anchors.centerIn: parent
            font.pointSize: 20
            color: ThemeManager.getColor("text")
        }
        ThemeSwitch {
            anchors {
                top: parent.bottom
                right: parent.right
                margins: 10
            }
        }
    }
}