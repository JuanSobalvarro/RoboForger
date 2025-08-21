import QtQuick
import QtQuick3D
import QtQuick3D.Helpers

import GeometryObjects

Model {
    id: splineModel

    property list<vector3d> startPoints: []
    property list<vector3d> endPoints: []
    property real thickness: 1.0
    property color lineColor: "blue"
    property real scaling: 1.0

    geometry: LineGeometry {
        id: lineGeometry
        thickness: splineModel.thickness
        scale: isNaN(splineModel.scaling) ? 1.0 : splineModel.scaling
        Component.onCompleted: {
            var lines = [];
            for (var i = 0; i < splineModel.startPoints.length; i++) {
                lines.push({
                    start: [splineModel.startPoints[i].x, splineModel.startPoints[i].y, splineModel.startPoints[i].z],
                    end: [splineModel.endPoints[i].x, splineModel.endPoints[i].y, splineModel.endPoints[i].z]
                });
            }
            set_lines(lines);
        }
    }

    materials: PrincipledMaterial {
        baseColor: lineColor
        lighting: PrincipledMaterial.NoLighting
    }
}
