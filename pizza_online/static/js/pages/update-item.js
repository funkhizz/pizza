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