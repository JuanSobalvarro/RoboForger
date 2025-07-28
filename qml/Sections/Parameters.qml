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

                        text: isNaN(appViewModel.dxfWorker.scale) ? "" : appViewModel.dxfWorker.scale.toString()
                        onTextChanged: {
                            console.log("Scale Factor Changed: ", text);
                            if (text === "") {
                                appViewModel.dxfWorker.scale = NaN;
                            } else {
                                // Ensure the text is a valid number
                                if (!isNaN(parseFloat(text))) {
                                    appViewModel.dxfWorker.scale = parseFloat(text);
                                }
                            }
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

                        text: appViewModel.dxfWorker.floatPrecision === 0 ? "" : appViewModel.dxfWorker.floatPrecision.toString()
                        onTextChanged: {
                            if (text === "") {
                                appViewModel.dxfWorker.floatPrecision = NaN;
                            } else {
                                // Ensure the text is a valid number
                                if (parseFloat(text) >= 0) {
                                    appViewModel.dxfWorker.floatPrecision = parseFloat(text);
                                }
                            }
                        }
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Polyline Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1

                        text: appViewModel.dxfWorker.linesVelocity === 0 ? "" : appViewModel.dxfWorker.linesVelocity.toString()
                        onTextChanged: {
                            if (text === "") {
                                appViewModel.dxfWorker.linesVelocity = NaN;
                            } else {
                                // Ensure the text is a valid number
                                if (parseFloat(text) >= 0) {
                                    appViewModel.dxfWorker.linesVelocity = parseFloat(text);
                                }
                            }
                        }
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Arc Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1

                        text: appViewModel.dxfWorker.arcsVelocity === 0 ? "" : appViewModel.dxfWorker.arcsVelocity.toString()
                        onTextChanged: {
                            if (text === "") {
                                appViewModel.dxfWorker.arcsVelocity = NaN;
                            } else {
                                // Ensure the text is a valid number
                                if (parseFloat(text) >= 0) {
                                    appViewModel.dxfWorker.arcsVelocity = parseFloat(text);
                                }
                            }
                        }
                    }

                    LabeledInput {
                        Layout.fillWidth: true
                        label: "Circle Velocity"
                        placeholder: "Velocity (1000)"
                        Layout.leftMargin: Scaler.margin1
                        Layout.rightMargin: Scaler.margin1

                        text: appViewModel.dxfWorker.circlesVelocity === 0 ? "" : appViewModel.dxfWorker.circlesVelocity.toString()
                        onTextChanged: {
                            if (text === "") {
                                appViewModel.dxfWorker.circlesVelocity = NaN;
                            } else {
                                // Ensure the text is a valid number
                                if (parseFloat(text) >= 0) {
                                    appViewModel.dxfWorker.circlesVelocity = parseFloat(text);
                                }
                            }
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
                        checked: appViewModel.dxfWorker.useDetector

                        onCheckedChanged: appViewModel.dxfWorker.useDetector = checked
                    }

                    TCheckBox {
                        text: "Use Offset programming"
                        font.pixelSize: Scaler.font6
                        Layout.leftMargin: Scaler.margin2
                        Layout.rightMargin: Scaler.margin2
                        indicatorSize: Scaler.checkboxIndicatorSize2
                        spacing: Scaler.spacing2
                        checked: appViewModel.dxfWorker.useOffset

                        onCheckedChanged: appViewModel.dxfWorker.useOffset = checked
                    }
                }
            }
        }
    }
}
