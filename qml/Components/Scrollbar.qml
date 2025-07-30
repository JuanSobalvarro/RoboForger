import QtQuick

Item {
    id: scrollbar

    property QtObject target                //< The flickable to control
    property bool autoHide: true            //< If true, the bar will be hidden unless mouseover or moving
    property real visibleOpacity: 0.9       //< When visible (not hidden), how "opaque" are we?
    property int orientation: Qt.Vertical   //< Either Qt.Vertical or Qt.Horizontal

    function decPos(amount) {
        if( !amount ) amount = 0.10;
        let newPos = position - amount;
        if( newPos < 0 )
            newPos = 0;

        scrollbar.position = newPos;
        recalculateHandle();
    }

    function incPos(amount) {
        if( !amount ) amount = 0.10;
        const max = 1-scrollbar.size;
        let newPos = position + amount;
        if( newPos >= max )
            newPos = max;

        scrollbar.position = newPos;
        recalculateHandle();
    }

    // These don't normally need to be set:
    property real minimumSize: 0.1      //< The minimum size of the handle
    property real position: 0           //< The position of the scroller (between 0.0 and 1.0)

    // The rest, as they say, is logic.
    implicitHeight: orientation == Qt.Horizontal ? 24 : parent.height
    implicitWidth: orientation == Qt.Horizontal ? parent.width : 24

    property real size: 0.5
    onSizeChanged: recalculateHandle();
    onPositionChanged: {
        updatePosition();
        recalculateHandle();
    }

    MouseArea {
        id: hoverTester
        anchors.fill: scrollbar
        hoverEnabled: true
    }

    Item {
        id: scrollerHint
        anchors.fill: parent
        opacity: (scrollbar.size < 1) ? (autoHide ? (hoverTester.containsMouse || scrollbar.target.dragging ? scrollbar.visibleOpacity : 0) : scrollbar.visibleOpacity) : 0
        Behavior on opacity {
            NumberAnimation {
                target: scrollerHint
                property: 'opacity'
                duration: 200
            }
        }

        Rectangle {
            id: scrollerHintBG
            y: scrollbar.orientation === Qt.Horizontal ? parent.height * 0.5 - (height * 0.5) : 24
            x: scrollbar.orientation === Qt.Horizontal ? 24 : parent.width * 0.5 - (width * 0.5)
            width: scrollbar.orientation === Qt.Horizontal ? parent.width - 48 : 6
            height: scrollbar.orientation === Qt.Horizontal ? 6 : parent.height - 48
            radius: 3
            color: '#FF0000'

            Rectangle {
                id: handle
                y: scrollbar.orientation === Qt.Horizontal ? parent.height * 0.5 - (height * 0.5) : handle.y
                x: scrollbar.orientation === Qt.Horizontal ? handle.x : parent.width * 0.5 - (width * 0.5)
                width: scrollbar.orientation === Qt.Horizontal ? handle.width : 6
                height: scrollbar.orientation === Qt.Horizontal ? 6 : handle.height
                color: '#00ff00'
                radius: 3

                MouseArea {
                    id: handleDragger
                    anchors.fill: parent
                    cursorShape: scrollbar.orientation == Qt.Horizontal ? Qt.SizeHorCursor : Qt.SizeVerCursor
                    drag {
                        target: parent
                        axis: scrollbar.orientation == Qt.Horizontal ? Drag.XAxis : Drag.YAxis
                        minimumX: 0
                        maximumX: scrollerHintBG.width - handle.width
                        minimumY: 0
                        maximumY: scrollerHintBG.height - handle.height
                        smoothed: true
                        threshold: 0
                    }

                    onMouseXChanged: function(ev) { if( scrollbar.orientation == Qt.Horizontal ) dragged(ev) }
                    onMouseYChanged: function(ev) { if( scrollbar.orientation != Qt.Horizontal ) dragged(ev) }

                    function dragged(ev) {
                        if( !drag.active )
                            return;

                        const myPos = ( scrollbar.orientation == Qt.Horizontal ? handle.x : handle.y );
                        const maxPos = ( scrollbar.orientation == Qt.Horizontal ? (scrollerHintBG.width-handle.width) : (scrollerHintBG.height-handle.height) );

                        const newratio = myPos / maxPos;
                        const newpos = (1-scrollbar.size) * newratio;
                        scrollbar.position = newpos;
                    }
                } // handleDragger
            } // handle
        } // scrollerHintBG
    }

    function recalculateHandlePosition()
    {
        let newHandlePos = scrollbar.position * (scrollbar.orientation == Qt.Horizontal ? scrollbar.width : scrollbar.height);
        if( scrollbar.orientation == Qt.Horizontal )
            handle.x = newHandlePos;
        else
            handle.y = newHandlePos;
    }

    function recalculateHandleSize()
    {
        const maxSize = (scrollbar.orientation == Qt.Horizontal ? scrollbar.width : scrollbar.height);

        let newHandleSize = maxSize * scrollbar.size;
        if( newHandleSize > maxSize )
            newHandleSize = maxSize;
        else if( newHandleSize < 10 )
            newHandleSize = 10;

        if( scrollbar.orientation == Qt.Horizontal )
            handle.width = newHandleSize;
        else
            handle.height = newHandleSize;
    }

    function recalculateHandle() {
        if( handleDragger.drag.active )
            return;

        recalculateHandlePosition();
        recalculateHandleSize();
    }

    Connections {
        target: scrollbar.target
        function onContentWidthChanged() { scrollbar.updateSize(); }
        function onContentHeightChanged() { scrollbar.updateSize(); }
        function onWidthChanged() { scrollbar.updateSize(); }
        function onHeightChanged() { scrollbar.updateSize(); }
        function onContentXChanged() { recentre(); }
        function onContentYChanged() { recentre(); }
    }

    function recentre() {
        // Called to move the handle position to match wherever contentX is:
        if( scrollbar.orientation == Qt.Horizontal )
        {
            if( scrollbar.target.width >= scrollbar.target.contentWidth )
            {
                scrollbar.position = 0;
                scrollbar.target.contentX = 0;
            }
            else if( scrollbar.target.contentX > scrollbar.target.contentWidth - scrollbar.target.width )
                scrollbar.position = (1-scrollbar.size);
            else {
                const diff = scrollbar.target.contentWidth - scrollbar.target.width;
                const cquotient = scrollbar.target.contentX / diff;
                const hquotient = (1-scrollbar.size);

                const newpos = hquotient * cquotient;
                if( newpos >= 0 )
                    scrollbar.position = newpos;
            }
        } else {
            if( scrollbar.target.height >= scrollbar.target.contentHeight )
            {
                scrollbar.position = 0;
                scrollbar.target.contentY = 0;
            }
            else if( scrollbar.target.contentY > scrollbar.target.contentHeight - scrollbar.target.height )
                scrollbar.position = (1-scrollbar.size);
            else {
                const diff = scrollbar.target.contentHeight - scrollbar.target.height;
                const cquotient = scrollbar.target.contentY / diff;
                const hquotient = (1-scrollbar.size);

                const newpos = hquotient * cquotient;
                if( newpos >= 0 )
                    scrollbar.position = newpos;
            }
        }
    }

    function updateSize() {
        // Find the ratio to calculate our handle size:
        const ratio = (scrollbar.orientation == Qt.Horizontal ? (scrollbar.target.width / scrollbar.target.contentWidth) : (scrollbar.target.height / scrollbar.target.contentHeight));
        scrollbar.size = ratio <= 1 ? ratio : 1
    }

    function updatePosition() {
        const quotient = (1-scrollbar.size);
        if( quotient <= 0 )
            return;

        const handlepos = scrollbar.position / quotient;
        const viewportDiff = (scrollbar.orientation == Qt.Horizontal ? (scrollbar.target.contentWidth - scrollbar.target.width) : (scrollbar.target.contentHeight - scrollbar.target.height))
        const diff = viewportDiff * handlepos;

        if( scrollbar.orientation == Qt.Horizontal )
            scrollbar.target.contentX = diff;
        else
            scrollbar.target.contentY = diff;
    }

    Component.onCompleted: recalculateHandle();
}