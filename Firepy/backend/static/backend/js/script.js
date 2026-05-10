document.getElementById("username").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("password").focus();
    }
});
document.getElementById("password").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("loginbtn").click();
    }
});

// Password Toggle Function
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eyeOpen = document.querySelector('.eye-open');
    const eyeClosed = document.querySelector('.eye-closed');

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

// Reset Password page Toggle Functions

// New Password Toggle Function
function toggle_New_Password() {
    const New_passwordInput = document.getElementById('new_password');
    const New_eyeOpen = document.querySelector('.eye-open');
    const New_eyeClosed = document.querySelector('.eye-closed');

    if (New_passwordInput.type === 'password') {
        New_passwordInput.type = 'text';
        New_eyeOpen.style.display = 'none';
        New_eyeClosed.style.display = 'block';
    } else {
        New_passwordInput.type = 'password';
        New_eyeOpen.style.display = 'block';
        New_eyeClosed.style.display = 'none';
    }
}


// Confirm Password Toggle Function
function toggle_Confirm_Password() {
    const Confirm_passwordInput = document.getElementById('confirm_password');
    const Confirm_eyeOpen = document.querySelectorAll('.eye-open')[1];
    const Confirm_eyeClosed = document.querySelectorAll('.eye-closed')[1];

    if (Confirm_passwordInput.type === 'password') {
        Confirm_passwordInput.type = 'text';
        Confirm_eyeOpen.style.display = 'none';
        Confirm_eyeClosed.style.display = 'block';
    } else {
        Confirm_passwordInput.type = 'password';
        Confirm_eyeOpen.style.display = 'block';
        Confirm_eyeClosed.style.display = 'none';
    }
}