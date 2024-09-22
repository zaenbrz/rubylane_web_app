function validateForm() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var errorMessage = "";

    if (username.trim() === "") {
        errorMessage += "Username is required.<br>";
    }
    if (password.trim() === "") {
        errorMessage += "Password is required.<br>";
    }

    if (errorMessage !== "") {
        document.getElementById("error-message").innerHTML = errorMessage;
        document.getElementById("error-message").style.display = "block";
        return false;
    } else {
        return true;
    }
}
