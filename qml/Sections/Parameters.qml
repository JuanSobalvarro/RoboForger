// Components/Parameters.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import Themes
import Utils
import TElements
import Components

Item {
    id: parametersItem

    TRectangle {
        id: backgroundRect
        anchors.fill: parent
        color: ThemeManager.getColor("background")

        ColumnLayout {
            id: lcol
            anchors.fill: parent

            // --- Title ---
            TRectangle {
                color: ThemeManager.getColor("background1")
                // radius: 8

                Layout.fillWidth: true
                Layout.preferredHeight: Scaler.font3 * 2

                TText {
                    anchors.centerIn: parent
                    text: "Parameters Configuration"
                    font.pixelSize: Scaler.font3
                    font.bold: true
                    color: ThemeManager.getColor("text")
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    wrapMode: Text.WordWrap
                }
            }

            // --- Parser Section ---
            TRectangle {
                Layout.fillWidth: true
                Layout.leftMargin: Scaler.margin2
                Layout.rightMargin: Scaler.margin2
                Layout.preferredHeight: parserGrid.implicitHeight
                // Layout.alignment: Qt.AlignTop
                color: ThemeManager.getColor("background")

                ColumnLayout {
                    id: parserGrid
                    anchors.fill: parent

                    TText {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Scaler.font4 * 1
                        text: "Parser"
                        font.pixelSize: Scaler.font4
                        font.bold: true
                        color: ThemeManager.getColor("text")
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Scale Factor"
                        placeholder: "Scale (1.0)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1
                    }
                }
            }

            TSeparator {
                Layout.fillWidth: true
                Layout.leftMargin: Scaler.margin2
                Layout.rightMargin: Scaler.margin2
                thickness: 1
                color: ThemeManager.getColor("background_sel")
            }

            // --- Converter Section ---
            TRectangle {
                Layout.fillWidth: true
                Layout.leftMargin: Scaler.margin2
                Layout.rightMargin: Scaler.margin2
                Layout.preferredHeight: converterGrid.implicitHeight
                color: ThemeManager.getColor("background")

                ColumnLayout {
                    id: converterGrid
                    anchors.fill: parent

                    TText {
                        Layout.fillWidth: true
                        text: "Converter"
                        font.pixelSize: Scaler.font4
                        font.bold: true
                        color: ThemeManager.getColor("text")
                    }
                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Float Precision"
                        placeholder: "Precision (2)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Polyline Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Arc Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Circle Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1
                    }
                }
            }

            TSeparator {
                Layout.fillWidth: true
                thickness: 1
                Layout.leftMargin: Scaler.margin2
                Layout.rightMargin: Scaler.margin2
                color: ThemeManager.getColor("background_sel")
            }

            // Drawing and rapid section
            TRectangle {
                Layout.fillWidth: true
                Layout.leftMargin: Scaler.margin2
                Layout.rightMargin: Scaler.margin2
                Layout.preferredHeight: checkboxGrid.implicitHeight
                color: ThemeManager.getColor("background")

                ColumnLayout {
                    id: checkboxGrid
                    anchors.fill: parent
                    spacing: 5

                    TText {
                        Layout.fillWidth: true
                        text: "Drawing and Rapid"
                        font.pixelSize: Scaler.font4
                        font.bold: true
                        color: ThemeManager.getColor("text")
                        Layout.bottomMargin: Scaler.gridSpacing
                    }

                    TCheckBox {
                        text: "Use AI trace detection"
                        checked: false
                        font.pixelSize: Scaler.font6
                        Layout.leftMargin: Scaler.margin2
                        Layout.rightMargin: Scaler.margin2
                        indicatorSize: Scaler.checkboxIndicatorSize2
                        spacing: Scaler.spacing2
                    }

                    TCheckBox {
                        text: "Use Offset programming"
                        checked: false
                        font.pixelSize: Scaler.font6
                        Layout.leftMargin: Scaler.margin2
                        Layout.rightMargin: Scaler.margin2
                        indicatorSize: Scaler.checkboxIndicatorSize2
                        spacing: Scaler.spacing2
                    }
                }
            }
        }
    }
}
