import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

import GeometryObjects

Model {
    id: arcModel

    property vector3d center: Qt.vector3d(0, 0, 0)
    property real radius: 5.0 // Default radius for the arc
    property real startAngle: 0.0 // Start angle in degrees
    property real endAngle: 90.0 // End angle in degrees
    property bool clockwise: true // Direction of the arc, true for clockwise
    property real thickness: 1.0 // Thickness of the arc
    property color arcColor: "blue" // Color of the arc
    property real scaling: 1.0 // Scale factor for the arc

    geometry: ArcGeometry {
        id: arcGeometry
        thickness: arcModel.thickness
        scale: isNaN(arcModel.scaling) ? 1.0 : arcModel.scaling
    }

    materials: PrincipledMaterial {
        baseColor: arcColor
        lighting: PrincipledMaterial.NoLighting
    }

    function updateGeometry() {
        arcGeometry.set_arcs([{
            center: [arcModel.center.x, arcModel.center.y, arcModel.center.z],
            radius: arcModel.radius,
            startAngle: arcModel.startAngle,
            endAngle: arcModel.endAngle,
            clockwise: arcModel.clockwise,
            thickness: arcModel.thickness
        }]);
    }

    Component.onCompleted: updateGeometry()

    // onCenterChanged: updateGeometry()
    // onRadiusChanged: updateGeometry()
    // onStartAngleChanged: updateGeometry()
    // onEndAngleChanged: updateGeometry()
    // onClockwiseChanged: updateGeometry()
    // onThicknessChanged: updateGeometry()
    // onScalingChanged: {
    //     arcGeometry.scale = isNaN(arcModel.scaling) ? 1.0 : arcModel.scaling;
    //     updateGeometry()
    // }
}