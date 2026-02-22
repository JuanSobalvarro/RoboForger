import QtQuick
import QtQuick3D
import QtQuick3D.Helpers
import RoboForger.Geometries 


Item {
    id: root
    width: 400
    height: 400

    View3D {
        id: view3d
        anchors.fill: parent

        environment: SceneEnvironment {
            clearColor: "#010101"
            backgroundMode: SceneEnvironment.Color
            antialiasingMode: SceneEnvironment.MSAA
            antialiasingQuality: SceneEnvironment.VeryHigh
        }

        PerspectiveCamera {
            id: camera
            position: Qt.vector3d(500, 500, 1500)
            eulerRotation: Qt.vector3d(-10, 10, 0)
            clipNear: 1; clipFar: 10000
        }

        DirectionalLight {
            eulerRotation.x: -45; eulerRotation.y: 45; brightness: 2.0
        }

        // grid
        Repeater3D {
            model: gridPolylineModel
            delegate: LineRenderer {
                shapeColor: model.color
                shapeGeometry: PolylineGeometry {
                    points: model.points
                    thickness: model.thickness
                }
            }
        }

        // limits 
        Repeater3D {
            model: limitsPolylineModel
            delegate: LineRenderer {
                shapeColor: model.color
                shapeGeometry: PolylineGeometry {
                    points: model.points
                    thickness: model.thickness
                }
            }
        }

        Repeater3D {
            model: axisPolylineModel
            delegate: LineRenderer {
                shapeColor: model.color
                shapeGeometry: PolylineGeometry {
                    points: model.points
                    thickness: model.thickness
                }
            }
        }

        // polylines
        Repeater3D {
            model: drawingPolylineModel
            delegate: LineRenderer {
                shapeColor: model.color
                shapeGeometry: PolylineGeometry {
                    points: model.points
                    thickness: model.thickness
                }
            }
        }

        // Arcs
        Repeater3D {
            model: drawingArcModel
            delegate: LineRenderer {
                shapeColor: model.color
                shapeGeometry: ArcGeometry {
                    center: model.center
                    radius: model.radius
                    start_angle: model.start_angle
                    end_angle: model.end_angle
                    clockwise: model.clockwise
                    thickness: model.thickness
                }
            }
        }

        // Circles
        Repeater3D {
            model: drawingCircleModel
            delegate: LineRenderer {
                shapeColor: model.color
                shapeGeometry: CircleGeometry {
                    center: model.center
                    radius: model.radius
                    thickness: model.thickness
                }
            }
        }
    }

    // controls
    WasdController { controlledObject: camera }

    PreviewOverlay {
        id: overlay
        anchors.fill: parent
        camera: camera
        view3d: view3d
    }

    function handleKeyPress(event) {
        if (event.key === Qt.Key_U) {
            overlay.toggleRenderStats()
        }
    }

    Keys.onPressed: (event) => handleKeyPress(event)
}