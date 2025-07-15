import QtQuick
import QtQuick.Shapes
import QtQuick.Controls
import Themes

Item {
    id: loader
    property bool running: true
    property int size: 50
    property color color: ThemeManager.getColor("primary") // Color del loader

    width: size
    height: size

    BusyIndicator {
        running: loader.running
    }
}