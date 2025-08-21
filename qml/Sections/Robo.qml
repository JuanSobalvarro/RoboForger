import QtQuick
import QtQuick.Layouts

import "../TElements"
import "../Themes"
import "../Components"
import "../Utils"

import ApplicationObjects

Item {
    id: roboItem

    TRectangle {
        id: backgroundRect
        anchors.fill: parent
        color: ThemeManager.getColor("background")

        ColumnLayout {
            anchors.fill: parent

            // Title
            TRectangle {
                color: ThemeManager.getColor("background1")

                Layout.fillWidth: true
                Layout.preferredHeight: 40
                Layout.alignment: Qt.AlignTop

                TText {
                    text: "Robo Parameters"
                    font.pixelSize: 20
                    font.bold: true
                    color: ThemeManager.getColor("text")
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    anchors.centerIn: parent
                }
            }

            // Tool name
            LabeledInput {
                label: "Tool Name"
                placeholder: "Enter tool name (tool0)"
                Layout.fillWidth: true
                Layout.leftMargin: Scaler.margin1
                Layout.rightMargin: Scaler.margin1

                text: Orchestrator.dxfWorker.toolName
                onEditingFinished: {
                    Orchestrator.dxfWorker.toolName = text
                }
            }

            TSeparator {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                Layout.leftMargin: Scaler.margin1
                Layout.rightMargin: Scaler.margin1
            }

            // Workspace limits
            GridLayout {
                Layout.alignment: Qt.AlignHCenter
                columns: 3
                TText {
                    Layout.row: 0
                    Layout.column: 0
                    Layout.columnSpan: 3
                    Layout.rowSpan: 1
                    Layout.bottomMargin: 10
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    text: "Workspace limits InfLimit - SupLimit"
                    font.pixelSize: 16
                    font.bold: true
                    color: ThemeManager.getColor("text")
                }

                ColumnLayout {
                    Layout.row: 1
                    Layout.column: 0
                    Layout.alignment: Qt.AlignHCenter

                    TText {
                        Layout.column: 0
                        Layout.row: 1
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        text: "Inferior Limit Vector"
                        font.pixelSize: 14
                        color: ThemeManager.getColor("text")
                    }
                    NumberLabeledInput {
                        label: "X";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "inferiorLimitX"
                    }
                    NumberLabeledInput {
                        label: "Y";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "inferiorLimitY"
                    }
                    NumberLabeledInput {
                        label: "Z";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "inferiorLimitZ"
                    }
                }


                TSeparator {
                    Layout.row: 1
                    Layout.column: 1
                    Layout.fillHeight: true
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    width: 1
                    thickness: 1
                    orientation: Qt.Vertical
                }

                ColumnLayout {
                    Layout.row: 1
                    Layout.column: 2
                    Layout.alignment: Qt.AlignHCenter

                    TText {
                        Layout.column: 2
                        Layout.row: 1
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        text: "Superior Limit Vector"
                        font.pixelSize: 14
                        color: ThemeManager.getColor("text")
                    }

                    NumberLabeledInput {
                        label: "X";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "superiorLimitX"
                    }
                    NumberLabeledInput {
                        label: "Y";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "superiorLimitY"
                    }
                    NumberLabeledInput {
                        label: "Z";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "superiorLimitZ"
                    }

                }
            }

            TSeparator {
                Layout.fillWidth: true
                Layout.leftMargin: Scaler.margin1
                Layout.rightMargin: Scaler.margin1
                thickness: 1
            }

            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                ColumnLayout {
                    // Origin
                    NumberLabeledInput {
                        label: "Origin X";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "originX"
                        placeholder: "0.0"
                    }
                    NumberLabeledInput {
                        label: "Origin Y";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "originY"
                        placeholder: "0.0"
                    }
                    NumberLabeledInput {
                        label: "Origin Z";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "originZ"
                        placeholder: "0.0"
                    }

                }
                ColumnLayout {
                    // Zero
                    NumberLabeledInput {
                        label: "Zero X";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "zeroX"
                    }
                    NumberLabeledInput {
                        label: "Zero Y";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "zeroY"
                    }
                    NumberLabeledInput {
                        label: "Zero Z";
                        placeholder: "0.0";
                        targetObject: Orchestrator.dxfWorker
                        targetProperty: "zeroZ"
                    }

                }
            }
        }
    }
}