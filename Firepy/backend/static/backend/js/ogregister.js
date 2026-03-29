document.getElementById("fullname").addEventListener("keydown",function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("email").focus();
    }
});

document.getElementById("email").addEventListener("keydown",function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("username").focus();
    }
});

document.getElementById("username").addEventListener("keydown",function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("password").focus();
    }
});

document.getElementById("password").addEventListener("keydown",function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("confirmpassword").focus();
    }
});
document.getElementById("confirmpassword").addEventListener("keydown",function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("registerbtn").click();
    }
});

function RegisterUser() {
    // Get the values entered in the fullname, email, username , password and  confirmpassword fields
    const fullname = document.getElementById("fullname").value;
    const email = document.getElementById("email").value
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmpassword = document.getElementById("confirmpassword").value;

    // Simple validation (you can extend it based on your needs)
    if (username && password) {
        // Store the username in localStorage
        localStorage.setItem("username", username);

        // Use the variable defined in the HTML template
        window.location.href = typeof newReleasesUrl !== "undefined" ? newReleasesUrl : "/";  // Change to your homepage URL
    } else {
        alert("Please enter all Fields.");
    }
}

 // Password Toggle Function
        function togglePassword(inputId) {
            const passwordInput = document.getElementById(inputId);
            const passwordWrapper = passwordInput.parentElement;
            const eyeOpen = passwordWrapper.querySelector('.eye-open');
            const eyeClosed = passwordWrapper.querySelector('.eye-closed');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                eyeOpen.style.display = 'none';
                eyeClosed.style.display = 'block';
            } else {
                passwordInput.type = 'password';
                eyeOpen.style.display = 'block';
                eyeClosed.style.display = 'none';
            }
        }