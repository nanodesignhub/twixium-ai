document.addEventListener("DOMContentLoaded", () => {
    const adminLoginForm = document.getElementById("adminLoginForm");
    const messageDiv = document.getElementById("message");

    if (adminLoginForm) {
        adminLoginForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const email = document.getElementById("email").value;
            const password = document.getElementById("password").value;

            try {
                const response = await AuthService.login(email, password);
                if (response.message === "Login successful" && response.is_admin) {
                    messageDiv.textContent = "Login successful! Redirecting...";
                    messageDiv.style.color = "green";
                    window.location.href = "/admin"; // Redirect to admin dashboard
                } else if (response.message === "Login successful" && !response.is_admin) {
                    messageDiv.textContent = "You do not have admin privileges.";
                    messageDiv.style.color = "red";
                } else {
                    messageDiv.textContent = response.error || "Login failed.";
                    messageDiv.style.color = "red";
                }
            } catch (error) {
                console.error("Error during admin login:", error);
                messageDiv.textContent = "An error occurred during login.";
                messageDiv.style.color = "red";
            }
        });
    }
});


