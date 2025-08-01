import QtQuick
import QtQuick.Templates as T

import Themes
import TElements.impl

T.CheckBox {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding,
                             implicitIndicatorHeight + topPadding + bottomPadding)

    spacing: 10

    property alias radius: indicator.radius
    property int indicatorSize: 24

    indicator: TCheckIndicator {
        id: indicator
        x: control.text ? (control.mirrored ? control.width - width - control.rightPadding : control.leftPadding) : control.leftPadding + (control.availableWidth - width) / 2
        y: control.topPadding + (control.availableHeight - height) / 2
        control: control
        radius: 5
        implicitWidth: control.indicatorSize
        implicitHeight: control.indicatorSize
        // Can add ripple (wave) here
    }

    contentItem: TText {
        leftPadding: control.indicator && !control.mirrored ? control.indicator.width + control.spacing : 0
        rightPadding: control.indicator && control.mirrored ? control.indicator.width + control.spacing : 0

        text: control.text
        font: control.font
        color: ThemeManager.getColor("text")
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
    }
}
