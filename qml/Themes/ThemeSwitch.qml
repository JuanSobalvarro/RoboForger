import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Effects
import Utils

Item {
    width: 160
    height: 48

    // This rectangle will be the visual main component with border and color
    Rectangle {
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
            Button {
                id: lightButton
                Layout.fillWidth: true
                Layout.fillHeight: true
                background: Rectangle {
                    radius: themeSwitch.radius
                    color: ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                    Behavior on color { ColorAnimation { duration: 200 } }
                }

                icon.source: Assets.asset("icons/sun.svg")
                icon.width: 24
                icon.height: 24
                icon.color: ThemeManager.isLight() ? "#ffffff" : ThemeManager.getColor("text")
                onClicked: ThemeManager.setLight()
            }

            // Dark theme button
            Button {
                id: darkButton
                Layout.fillWidth: true
                Layout.fillHeight: true
                background: Rectangle {
                    radius: themeSwitch.radius
                    color: !ThemeManager.isLight() ? ThemeManager.getColor("primary") : "transparent"
                    Behavior on color { ColorAnimation { duration: 200 } }
                }

                icon.source: Assets.asset("icons/moon.svg")
                icon.width: 24
                icon.height: 24
                icon.color: !ThemeManager.isLight() ? "#ffffff" : ThemeManager.getColor("text")
                onClicked: ThemeManager.setDark()
            }
        }

        Behavior on color {
            ColorAnimation { duration: 300 }
        }

        Behavior on border.color {
            ColorAnimation { duration: 300 }
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