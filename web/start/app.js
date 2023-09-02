document.getElementById('phoneNumber').addEventListener('keydown', function(e) {
    if (!(/[0-9]/.test(e.key)))
        e.preventDefault();
});

let telegram = window.Telegram.WebApp;

telegram.expand();

telegram.MainButton.text_color = "#FFFFFF";

document.getElementById("sendButton").addEventListener('click', function () {
   let checkBox = document.getElementById("dataProcessingCheck");
   if (!checkBox.checked)
       return {};

   let fullname = document.getElementById("fullName").textContent;
   let email = document.getElementById("email").textContent;
   let phoneNumber = document.getElementById("phoneNumber").textContent;

   return {fullname, email, phoneNumber};
});
