import QtQuick

LabeledInput {
    property real defaultValue: NaN
    property var targetProperty

    text: targetProperty === defaultValue ? "" : targetProperty.toString()

    Component.onCompleted: updateTextFromTarget()
    onTargetPropertyChanged: updateTextFromTarget()

    function updateTextFromTarget() {
        // Avoid infinite loops
        if (targetProperty === defaultValue) {
            text = "";
        } else {
            let parsed = parseFloat(text);
            if (isNaN(parsed) || parsed !== targetProperty) {
                text = targetProperty.toString();
            }
        }
    }
}
