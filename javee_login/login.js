document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Simple validation (replace with real validation logic)
    if (username === "jeni" && password === "javee@123") {
        alert("Login successful!");
        window.location.href = "welcome.html"; // Redirect to another page
    } else {
        document.getElementById("error-message").innerText = "Invalid username or password!";
        document.getElementById("error-message").style.display = "block";
    }
});
