document.getElementById("username").addEventListener("keydown",function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        document.getElementById("password").focus();
    }
});
document.getElementById("password").addEventListener("keydown",function(event) {
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