pragma Singleton
import QtQuick
import "." as Local

QtObject {
    property string currentThemeName: "dark"

    function isLight() {
        return currentThemeName === "light";
    }

    function setLight() {
        currentThemeName = "light"
        console.log("Light theme set")
    }

    function setDark() {
        currentThemeName = "dark"
        console.log("Dark theme set")
    }

    function getColor(name) {
        const themeData = Local.Themes
        if (themeData && themeData[name]) {
            return themeData[name][currentThemeName];
        } else {
            console.warn(`Color '${name}' not found in theme '${currentThemeName}'`);
            return "#ff0000"; // fallback/error color
        }
    }
}