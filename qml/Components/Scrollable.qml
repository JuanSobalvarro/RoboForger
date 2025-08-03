import QtQuick

Item {
    id: root
    clip: true

    property bool autoScrollDown: true

    property alias vScrollbar: scrollV
    property alias hScrollbar: scrollH
    property alias flickable: flick

    Flickable {
        id: flick
        anchors.fill: parent
        clip: true
        interactive: true
        boundsBehavior: Flickable.StopAtBounds

        // Content container
        Item {
            id: contentRoot
            // Always fill horizontally to match Flickable's width
            width: flick.width
            // Vertical: size to children, or use height if you want
            implicitHeight: childrenRect.height
        }

        contentWidth: contentRoot.width        // fill horizontally
        contentHeight: contentRoot.implicitHeight
    }

    Scrollbar {
        id: scrollV
        orientation: Qt.Vertical
        target: flick
        visibleOpacity: 1.0
        breadth: 10
        autoHide: true
    }

    // dont know if working
    Scrollbar {
        id: scrollH
        orientation: Qt.Horizontal
        target: flick
        visible: false
    }

    // Add external children into contentRoot
    default property alias content: contentRoot.data

    onAutoScrollDownChanged: {
        if (autoScrollDown && flick.contentHeight > flick.height) {
            flick.contentY = flick.contentHeight - flick.height;
        }
    }

    Connections {
        target: flick
        function onContentHeightChanged() {
            if (autoScrollDown && flick.contentHeight > flick.height) {
                flick.contentY = flick.contentHeight - flick.height;
            }
        }
    }
}
