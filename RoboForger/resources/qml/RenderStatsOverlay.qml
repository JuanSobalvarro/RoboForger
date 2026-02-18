import QtQuick
import QtQuick3D

Rectangle {
    id: root
    
    required property View3D view3d

    radius: 8
    color: "#CCFFFFFF"        // translucent white
    border.color: "#40FFFFFF"
    border.width: 1

    anchors.right: parent.right
    anchors.bottom: parent.bottom
    anchors.margins: 12

    implicitWidth: content.implicitWidth + 16
    implicitHeight: content.implicitHeight + 16

    Column {
        id: content
        spacing: 4
        anchors.centerIn: parent

        Text {
            text: `FPS: ${view3d.renderStats.fps}`
            color: "#202020"
            font.pixelSize: 12
            font.bold: true
        }

        Text {
            text: `G API: ${view3d.renderStats.graphicsApiName}`
            color: "#303030"
            font.pixelSize: 11
        }

        Text {
            text: `Render time: ${view3d.renderStats.renderTime} ms`
            color: "#303030"
            font.pixelSize: 11
        }
    }
}
