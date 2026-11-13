document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("auth-btn");
    const emailInput = document.getElementById("auth-email");
    const passInput = document.getElementById("auth-password");

    btn.addEventListener("click", (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passInput.value.trim();

        if (!email || !password) {
            showToast(false, "Введите email и пароль");
            return;
        }

        // Симуляция успешной авторизации
        showToast(true, "Пользователь успешно авторизован");

        setTimeout(() => {
            window.location.href = "../html's/home.html";  // или правильный путь
        }, 1000);
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("reg-btn");
    const emailInput = document.getElementById("reg-email");
    const passInput = document.getElementById("reg-password");
    const confirmPassInput = document.getElementById("reg-confirm-password");

    btn.addEventListener("click", (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passInput.value.trim();
        const confirmPassword = confirmPassInput.value.trim();

        // Проверка на пустые поля
        if (!email || !password || !confirmPassword) {
            showToast(false, "Заполните все поля");
            return;
        }

        // Проверка совпадения паролей
        if (password !== confirmPassword) {
            showToast(false, "Пароли не совпадают");
            return;
        }

        // Дополнительно: простая проверка длины пароля (по желанию)
        if (password.length < 6) {
            showToast(false, "Пароль должен быть не менее 6 символов");
            return;
        }

        // Симуляция успешной регистрации
        showToast(true, "Регистрация успешна");

        // Редирект на авторизацию через 1 секунду
        setTimeout(() => {
            window.location.href = "../html's/auth.html";  // или правильный путь к auth.html
        }, 1000);
    });
});