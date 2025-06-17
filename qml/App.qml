import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Themes
import Utils
import TComponents

ApplicationWindow {
    id: appWindow
    width: 1080
    height: 720
    visible: true
    title: "RoboForger by JuSo"

    TRectangle {
        anchors.fill: parent
        color: ThemeManager.getColor("background")

        ColumnLayout {
            anchors.fill: parent
            spacing: 8

            // App Header
            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                Text {
                    text: "RoboForger"
                    font.pixelSize: 24
                    color: ThemeManager.getColor("primary")
                    font.bold: true
                }

                Item { Layout.fillWidth: true }
            }

            // File Buttons + Animation Row
            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                spacing: 24
                anchors.margins: 8

                TButton {
                    text: "➕  Add DXF File"
                    Layout.preferredWidth: 180
                    onClicked: {} // connect later
                }

                Item { Layout.fillWidth: true }

                // TLoader {
                //     running: true // bind this to processing property later
                //     size: 48
                // }

                Item { Layout.fillWidth: true }

                TButton {
                    bg_color: ThemeManager.getColor("selection_1")
                    border_color: ThemeManager.getColor("error")
                    button_text: "Save Rapid Code"
                    text_color: ThemeManager.getColor("text")
                    radius: 10
                    Layout.preferredWidth: 180
                    onClicked: {} // connect later
                }
            }

            // Feedback Section
            TRectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color: ThemeManager.getColor("sidebar_background")
                radius: 8
                border.color: ThemeManager.getColor("sidebar_border")

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 16

                    Text {
                        text: `Figures found: ${feedback.figuresFound}`
                        color: ThemeManager.getColor("text")
                    }
                    Text {
                        text: `Lines: ${feedback.linesFound}`
                        color: ThemeManager.getColor("text")
                    }
                    Text {
                        text: `Arcs: ${feedback.arcsFound}`
                        color: ThemeManager.getColor("text")
                    }
                }
            }

            // Console Area
            // ConsoleOutput {
            //     Layout.fillWidth: true
            //     Layout.fillHeight: true
            //     border.color: ThemeManager.getColor("popup_border")
            // }
        }
        ThemeSwitch {
            anchors.bottom: parent.bottom
            anchors.right: parent.right
        }
    }
}

