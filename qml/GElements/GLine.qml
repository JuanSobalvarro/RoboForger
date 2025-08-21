// GElements/GLine.qml
import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

import GeometryObjects



Model {
    id: lineModel

    property vector3d startPoint: Qt.vector3d(0, 0, 0)
    property vector3d endPoint: Qt.vector3d(10, 10, 10)
    property real thickness: 1.0 // Increased default thickness for visibility
    property color lineColor: "red"
    property real scaling: 1.0 // Scale factor for the line

    geometry: LineGeometry {
        id: lineGeometry
        thickness: lineModel.thickness
        scale: isNaN(lineModel.scaling) ? 1.0 : lineModel.scaling
        Component.onCompleted: {
            set_lines([{start: [lineModel.startPoint.x, lineModel.startPoint.y, lineModel.startPoint.z],
                end: [lineModel.endPoint.x, lineModel.endPoint.y, lineModel.endPoint.z]}]);
        }
    }

    materials: PrincipledMaterial {
        baseColor: lineColor
        lighting: PrincipledMaterial.NoLighting
    }
}

