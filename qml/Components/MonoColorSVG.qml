import QtQuick
import Qt5Compat.GraphicalEffects

Item {
    id: svgItem

    property string color: "#00000000"
    property bool mipmap: true
    property bool smooth: true

    property alias source: svgImage.source

    Image {
        id: svgImage
        anchors.fill: parent
        fillMode: Image.PreserveAspectFit
        source: "qrc:/assets/utils/monkey.svg"
        mipmap: svgItem.mipmap
        smooth: svgItem.smooth
        visible: false
    }

    ColorOverlay {
        anchors.fill: parent
        source: svgImage
        color: svgItem.color
    }
}
