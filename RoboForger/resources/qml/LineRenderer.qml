import QtQuick
import QtQuick3D

Model {
    id: renderer

    // Define properties that the parent will inject
    property var shapeGeometry: null 
    property color shapeColor: "white"
    
    // Assign the geometry dynamically
    geometry: shapeGeometry

    materials: [
        DefaultMaterial {
            diffuseColor: renderer.shapeColor
            lighting: DefaultMaterial.NoLighting 
        }
    ]
}