// Components/Parameters.qml
import QtQuick
import QtQuick.Layouts

import "../Themes"
import "../Utils"
import "../TElements"
import "../Components"

import ApplicationObjects

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

                        text: isNaN(Orchestrator.dxfWorker.scale) ? "" : Orchestrator.dxfWorker.scale.toString()
                        onEditingFinished: {
                            var value = parseFloat(text)
                            Orchestrator.dxfWorker.scale = !isNaN(value) ? value : 1.0
                        }
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

                        text: Orchestrator.dxfWorker.floatPrecision === 0 ? "" : Orchestrator.dxfWorker.floatPrecision.toString()
                        onEditingFinished: {
                            var value = parseFloat(text)
                            Orchestrator.dxfWorker.floatPrecision = !isNaN(value) && value >= 0 ? value : NaN
                        }
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Polyline Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1

                        text: Orchestrator.dxfWorker.linesVelocity === 0 ? "" : Orchestrator.dxfWorker.linesVelocity.toString()
                        onEditingFinished: {
                            var value = parseFloat(text)
                            Orchestrator.dxfWorker.linesVelocity = !isNaN(value) && value >= 0 ? value : NaN
                        }
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Arc Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1

                        text: Orchestrator.dxfWorker.arcsVelocity === 0 ? "" : Orchestrator.dxfWorker.arcsVelocity.toString()
                        onEditingFinished: {
                            var value = parseFloat(text)
                            Orchestrator.dxfWorker.arcsVelocity = !isNaN(value) && value >= 0 ? value : NaN
                        }
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Circle Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1

                        text: Orchestrator.dxfWorker.circlesVelocity === 0 ? "" : Orchestrator.dxfWorker.circlesVelocity.toString()
                        onEditingFinished: {
                            var value = parseFloat(text)
                            Orchestrator.dxfWorker.circlesVelocity = !isNaN(value) && value >= 0 ? value : NaN
                        }
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Lifting"
                        placeholder: "50"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1

                        text: Orchestrator.dxfWorker.lifting === 0 ? "" : Orchestrator.dxfWorker.lifting.toString()
                        onEditingFinished: {
                            var value = parseFloat(text)
                            Orchestrator.dxfWorker.lifting = !isNaN(value) && value >= 0 ? value : NaN
                        }
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
                        font.pixelSize: Scaler.font6
                        Layout.leftMargin: Scaler.margin2
                        Layout.rightMargin: Scaler.margin2
                        indicatorSize: Scaler.checkboxIndicatorSize2
                        spacing: Scaler.spacing2
                        checked: Orchestrator.dxfWorker.useDetector
                        onCheckedChanged: Orchestrator.dxfWorker.useDetector = checked
                    }

                    TCheckBox {
                        text: "Use Offset programming"
                        font.pixelSize: Scaler.font6
                        Layout.leftMargin: Scaler.margin2
                        Layout.rightMargin: Scaler.margin2
                        indicatorSize: Scaler.checkboxIndicatorSize2
                        spacing: Scaler.spacing2
                        checked: Orchestrator.dxfWorker.useOffset
                        onCheckedChanged: Orchestrator.dxfWorker.useOffset = checked
                    }
                }
            }
        }
    }
}
