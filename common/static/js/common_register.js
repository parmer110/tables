document.addEventListener("DOMContentLoaded", ()=>{
    var input = document.querySelector("#phone_number");

    var itiOptions = {
      separateDialCode: true,
      utilsScript: utilsScript,
      nationalMode: false,
      preferredCountries: ['us', 'gb', 'ir'],
    };

    fetch('/country-code/')
        .then(response => response.json())
        .then(json => {
            if (json.country_code) {
                itiOptions.initialCountry = json.country_code.toLowerCase();
            } else {
                itiOptions.initialCountry = 'us';
            }

            var iti = window.intlTelInput(input, itiOptions);

            input.addEventListener('blur', () => {
              if (iti.isValidNumber()) {
                input.setCustomValidity('');
              } else {
                input.setCustomValidity('لطفاً یک شماره تلفن معتبر وارد کنید.');
              }
            });
        })
        .catch(error => console.log(error));
});
