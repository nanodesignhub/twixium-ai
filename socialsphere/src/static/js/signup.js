
document.addEventListener("DOMContentLoaded", () => {
    const signupForm = document.getElementById("signupForm");
    const messageDiv = document.getElementById("message");

    if (signupForm) {
        signupForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await AuthService.register(email, password);
                if (response.message === "User registered successfully") {
                    messageDiv.textContent = "Registration successful! You can now log in.";
                    messageDiv.style.color = "green";
                    signupForm.reset();
                } else {
                    messageDiv.textContent = response.error || "Registration failed.";
                    messageDiv.style.color = "red";
                }
            } catch (error) {
                console.error("Error during registration:", error);
                messageDiv.textContent = "An error occurred during registration.";
                messageDiv.style.color = "red";
            }
        });
    }
});


