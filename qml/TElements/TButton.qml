// TComponents/TButton.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import QtQuick.Shapes
import Themes

Item {
    id: root
    width: 120
    height: 40

    // --- Customizable Properties ---
    property string text: ""
    property url iconSource: ""
    property color iconColor: "white"
    property alias background: background

    signal clicked()

    // --- Background ---
    TRectangle {
        id: background
        anchors.fill: parent
        radius: 8
        color: ThemeManager.getColor("primary")
        border.color: "#00000020"
    }

    // --- Icon Only (Centered if no text) ---
    Item {
        id: iconOnlyContainer
        anchors.centerIn: parent
        visible: text === ""
        width: 20
        height: 20

        Image {
            id: rawSvgIconOnly
            source: iconSource
            anchors.fill: parent
            visible: false
            // smooth: true
            mipmap: true
        }

        ColorOverlay {
            anchors.fill: rawSvgIconOnly
            source: rawSvgIconOnly
            color: iconColor
        }
    }

    // --- Icon + Text Layout ---
    RowLayout {
        id: iconAndTextLayout
        anchors.centerIn: parent
        spacing: 8
        visible: text !== ""

        Item {
            id: iconWrapper
            visible: iconSource !== ""
            width: 20
            height: 20

            Image {
                id: rawSvg
                source: iconSource
                anchors.fill: parent
                visible: false
                smooth: true
            }

            ColorOverlay {
                anchors.fill: rawSvg
                source: rawSvg
                color: iconColor
            }
        }

        Text {
            id: label
            text: root.text
            font.pixelSize: 14
            color: "white"
            verticalAlignment: Text.AlignVCenter
        }
    }

    // --- Click Handling ---
    MouseArea {
        id: controlMouseArea
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked()
    }
}
