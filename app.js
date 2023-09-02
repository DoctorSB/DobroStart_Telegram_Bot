let telegram = window.Telegram.WebApp;

telegram.expand();

telegram.MainButton.text_color = "#FFFFFF";
telegram.MainButton.color = "#2BD455";

let mainButton = document.getElementById("confirmButton");

mainButton.addEventListener("click", function () {
    let check = document.getElementById("checkbox1");
    if (!check.checked)
        return;

    if (telegram.MainButton.isVisible) {
        telegram.MainButton.hide();
    }
    else {
        telegram.MainButton.setText("Подтверждено!");
        telegram.MainButton.show();
    }
});

Telegram.WebApp.onEvent("mainButtonClick", function () {});


function validPhoneNumber(input) {
    input.value = input.value.replace(/\D/g, '');

    if (input.value.length > 11) {
        input.value = input.value.slice(0, 11);
    }
}

