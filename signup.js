/ static/js/signup.js

document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const messageDiv = document.getElementById('message'); // Assuming a div with id="message" for feedback

    if (signupForm) {
        signupForm.addEventListener('submit', async function(event) {
            event.preventDefault(); // Prevent default form submission

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Basic client-side validation
            if (!email || !password) {
                displayMessage('Please enter both email and password.', 'error');
                return;
            }

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email, password }),
                });

                const data = await response.json();

                if (response.ok) {
                    displayMessage(data.message || 'Registration successful! Redirecting to login...', 'success');
                    // Redirect to login page after successful registration
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 2000); // Redirect after 2 seconds
                } else {
                    displayMessage(data.error || 'Registration failed. Please try again.', 'error');
                }
            } catch (error) {
                console.error('Error during registration:', error);
                displayMessage('An unexpected error occurred. Please try again later.', 'error');
            }
        });
    }

    function displayMessage(message, type) {
        if (messageDiv) {
            messageDiv.textContent = message;
            messageDiv.className = 'p-3 rounded-md mt-4 text-center ';
            if (type === 'success') {
                messageDiv.classList.add('bg-green-100', 'text-green-800');
            } else if (type === 'error') {
                messageDiv.classList.add('bg-red-100', 'text-red-800');
            } else {
                messageDiv.classList.add('bg-blue-100', 'text-blue-800'); // Default for info
            }
            messageDiv.style.display = 'block'; // Ensure it's visible
        }
    }
});
