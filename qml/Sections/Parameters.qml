// Components/Parameters.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.FluentWinUI3
// import QtQuick.Controls.Material
import QtQuick.Layouts

import Themes
import Utils
import TElements
import Components

Item {
    id: parametersItem

    Component.onCompleted: {
        Scaler.baseUnit = parametersItem.width / 500
    }

    TRectangle {
        anchors.fill: parent
        color: ThemeManager.getColor("background")

        ColumnLayout {
            id: lcol
            anchors.fill: parent

            // TRectangle {
            //     anchors.fill: parent
            //     color: "red"
            //     radius: 0
            // }

            // --- Title ---
            TRectangle {
                color: ThemeManager.getColor("background1")
                radius: 8

                Layout.fillWidth: true
                Layout.preferredHeight: Scaler.fontMainTitle * 1.5 + Scaler.gridSpacing * 2
                Layout.alignment: Qt.AlignTop

                TText {
                    anchors.centerIn: parent
                    text: "Parameters Configuration"
                    font.pixelSize: Scaler.fontMainTitle
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
                Layout.preferredHeight: parserGrid.implicitHeight
                Layout.alignment: Qt.AlignTop
                color: ThemeManager.getColor("background")
                radius: 8

                ColumnLayout {
                    id: parserGrid
                    anchors.fill: parent

                    TText {
                        Layout.fillWidth: true
                        Layout.preferredHeight: Scaler.fontSubTitle * 1
                        text: "Parser"
                        font.pixelSize: Scaler.fontSubTitle
                        font.bold: true
                        color: ThemeManager.getColor("text")
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Scale Factor"
                        placeholder: "Scale (1.0)"
                    }
                }
            }

            TSeparator {
                Layout.alignment: Qt.AlignTop
                Layout.fillWidth: true
                Layout.leftMargin: Scaler.gridSpacing
                Layout.rightMargin: Scaler.gridSpacing
                thickness: 1
                color: ThemeManager.getColor("background_sel")
            }

            // --- Converter Section ---
            TRectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: converterGrid.implicitHeight
                color: ThemeManager.getColor("background")
                radius: 8

                ColumnLayout {
                    id: converterGrid
                    anchors.fill: parent

                    TText {
                        Layout.fillWidth: true
                        text: "Converter"
                        font.pixelSize: Scaler.fontSubTitle
                        font.bold: true
                        color: ThemeManager.getColor("text")
                        // Layout.bottomMargin: Scaler.gridSpacing
                    }
                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Float Precision"
                        placeholder: "Precision (2)"
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Polyline Velocity"
                        placeholder: "Velocity (1000)"
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Arc Velocity"
                        placeholder: "Velocity (1000)"
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Circle Velocity"
                        placeholder: "Velocity (1000)"
                    }
                }
            }

            TSeparator {
                Layout.fillWidth: true
                thickness: 1
                Layout.leftMargin: Scaler.gridSpacing
                Layout.rightMargin: Scaler.gridSpacing
                color: ThemeManager.getColor("background_sel")
            }

            // Drawing y rapid
            TRectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: checkboxGrid.implicitHeight
                color: ThemeManager.getColor("background")
                radius: 8

                ColumnLayout {
                    id: checkboxGrid
                    anchors.fill: parent

                    TText {
                        Layout.fillWidth: true
                        text: "Drawing and Rapid"
                        font.pixelSize: Scaler.fontSubTitle
                        font.bold: true
                        color: ThemeManager.getColor("text")
                        Layout.bottomMargin: Scaler.gridSpacing
                    }

                    TCheckBox {
                        text: "Use AI trace detection"
                        checked: false
                        font.pixelSize: Scaler.fontCheckbox
                    }

                    TCheckBox {
                        text: "Use Offset programming"
                        checked: false
                        font.pixelSize: Scaler.fontCheckbox
                    }
                }
            }
        }
    }
}
