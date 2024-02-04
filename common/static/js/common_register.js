import 'intl-tel-input/build/css/intlTelInput.css';
import intlTelInput from 'intl-tel-input';
import utilsScript from 'intl-tel-input/build/js/utils.js';

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

            var iti = intlTelInput(input, itiOptions);
            input.addEventListener('blur', () => {
              if (iti.isValidNumber()) {
                input.setCustomValidity('');
                var fullNumber = iti.getNumber(intlTelInputUtils.numberFormat.E164);
                document.getElementById('fullNumber').value = fullNumber;
              } else {
                input.setCustomValidity('Please enter valid phone number.');
              }
            });
        })
        .catch(error => console.log(error));
});
