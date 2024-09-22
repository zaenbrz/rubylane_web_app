$(document).ready(function() {
    $('#login-form').submit(function(event) {
        var username = $('#username').val().trim();
        var password = $('#password').val().trim();
        var errorMessage = '';

        if (username === '') {
            errorMessage += 'Username is required.<br>';
        }
        if (password === '') {
            errorMessage += 'Password is required.<br>';
        }

        if (errorMessage !== '') {
            event.preventDefault(); // Prevent form submission
            $('#error-message').html(errorMessage);
            $('#error-message').show();
        } else {
            $('#error-message').hide();
        }
    });
});
