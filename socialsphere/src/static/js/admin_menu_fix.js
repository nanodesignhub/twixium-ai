
document.addEventListener("DOMContentLoaded", () => {
    const sidebarLinks = document.querySelectorAll(".sidebar a");
    const contentSections = document.querySelectorAll(".content section");
    const pageTitle = document.getElementById("page-title");

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
            e.preventDefault(); // Prevent default anchor behavior
            const targetId = link.getAttribute("href").substring(1); // Remove #

            if (targetId === "logout") {
                // Logout logic is handled in admin.js
                return;
            }

            setActiveLink(link.id);
            showSection(`${targetId}-content`);
            pageTitle.textContent = link.textContent.trim();

            // Specific actions for each section if needed
            if (targetId === "users") {
                // Assuming loadUsers() is defined in admin.js and available globally or called here
                if (typeof loadUsers === "function") {
                    loadUsers();
                } else {
                    console.warn("loadUsers function not found. Ensure admin.js is loaded correctly.");
                }
            }
        });
    });

    // Initial load: show dashboard
    showSection("dashboard-content");
    setActiveLink("dashboard-link");
});


