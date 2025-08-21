import QtQuick

LabeledInput {
    property var targetObject
    property string targetProperty: ""

    // Show empty string if Python property is NaN, otherwise show its value
    text: {
        var v = targetObject ? targetObject[targetProperty] : NaN
        return isNaN(v) ? "" : v.toString()
    }

    placeholder: targetObject && !isNaN(targetObject[targetProperty])
                 ? targetObject[targetProperty].toString()
                 : ""

    onEditingFinished: {
        var trimmed = text.trim()
        var value = parseFloat(trimmed)

        if (trimmed === "" || isNaN(value)) {
            targetObject[targetProperty] = NaN
        } else {
            targetObject[targetProperty] = value
        }
    }
}