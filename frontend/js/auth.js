document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("auth-btn");
    const emailInput = document.getElementById("auth-email");
    const passInput = document.getElementById("auth-password");
    const message = document.getElementById("auth-message");

    btn.addEventListener("click", async (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passInput.value.trim();

        if (!email || !password) {
            message.textContent = "Введите email и пароль";
            message.className = "reg-message error";
            message.style.display = "block";
            return;
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/auth/login-json", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!response.ok) {
                message.textContent = data.detail || "Ошибка авторизации";
                message.className = "reg-message error";
                message.style.display = "block";
                return;
            }

            // Сохраняем токен
            localStorage.setItem("token", data.access_token);

            // Сообщение + редирект
            message.textContent = "Успешный вход. Перенаправляю...";
            message.className = "reg-message success";
            message.style.display = "block";

            setTimeout(() => {
                window.location.href = "/static/html's/home.html";
            }, 1000);

        } catch (err) {
            message.textContent = "Нет соединения с сервером";
            message.className = "reg-message error";
            message.style.display = "block";
        }
    });
});
