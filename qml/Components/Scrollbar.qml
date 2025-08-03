import QtQuick

Item {
    id: scrollbar
    property Flickable target
    property bool autoHide: true
    property real visibleOpacity: 0.8
    property real fadedOpacity: 0.2
    property int orientation: Qt.Vertical
    property real breadth: 8
    property int handleMargin: breadth / 3

    // Size and position
    property real position: 0.0
    property real size: 0.5
    property real minimumSize: 10

    property color backgroundColor: "#222"
    property color handleColor: "#888"

    anchors {
        right: parent.right
        top: parent.top
        bottom: orientation === Qt.Vertical ? parent.bottom : undefined
        left: orientation === Qt.Horizontal ? parent.left : undefined
    }
    width: orientation === Qt.Vertical ? breadth : parent.width
    height: orientation === Qt.Horizontal ? breadth : parent.height

    // Show only when target exists and content is scrollable
    visible: target && size < 1.0

    // Background
    Rectangle {
        id: track
        anchors.fill: parent
        color: backgroundColor
        radius: 4
        opacity: autoHide ? fadedOpacity : visibleOpacity
        Behavior on opacity { NumberAnimation { duration: 200 } }

        // Track click -> jump
        // MouseArea {
        //     anchors.fill: parent
        //     onClicked: {
        //         if (!target) return
        //         let totalSize = orientation === Qt.Vertical
        //             ? target.contentHeight - target.height
        //             : target.contentWidth - target.width
        //         if (totalSize <= 0) return
        //
        //         if (orientation === Qt.Vertical) {
        //             let ratio = (mouse.y - handle.height / 2) / (track.height - handle.height)
        //             target.contentY = Math.max(0, Math.min(1, ratio)) * totalSize
        //         } else {
        //             let ratio = (mouse.x - handle.width / 2) / (track.width - handle.width)
        //             target.contentX = Math.max(0, Math.min(1, ratio)) * totalSize
        //         }
        //     }
        // }
    }

    // Handle
    Rectangle {
        id: handle
        radius: 4
        color: handleColor
        opacity: autoHide ? visibleOpacity : visibleOpacity
        Behavior on opacity { NumberAnimation { duration: 200 } }

        width: orientation === Qt.Vertical
            ? parent.width - (handleMargin * 2)
            : Math.max(size * (parent.width - (handleMargin * 2)), minimumSize)
        height: orientation === Qt.Vertical
            ? Math.max(size * (parent.height - (handleMargin * 2)), minimumSize)
            : parent.height - (handleMargin * 2)

        x: orientation === Qt.Vertical
            ? handleMargin
            : handleMargin + position * ((parent.width - (handleMargin * 2)) - width)
        y: orientation === Qt.Vertical
            ? handleMargin + position * ((parent.height - (handleMargin * 2)) - height)
            : handleMargin

        MouseArea {
            anchors.fill: parent
            cursorShape: orientation === Qt.Vertical ? Qt.SizeVerCursor : Qt.SizeHorCursor
            drag.target: handle
            drag.axis: orientation === Qt.Vertical ? Drag.YAxis : Drag.XAxis
            drag.minimumX: handleMargin
            drag.minimumY: handleMargin
            drag.maximumX: orientation === Qt.Vertical
                ? parent.width - handle.width - handleMargin
                : parent.width - handle.width - handleMargin
            drag.maximumY: orientation === Qt.Vertical
                ? scrollbar.height - handle.height - handleMargin
                : scrollbar.height - handle.height - handleMargin

            onPositionChanged: {
                let maxPos = orientation === Qt.Vertical
                    ? (track.height - (handleMargin * 2)) - handle.height
                    : (track.width - (handleMargin * 2)) - handle.width
                let ratio = orientation === Qt.Vertical
                    ? (handle.y - handleMargin) / maxPos
                    : (handle.x - handleMargin) / maxPos
                if (target) {
                    if (orientation === Qt.Vertical)
                        target.contentY = ratio * (target.contentHeight - target.height)
                    else
                        target.contentX = ratio * (target.contentWidth - target.width)
                }
            }
        }
    }

    // Updates
    Connections {
        target: scrollbar.target
        function onContentHeightChanged() { updateSize() }
        function onContentWidthChanged() { updateSize() }
        function onHeightChanged() { updateSize() }
        function onWidthChanged() { updateSize() }
        function onContentYChanged() { updatePosition() }
        function onContentXChanged() { updatePosition() }
    }

    function updateSize() {
        if (!target) return
        size = orientation === Qt.Vertical
            ? Math.min(1.0, target.height / target.contentHeight)
            : Math.min(1.0, target.width / target.contentWidth)
    }

    function updatePosition() {
        if (!target) return
        let maxScroll = orientation === Qt.Vertical
            ? target.contentHeight - target.height
            : target.contentWidth - target.width
        position = maxScroll > 0
            ? (orientation === Qt.Vertical ? target.contentY : target.contentX) / maxScroll
            : 0
    }

    Component.onCompleted: {
        updateSize()

    }
}
