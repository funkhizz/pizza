const firstElement = document.getElementById('id1')
const secondElement = document.getElementById('id2')

firstElement.addEventListener('change', function () {
    updateSecondElement();
});

function updateSecondElement() {
    secondElement.value = document.getElementById('id1').value;
    secondElement.text = document.getElementById('id1').text;
}

secondElement.addEventListener('change', function () {
    updateFirstElement();
});

function updateFirstElement() {
    firstElement.value = document.getElementById('id2').value;
    firstElement.text = document.getElementById('id2').text;
}

$(document).ready(function () {
    $(".topping-card__title").on("click", function () {
        var div = $(this)
        if (!div.hasClass("base-ingredient")) {
            div.toggleClass("active")
            if (div.children()[0].name == "not_selected") {
                div.children()[0].name = "is_selected";
            } else {
                div.children()[0].name = "not_selected";
            }
        }
    });
});