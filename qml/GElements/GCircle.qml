import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

import GeometryObjects

Model {
    id: circleModel

    property vector3d center: Qt.vector3d(0, 0, 0)
    property real radius: 5.0 // Default radius for the circle
    property real thickness: 1.0 // Thickness of the circle
    property color circleColor: "green" // Color of the circle
    property real scaling: 1.0 // Scale factor for the circle

    geometry: CircleGeometry {
        id: circleGeometry
        thickness: circleModel.thickness
        scale: isNaN(circleModel.scaling) ? 1.0 : circleModel.scaling
        Component.onCompleted: {
            set_circles([{
                center: [circleModel.center.x, circleModel.center.y, circleModel.center.z],
                radius: circleModel.radius,
                thickness: circleModel.thickness
            }]);
        }
    }

    materials: PrincipledMaterial {
        baseColor: circleModel.circleColor
        lighting: PrincipledMaterial.NoLighting
    }

}