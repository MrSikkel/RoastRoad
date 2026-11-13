document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("reg-btn");
    const emailInput = document.getElementById("reg-email");
    const passInput = document.getElementById("reg-password");
    const confirmPassInput = document.getElementById("reg-confirm-password");
    const messageEl = document.getElementById("reg-message");

    if (!btn) return;

    btn.addEventListener("click", async (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passInput.value.trim();
        const confirmPassword = confirmPassInput ? confirmPassInput.value.trim() : "";

        // Reset message
        if (messageEl) {
            messageEl.style.display = "none";
            messageEl.textContent = "";
        }

        // 1. Validation
        if (!email || !password || !confirmPassword) {
            displayAlert(false, "Заполните все обязательные поля");
            return;
        }

        if (password !== confirmPassword) {
            displayAlert(false, "Пароли не совпадают");
            return;
        }

        if (password.length < 6) {
            displayAlert(false, "Пароль должен содержать не менее 6 символов");
            return;
        }

        // 2. API Request
        try {
            const response = await fetch("http://127.0.0.1:8000/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json().catch(() => null);

            if (response.ok) {
                displayAlert(true, "Регистрация успешна! Перенаправляю...");
                setTimeout(() => {
                    window.location.href = "auth.html";
                }, 1500);
            } else {
                displayAlert(false, data?.detail || "Ошибка регистрации");
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
