import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

import TElements
import GElements

import Utils

import ApplicationObjects

Item {
    id: previewItem

    TRectangle {
        id: background
        anchors.fill: parent
        color: "black"
    }

    View3D {
        id: view
        anchors.fill: parent
        camera: camera

        environment: SceneEnvironment {
            antialiasingMode: SceneEnvironment.MSAA
        }

        // X is red
        // Y is green
        // Z is blue
        AxisHelper {
            enableXYGrid: true
            enableXZGrid: false
            enableYZGrid: false

        }

        PerspectiveCamera {
            id: camera
            position: Qt.vector3d(0, 0, 500)
            clipFar: 10000000
        }

        DirectionalLight {
            // eulerRotation.x: -30
        }

        // Repeater of lines to be drawn
        Repeater3D {
            id: lineRepeater
            model: Orchestrator.dxfWorker.lineModel
            delegate: GLine {
                startPoint: Qt.vector3d(model.start_x, model.start_y, model.start_z)
                endPoint: Qt.vector3d(model.end_x, model.end_y, model.end_z)
                thickness: 10
                scaling: Orchestrator.dxfWorker.scale
                lineColor: "yellow" // Use model color or default to white

                // Component.onCompleted: {
                //     console.log("Model: ", model.start_x);
                // }
            }
        }

        // Repeater of arcs to be drawn
        Repeater3D {
            model: Orchestrator.dxfWorker.arcModel
            delegate: GArc {
                center: Qt.vector3d(model.center_x, model.center_y, model.center_z)
                radius: model.radius
                startAngle: model.start_angle
                endAngle: model.end_angle
                clockwise: model.clockwise
                thickness: 10
                scaling: Orchestrator.dxfWorker.scale
                arcColor: "blue" // Use model color or default to blue

                // Component.onCompleted: {
                //     console.log("Arc Model: ", model.center_x);
                // }
            }
        }

        // Repeater of circles to be drawn
        Repeater3D {
            model: Orchestrator.dxfWorker.circleModel
            delegate: GCircle {
                center: Qt.vector3d(model.center_x, model.center_y, model.center_z)
                radius: model.radius
                thickness: 10
                scaling: Orchestrator.dxfWorker.scale
                circleColor: "green" // Use model color or default to green

                // Component.onCompleted: {
                //     console.log("Circle Model: ", model.center_x);
                // }
            }
        }

        // Repeater for splines
        Repeater3D {
            model: Orchestrator.dxfWorker.splineModel
            delegate: GSpline {
                startPoints: model.startPoints
                endPoints: model.endPoints
                thickness: model.thickness
                lineColor: model.lineColor
                scaling: model.scaling
            }
        }

        // CUbe model test
        // Model {
        //     id: cube
        //     source: "#Cube"
        //     position: Qt.vector3d(0, 0, 0)
        //     materials: PrincipledMaterial {
        //         baseColorMap: Texture {
        //             sourceItem: Rectangle {
        //                 width: 100
        //                 height: 100
        //                 color: "red"
        //             }
        //         }
        //     }
        //
        //     Vector3dAnimation on eulerRotation {
        //         loops: Animation.Infinite
        //         duration: 5000
        //         from: Qt.vector3d(0, 0, 0)
        //         to: Qt.vector3d(360, 0, 360)
        //     }
        // }
    }

    WasdController {
        controlledObject: camera
    }

    TButton {
        id: resetViewButton
        anchors.top: parent.top
        anchors.right: parent.right
        width: 80
        height: 20
        text: "Reset Camera"
        fontSize: Scaler.font8
        onClicked: {
            camera.position = Qt.vector3d(0, 0, 500);
            camera.eulerRotation = Qt.vector3d(0, 0, 0);
            // console.log("Camera view reset to default position and rotation.");
        }
    }

    // Connections {
    //     target: Orchestrator.dxfWorker
    //
    //     function onFileLoaded() {
    //         if (!target) {
    //             console.error("DXF Worker target is not set.");
    //             return;
    //         }
    //
    //         console.log("DXF file loaded successfully.");
    //
    //         // Check if lines is actually a model (list)
    //         if (target.lines && target.lines.length > 0) {
    //             console.log("Number of lines:", target.lines.length);
    //
    //             // Iterate through the first few items to see their properties
    //             var max_items_to_log = Math.min(target.lines.length, 5); // Log up to 5 lines
    //             for (var i = 0; i < max_items_to_log; i++) {
    //                 var line_item = target.lines[i]; // Access item by index
    //                 // Now access individual properties of the dictionary/object
    //                 console.log("Line", i + ":");
    //                 console.log("  start_x:", line_item.start_x);
    //                 console.log("  start_y:", line_item.start_y);
    //                 console.log("  start_z:", line_item.start_z);
    //                 console.log("  end_x:", line_item.end_x);
    //                 console.log("  end_y:", line_item.end_y);
    //                 console.log("  end_z:", line_item.end_z);
    //                 // If you have other properties like 'color', log them too
    //                 // console.log("  color:", line_item.color);
    //             }
    //             if (target.lines.length > max_items_to_log) {
    //                 console.log("...(and", target.lines.length - max_items_to_log, "more lines)");
    //             }
    //         } else {
    //             console.log("No lines found or target.lines is not a valid list.");
    //         }
    //
    //         // You can do similar checks for arcs and circles
    //         if (target.arcs && target.arcs.length > 0) {
    //             console.log("Number of arcs:", target.arcs.length);
    //             // ... log arc details
    //         }
    //         if (target.circles && target.circles.length > 0) {
    //             console.log("Number of circles:", target.circles.length);
    //             // ... log circle details
    //         }
    //     }
    // }
}