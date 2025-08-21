import QtQuick
import QtQuick.Effects

Item {
    id: svgItem

    property string color: "#ff0000ff"
    property bool mipmap: true
    property bool smooth: true

    property alias source: svgImage.source

    Image {
        id: svgImage    
        anchors.fill: parent
        fillMode: Image.PreserveAspectFit
        source: "qrc:/data/utils/monkey.svg"
        mipmap: svgItem.mipmap
        smooth: svgItem.smooth
        visible: false
    }

    MultiEffect {
        anchors.fill: svgImage
        source: svgImage
        colorization: 1.0
        colorizationColor: svgItem.color
    }
}
