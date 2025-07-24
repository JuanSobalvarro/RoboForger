import QtQuick
import QtQuick.Layouts

// Assuming TElements and Themes are in your import paths
import TElements
import Themes

TRectangle {
    id: root
    width: parent.width
    height: 32 // Set an explicit height for clarity
    color: ThemeManager.getColor("background1")

    // Expect a 'Window' object to be passed in. This is more robust.
    property Window window

    DragHandler {
        onActiveChanged: if (active) window.startSystemMove();
        target: null
    }

    // --- WINDOW TITLE (Optional) ---
    TText {
        id: titleLabel
        anchors.centerIn: parent
        text: window ? window.title : "Application" // Bind to window title
        font.pixelSize: 14
        color: ThemeManager.getColor("text")
    }


    // --- WINDOW CONTROL BUTTONS ---
    RowLayout {
        id: windowControlsLayout
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        spacing: 0

        // MINIMIZE BUTTON
        TButton {
            id: minimizeButton
            Layout.fillHeight: true
            Layout.preferredWidth: 45

            iconSource: "qrc:/assets/icons/minimize.svg"
            iconWidth: root.height * 0.4
            iconHeight: root.height * 0.4
            iconColor: ThemeManager.getColor("text")
            hoverColor: ThemeManager.getColor("selection_1")

            borderWidth: 0
            backgroundColor: "transparent"
            onClicked: window?.minimizeAni() // Use optional chaining for safety
        }

        // MAXIMIZE / RESTORE BUTTON
        // TButton {
        //     id: maximizeButton
        //     Layout.fillHeight: true
        //     Layout.preferredWidth: 45
        //
        //     // Toggle icon based on window state
        //     iconSource: window?.visibility === Window.Maximized
        //                 ? "qrc:/assets/icons/restore.svg"
        //                 : "qrc:/assets/icons/maximize.svg"
        //     iconWidth: root.height * 0.4
        //     iconHeight: root.height * 0.4
        //     iconColor: ThemeManager.getColor("text")
        //     hoverColor: ThemeManager.getColor("selection_1")
        //
        //     borderWidth: 0
        //     backgroundColor: "transparent"
        //     onClicked: {
        //         if (window) {
        //             window.visibility = window.visibility === Window.Maximized ? Window.Normal : Window.Maximized
        //         }
        //     }
        // }

        // CLOSE BUTTON
        TButton {
            id: closeButton
            Layout.fillHeight: true
            Layout.preferredWidth: 45

            iconSource: "qrc:/assets/icons/cancel.svg"
            iconWidth: root.height * 0.4
            iconHeight: root.height * 0.4
            iconColor: ThemeManager.getColor("text")
            hoverColor: ThemeManager.getColor("error")

            borderWidth: 0
            backgroundColor: "transparent"
            onClicked: window?.closeAni() // Use close() instead of Qt.quit()
        }
    }
}