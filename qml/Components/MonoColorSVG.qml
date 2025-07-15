import QtQuick
import Qt5Compat.GraphicalEffects

Item {
    id: svgItem
    anchors.fill: parent

    property string color: "#00000000"
    property alias source: svgImage.source

    Image {
        id: svgImage
        x: (parent.width - width) / 2
        y: (parent.height - height) / 2
        source: "qrc:/assets/utils/monkey.svg"
        fillMode: Image.PreserveAspectFit
        mipmap: true
        smooth: true
        visible: false

    }

    ColorOverlay {
        anchors.fill: parent
        source: svgImage
        color: svgItem.color
    }
}
