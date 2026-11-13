function showCartNotification(text = "Товар добавлен в корзину") {
    let notification = document.createElement("div");
    notification.textContent = text;

    notification.style.position = "fixed";
    notification.style.top = "20px";
    notification.style.right = "20px";
    notification.style.background = "#212529";
    notification.style.color = "#fff";
    notification.style.padding = "12px 18px";
    notification.style.borderRadius = "6px";
    notification.style.zIndex = "9999";
    notification.style.fontSize = "14px";
    notification.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
    notification.style.opacity = "0";
    notification.style.transition = "opacity 0.3s";

    document.body.appendChild(notification);

    requestAnimationFrame(() => {
        notification.style.opacity = "1";
    });

    setTimeout(() => {
        notification.style.opacity = "0";
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}
let currentCount = 1;

const countEl = document.querySelector(".count");
const plusBtn = document.querySelector(".add");
const minusBtn = document.querySelector(".minus");

if (plusBtn && minusBtn && countEl) {
    plusBtn.addEventListener("click", () => {
        currentCount++;
        countEl.textContent = currentCount;
    });

    minusBtn.addEventListener("click", () => {
        if (currentCount > 1) {
            currentCount--;
            countEl.textContent = currentCount;
        }
    });
}
function getCartCount() {
    return parseInt(localStorage.getItem("cartCount")) || 0;
}

function setCartCount(count) {
    localStorage.setItem("cartCount", count);
    updateCartBadge();
}
function updateCartBadge() {
    const cartIcon = document.querySelector(".fa-shopping-cart");
    if (!cartIcon) return;

    let badge = document.querySelector(".cart-badge");

    if (!badge) {
        badge = document.createElement("span");
        badge.className = "cart-badge";
        badge.style.position = "absolute";
        badge.style.top = "-6px";
        badge.style.right = "-10px";
        badge.style.background = "red";
        badge.style.color = "white";
        badge.style.borderRadius = "50%";
        badge.style.fontSize = "12px";
        badge.style.padding = "2px 6px";
        badge.style.fontWeight = "bold";

        cartIcon.parentElement.style.position = "relative";
        cartIcon.parentElement.appendChild(badge);
    }

    const count = getCartCount();
    badge.textContent = count;
    badge.style.display = count > 0 ? "inline-block" : "none";
}
updateCartBadge();
document.querySelectorAll(".btn.btn-dark").forEach(btn => {
    if (btn.textContent.includes("В корзину")) {
        btn.addEventListener("click", () => {
            const prevCount = getCartCount();
            setCartCount(prevCount + currentCount);

            showCartNotification();
        });
    }
});
