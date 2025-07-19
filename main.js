
document.addEventListener("DOMContentLoaded", () => {
    // Check auth status on pages that require it
    const protectedRoutes = ["/dashboard"]; // Add other protected routes here

    if (protectedRoutes.includes(window.location.pathname)) {
        AuthService.checkAuthStatus().then(data => {
            if (!data.logged_in) {
                window.location.href = "/login";
            }
        });
    }
});

