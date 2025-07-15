import QtQuick
import QtQuick.Layouts

import Themes
import Utils
import TElements

Item {
    id: descriptionItem

    // Text properties
    property string title: "RoboForger by JuSo"
    property string description: "RoboForger is a tool so given a 2D dxf file it can generate the rapid code given some
    parameters."

    TRectangle {
        anchors.fill: parent
        radius: 0
        color: ThemeManager.getColor("background")

        ColumnLayout {
            anchors.fill: parent
            // spacing: 20

            TRectangle {
                color: ThemeManager.getColor("background")
                Layout.fillWidth: true
                Layout.preferredHeight: descriptionItem.height * 0.4

                Image {
                    anchors.centerIn: parent
                    height: parent.height
                    fillMode: Image.PreserveAspectFit
                    source: "qrc:/assets/img/logo.png"
                }
            }

            TText {
                text: descriptionItem.title
                font.pixelSize: 24
                color: ThemeManager.getColor("text")
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }

            TText {
                text: descriptionItem.description
                font.pixelSize: 16
                color: ThemeManager.getColor("text")
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
            }
        }
    }
}
