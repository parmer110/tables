    document.addEventListener('DOMContentLoaded', () => {
        const logoutLink = document.getElementById('logout-link');
        if (logoutLink) {
            logoutLink.addEventListener('click', handleLogoutClick);
        }
    });

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    function handleLogoutClick (event) {
        event.preventDefault();  // Prevent the default action (navigation)
        var csrfToken = event.target.getAttribute('data-csrf-token');
        var logoutUrl = event.target.getAttribute('data-logout-url');
        // var token = getCookie('access_token');
        
        fetch(logoutUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'Authorization': 'eslope' // + token,
            },
            body: JSON.stringify({}) 
        })
        .then(response => {
            if (response.ok) {
                document.cookie = 'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                localStorage.clear();
                // If logout was successful, redirect to the homepage
                window.location.href = '/';
            } else {
                console.error('Logout failed:', response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));
    }