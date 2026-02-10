import QtQuick
import QtQuick.Controls
import QtQuick3D

Rectangle {
    id: overlayRoot 
    
    anchors.fill: parent
    color: "transparent"
    border.color: "white"
    border.width: 1

    property PerspectiveCamera camera
    property View3D view3d
        
    Button {
        anchors.top: parent.top
        anchors.left: parent.left
        text: "Reset Camera"
        onClicked: {
            if (overlayRoot.camera) {
                overlayRoot.camera.position = Qt.vector3d(500, 500, 1500)
                overlayRoot.camera.eulerRotation = Qt.vector3d(-10, 10, 0)
            }
        }
    }
    
    Text {
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        text: "Preview Scene"
        color: "white"
        font.pixelSize: 14
    }

    // Bottom Info
    Text {
        id: cameraText
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.margins: 10
        color: "white"
        font.pixelSize: 12
        text: overlayRoot.camera ? `Camera: ${overlayRoot.camera.position.x.toFixed(0)}, ${overlayRoot.camera.position.y.toFixed(0)}, ${overlayRoot.camera.position.z.toFixed(0)}` : ""
    }

    RenderStatsOverlay {
        id: renderStatsOverlay
        visible: false // default hidden
        view3d: overlayRoot.view3d
    }

    function toggleRenderStats() {
        renderStatsOverlay.visible = !renderStatsOverlay.visible
    }
}