pragma Singleton
import QtQuick 2.15

QtObject {
    function asset(name) {
        // During development
        return "../../assets/" + name;

        // OR: When using qrc
        // return "qrc:/images/" + name;
    }
}
