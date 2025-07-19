
class AuthService {
    static async register(email, password) {
        const response = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });
        return response.json();
    }

    static async login(email, password) {
        const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
        });
        return response.json();
    }

    static async logout() {
        const response = await fetch("/api/auth/logout", {
            method: "POST",
        });
        return response.json();
    }

    static async checkAuthStatus() {
        const response = await fetch("/api/auth/status");
        return response.json();
    }
}


