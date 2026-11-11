document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("auth-btn");
    const emailInput = document.getElementById("auth-email");
    const passInput = document.getElementById("auth-password");
    const messageEl = document.getElementById("auth-message");

    if (!btn) return;

    btn.addEventListener("click", async (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passInput.value.trim();

        // Reset message
        if (messageEl) {
            messageEl.style.display = "none";
            messageEl.textContent = "";
        }

        // 1. Validation
        if (!email || !password) {
            displayAlert(false, "Введите email и пароль");
            return;
        }

        // 2. API Request
        try {
            const response = await fetch("http://127.0.0.1:8000/auth/login-json", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json().catch(() => null);

            if (response.ok && data?.access_token) {
                // Save session token and email in localStorage
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("userEmail", email);

                displayAlert(true, "Успешный вход! Перенаправляю...");
                setTimeout(() => {
                    window.location.href = "home.html";
                }, 1000);
            } else {
                displayAlert(false, data?.detail || "Неверный логин или пароль");
            }

        } catch (error) {
            console.error("Connection error:", error);
            displayAlert(false, "Ошибка соединения с сервером");
        }
    });

    // Helper function to display alerts using Toast or fallback block
    function displayAlert(success, text) {
        if (typeof window.showToast === 'function') {
            window.showToast(success, text);
        } else if (messageEl) {
            messageEl.textContent = text;
            messageEl.className = `reg-message ${success ? 'success' : 'error'}`;
            messageEl.style.display = "block";
        } else {
            alert(text);
        }
    }
});
