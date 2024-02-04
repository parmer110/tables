navigator.geolocation.getCurrentPosition(
    function(position) {
        var form = document.getElementById('login-form');
        var inputLat = document.createElement('input');
        inputLat.type = 'hidden';
        inputLat.name = 'gps_latitude';
        inputLat.value = position.coords.latitude;
        form.appendChild(inputLat);

        var inputLong = document.createElement('input');
        inputLong.type = 'hidden';
        inputLong.name = 'gps_longitude';
        inputLong.value = position.coords.longitude;
        form.appendChild(inputLong);
    },
    function(error) {
        console.error('Error obtaining GPS coordinates', error);
    }
);

