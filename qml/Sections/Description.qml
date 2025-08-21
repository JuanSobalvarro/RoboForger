import QtQuick
import QtQuick.Layouts // Ensure this is imported

import Themes
import Utils
import TElements

Item {
    id: descriptionItem

    property string title: "RoboForger by JuSo"
    property string description: "RoboForger is a tool so given a 2D dxf file it can generate the rapid code given some parameters."

    TRectangle {
        anchors.fill: parent
        // color: ThemeManager.getColor("red")
        anchors.topMargin: Scaler.margin4
        anchors.leftMargin: Scaler.margin4
        // anchors.rightMargin: Scaler.margin4
        anchors.bottomMargin: Scaler.margin3

        ColumnLayout {
            id: rootColumnLayout
            anchors.fill: parent

            // spacing: Scaler.spacing2

            TRectangle {
                id: logoRect
                color: ThemeManager.getColor("background")
                Layout.fillWidth: true
                Layout.preferredHeight: rootColumnLayout.height * 0.5 // Set its preferred height (relative to its own parent which is the ColumnLayout now)
                Layout.alignment: Qt.AlignTop

                Image {
                    anchors.centerIn: parent
                    height: Scaler.scale(100)
                    fillMode: Image.PreserveAspectFit
                    source: "qrc:/data/img/logo.png"
                    mipmap: true
                    smooth: true
                }
            }

            TText {
                id: titleText
                text: descriptionItem.title
                font.pixelSize: Scaler.font1
                color: ThemeManager.getColor("text")
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                // Layout.topMargin: Scaler.margin2
                Layout.bottomMargin: Scaler.margin3
            }

            TText {
                text: descriptionItem.description
                font.pixelSize: Scaler.font6
                color: ThemeManager.getColor("text")
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                Layout.bottomMargin: Scaler.margin2
            }
        }
    }
}
