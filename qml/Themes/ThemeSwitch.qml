import QtQuick
import QtQuick.Layouts
import QtQuick.Effects
import TElements
import Utils

Item {
    width: 120
    height: 36

    // This rectangle will be the visual main component with border and color
    TRectangle {
        id: themeSwitch
        width: parent.width
        height: parent.height
        radius: height / 2
        color: ThemeManager.getColor("popup")
        border.color: ThemeManager.getColor("popup_border")
        border.width: 1

        RowLayout {
            anchors.fill: parent
            anchors.margins: 4
            spacing: 4

            // Light theme button
            TButton {
                id: lightButton
                Layout.fillWidth: true
                Layout.fillHeight: true
                backgroundColor: ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                cornerRadius: themeSwitch.radius
                borderWidth: 0
                hoverColor: ThemeManager.getColor("selection_1")
                pressedColor: ThemeManager.getColor("selection_2")

                iconSource: "qrc:/assets/icons/sun.svg"
                iconColor: ThemeManager.isLight() ? "#ffffff" : ThemeManager.getColor("text")
                iconWidth: Scaler.iconSize3
                iconHeight: Scaler.iconSize3
                onClicked: ThemeManager.setLight()
            }

            // Dark theme button
            TButton {
                id: darkButton
                Layout.fillWidth: true
                Layout.fillHeight: true
                backgroundColor: !ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                cornerRadius: themeSwitch.radius
                borderWidth: 0
                hoverColor: ThemeManager.getColor("selection_1")
                pressedColor: ThemeManager.getColor("selection_2")

                iconSource: "qrc:/assets/icons/moon.svg"
                iconColor: !ThemeManager.isLight() ? "#ffffff" : ThemeManager.getColor("text")
                iconWidth: Scaler.iconSize3
                iconHeight: Scaler.iconSize3
                onClicked: ThemeManager.setDark()
            }
        }
    }

    // Qt6: Real shadow using MultiEffect
    MultiEffect {
        anchors.fill: themeSwitch
        source: themeSwitch
        shadowEnabled: true
        shadowBlur: 1.0
        shadowColor: "#88000000"
        shadowVerticalOffset: 4
        shadowHorizontalOffset: 0
        // Optional: enable more effects if needed
    }
}