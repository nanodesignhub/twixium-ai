
// Twixium.ai - Admin Dashboard Script

document.addEventListener("DOMContentLoaded", () => {
    const sidebarLinks = document.querySelectorAll(".sidebar a");
    const contentSections = document.querySelectorAll(".content section");
    const pageTitle = document.getElementById("page-title");
    const logoutLink = document.getElementById("logout-link");
    const logoutModal = document.getElementById("logoutModal");
    const confirmLogoutBtn = document.getElementById("confirmLogout");
    const cancelLogoutBtn = document.getElementById("cancelLogout");

    // Function to show a specific content section
    const showSection = (sectionId) => {
        contentSections.forEach(section => {
            section.classList.add("hidden");
        });
        document.getElementById(sectionId).classList.remove("hidden");
    };

    // Function to set active link in sidebar
    const setActiveLink = (linkId) => {
        sidebarLinks.forEach(link => {
            link.classList.remove("active");
        });
        document.getElementById(linkId).classList.add("active");
    };

    // Handle sidebar navigation clicks
    sidebarLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            const targetId = link.getAttribute("href").substring(1); // Remove #

            if (targetId === "logout") {
                logoutModal.classList.remove("hidden");
                return;
            }

            setActiveLink(link.id);
            showSection(`${targetId}-content`);
            pageTitle.textContent = link.textContent.trim();

            // Specific actions for each section
            if (targetId === "users") {
                loadUsers();
            }
            // Add more conditions for other sections if they need data loading
        });
    });

    // Initial load: show dashboard
    showSection("dashboard-content");
    setActiveLink("dashboard-link
");

    // Logout Modal Logic
    cancelLogoutBtn.addEventListener("click", () => {
        logoutModal.classList.add("hidden");
    });

    confirmLogoutBtn.addEventListener("click", async () => {
        try {
            const response = await AuthService.logout();
            if (response.message === "Logged out successfully") {
                window.location.href = "/admin-login"; // Redirect to admin login page
            }
        } catch (error) {
            console.error("Error during logout:", error);
            alert("An error occurred during logout.");
        }
    });

    // Function to load users for the User Management section
    async function loadUsers() {
        try {
            const response = await fetch("/api/admin/users");
            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = "/admin-login"; // Redirect to login if unauthorized
                    return;
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const users = await response.json();
            const usersTableBody = document.getElementById("users-table-body");
            usersTableBody.innerHTML = ""; // Clear existing rows

            users.forEach(user => {
                const row = usersTableBody.insertRow();
                row.innerHTML = `
                    <td class="py-2 px-4 border-b">${user.id}</td>
                    <td class="py-2 px-4 border-b">${user.email}</td>
                    <td class="py-2 px-4 border-b">${user.is_admin ? "Yes" : "No"}</td>
                    <td class="py-2 px-4 border-b">
                        <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-1 px-2 rounded text-xs">Delete</button>
                    </td>
                `;
            });
        } catch (error) {
            console.error("Error loading users:", error);
            alert("Failed to load users. Please try again.");
        }
    }
});


