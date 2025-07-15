import QtQuick
import QtQuick.Layouts
import QtQuick.Effects
import TElements
import Utils

Item {
    width: 160
    height: 48

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
                background.color: ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                background.radius: themeSwitch.radius
                // background: Rectangle {
                //     radius: themeSwitch.radius
                //     color: ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                //     Behavior on color { ColorAnimation { duration: 200 } }
                // }

                iconSource: "qrc:/assets/icons/sun.svg"
                // icon.width: 24
                // icon.height: 24
                iconColor: ThemeManager.isLight() ? "#ffffff" : ThemeManager.getColor("text")
                onClicked: ThemeManager.setLight()
            }

            // Dark theme button
            TButton {
                id: darkButton
                Layout.fillWidth: true
                Layout.fillHeight: true
                background.color: !ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                background.radius: themeSwitch.radius
                // background: Rectangle {
                //     radius: themeSwitch.radius
                //     color: !ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                //     Behavior on color { ColorAnimation { duration: 200 } }
                // }

                iconSource: "qrc:/assets/icons/moon.svg"
                // icon.width: 24
                // icon.height: 24
                iconColor: !ThemeManager.isLight() ? "#ffffff" : ThemeManager.getColor("text")
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