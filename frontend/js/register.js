document.querySelector(".send-button").addEventListener("click", async (event) => {
    event.preventDefault();

    const email = document.getElementById("reg-email").value.trim();
    const password = document.getElementById("reg-password").value.trim();

    if (!email || !password) {
        alert("Введите email и пароль.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        if (!response.ok) {
            const error = await response.json();
            alert("Ошибка: " + error.detail);
            return;
        }

        alert("Регистрация успешна!");
        window.location.href = "auth.html";

    } catch (e) {
        alert("Ошибка соединения с сервером.");
        console.error(e);
    }
});


document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("reg-btn");
    const emailInput = document.getElementById("reg-email");
    const passInput = document.getElementById("reg-password");

    btn.addEventListener("click", async (event) => {
    event.preventDefault();

    const email = emailInput.value;
    const password = passInput.value;

    try {
        const response = await fetch("http://127.0.0.1:8000/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json().catch(() => null);

        if (response.ok) {
            message.textContent = "Регистрация успешна! Перенаправляю...";
            message.className = "reg-message success";
            message.style.display = "block";

            setTimeout(() => {
                window.location.href = "/static/html's/auth.html";
            }, 1500);

        } else {
            message.textContent = data?.detail || "Ошибка регистрации";
            message.className = "reg-message error";
            message.style.display = "block";
        }

    } catch (error) {
        message.textContent = "Ошибка соединения с сервером";
        message.className = "reg-message error";
        message.style.display = "block";
    }
});


});
