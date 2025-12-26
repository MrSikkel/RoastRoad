const searchIcon = document.querySelector('.search-icon');
const searchContainer = document.querySelector('.search-container');
const overlay = document.querySelector('.overlay');
const searchInput = document.querySelector('.search-container input');

if (searchIcon) {
    searchIcon.addEventListener('click', function (event) {
        event.preventDefault();
        searchContainer.style.display = 'block';
        overlay.style.display = 'block';

        if (searchInput) {
            searchInput.focus();
        }
    });
}

if (searchInput) {
    searchInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            window.location.href = 'catalog.html';
        }
    });
}

if (overlay) {
    overlay.addEventListener('click', function() {
        searchContainer.style.display = 'none';
        overlay.style.display = 'none';
    });
}

// === Универсальный Toast ===
let appToast = null;
let toastEl = null;

document.addEventListener('DOMContentLoaded', () => {
    toastEl = document.getElementById('appToast');
    if (toastEl) {
        appToast = new bootstrap.Toast(toastEl, { delay: 4000 });
    }

    window.showToast = function(success, message) {
        if (!appToast || !toastEl) return;

        const toastBody = toastEl.querySelector('.toast-body');
        toastBody.textContent = message;

        toastEl.classList.remove('text-bg-success', 'text-bg-danger');
        toastEl.classList.add(success ? 'text-bg-success' : 'text-bg-danger');

        appToast.show();
    };
});

// === ПРОМОКОД ===
document.addEventListener('DOMContentLoaded', () => {
    const promoInput = document.querySelector('.promocode-input');
    const promoBtn   = document.querySelector('.promocode .btn');

    if (!promoInput || !promoBtn) return;

    promoBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const value = promoInput.value.trim();

        if (value === '') {
            showToast(false, 'Введите промокод');
            return;
        }

        showToast(true, 'Промокод применён');
        promoInput.value = '';
    });
});

// === Адреса доставки: хранение, добавление, отображение ===
document.addEventListener('DOMContentLoaded', () => {
    const personalInfo = document.querySelector('.personal-info');
    const newAddressFields = document.getElementById('new-address-fields');
    const newAddressRadio = document.getElementById('new-address-radio');
    const existingAddressRadio = document.getElementById('existing-address'); // первый (существующий)

    if (!personalInfo || !newAddressFields || !newAddressRadio) return;

    // Ключ в localStorage
    const ADDRESSES_KEY = 'deliveryAddresses';

    // Создаём кнопку "Сохранить адрес"
    const saveBtn = document.createElement('button');
    saveBtn.textContent = 'Сохранить адрес';
    saveBtn.className = 'btn btn-dark mt-3';
    saveBtn.style.display = 'none';
    newAddressFields.appendChild(saveBtn);

    // Показ кнопки при вводе
    newAddressFields.addEventListener('input', () => {
        const hasValue = Array.from(newAddressFields.querySelectorAll('input'))
            .some(input => input.value.trim() !== '');
        saveBtn.style.display = hasValue ? 'block' : 'none';
    });

    // Загрузка сохранённых адресов
    function loadSavedAddresses() {
        const saved = localStorage.getItem(ADDRESSES_KEY);
        if (saved) {
            const addresses = JSON.parse(saved);
            addresses.forEach(addr => addAddressRadio(addr));
        }
    }

    // Формирование строки адреса для отображения
    function formatAddress(addr) {
        return `г. ${addr.city || 'Томск'}, ул. ${addr.street || ''}, д. ${addr.house || ''}${addr.entrance ? ', подъезд ' + addr.entrance : ''}${addr.floor ? ', этаж ' + addr.floor : ''}${addr.apartment ? ', кв. ' + addr.apartment : ''}`.replace(/,\s*$/, '').trim();
    }

    // Добавление радио-кнопки с адресом
    function addAddressRadio(addr) {
        const div = document.createElement('div');
        div.className = 'existing-one';

        const radioId = 'saved-address-' + Date.now() + Math.random();

        div.innerHTML = `
            <input type="radio" name="address" id="${radioId}" class="radio">
            <label for="${radioId}">${formatAddress(addr)}</label>
        `;

        // Вставляем перед "Добавить новый адрес"
        personalInfo.insertBefore(div, newAddressRadio.parentElement);
    }

    // Сохранение адреса
    saveBtn.addEventListener('click', (e) => {
        e.preventDefault();

        const fields = newAddressFields.querySelectorAll('[data-field]');
        const addr = {};
        let valid = true;

        fields.forEach(field => {
            const value = field.value.trim();
            if (!value && field.placeholder !== 'Подъезд' && field.placeholder !== 'Этаж' && field.placeholder !== 'Квартира') {
                valid = false;
            }
            addr[field.dataset.field] = value;
        });

        if (!valid) {
            showToast(false, 'Заполните обязательные поля (Город, Улица, Дом)');
            return;
        }

        // Получаем текущие адреса или создаём массив
        let addresses = JSON.parse(localStorage.getItem(ADDRESSES_KEY) || '[]');
        addresses.push(addr);
        localStorage.setItem(ADDRESSES_KEY, JSON.stringify(addresses));

        // Добавляем в список
        addAddressRadio(addr);

        // Очищаем поля и скрываем
        fields.forEach(field => field.value = '');
        saveBtn.style.display = 'none';

        // Автоматически выбираем новый адрес
        const newRadio = personalInfo.querySelector(`input[type="radio"]:last-of-type`);
        if (newRadio) newRadio.checked = true;

        showToast(true, 'Адрес успешно сохранён и добавлен в список');
    });

    // Переключение полей
    function toggleNewAddressFields() {
        if (newAddressRadio.checked) {
            newAddressFields.classList.add('show');
        } else {
            newAddressFields.classList.remove('show');
            newAddressFields.querySelectorAll('input').forEach(input => input.value = '');
            saveBtn.style.display = 'none';
        }
    }

    // Инициализация
    loadSavedAddresses();
    toggleNewAddressFields();

    personalInfo.addEventListener('change', (e) => {
        if (e.target.type === 'radio' && e.target.name === 'address') {
            toggleNewAddressFields();
        }
    });
});
// === Логика корзины ===
document.addEventListener('DOMContentLoaded', () => {
    const cartItems = document.querySelectorAll('.cart-item');
    const totalElement = document.querySelector('.total .bold-text');
    const itemsCountElement = document.querySelector('.numbers-in-cart .bold-text');

    if (cartItems.length === 0 || !totalElement || !itemsCountElement) return;

    // Загрузка из localStorage
    function loadCartFromStorage() {
        const savedCart = localStorage.getItem('cartData');
        if (savedCart) {
            const cartData = JSON.parse(savedCart);
            cartData.forEach((item, index) => {
                const cartItem = cartItems[index];
                if (cartItem) {
                    const countEl = cartItem.querySelector('.count');
                    const priceEl = cartItem.querySelector('.price');
                    const unitPrice = parseInt(cartItem.dataset.price);
                    countEl.textContent = item.count;
                    countEl.dataset.count = item.count;
                    priceEl.textContent = `${unitPrice * item.count} руб.`;
                }
            });
        }
    }

    // Пересчёт итога по актуальным элементам
    function updateTotalFresh() {
        let totalPrice = 0;
        let totalItems = 0;

        document.querySelectorAll('.cart-item').forEach(item => {
            const count = parseInt(item.querySelector('.count').dataset.count || 1);
            const price = parseInt(item.dataset.price);
            totalPrice += price * count;
            totalItems += count;
        });

        totalElement.textContent = `${totalPrice} руб.`;
        itemsCountElement.textContent = totalItems;

        if (typeof setCartCount === 'function') {
            setCartCount(totalItems);
        }
    }

    // Сохранение в localStorage по актуальным элементам
    function saveCartToStorageFresh() {
        const cartData = [];
        document.querySelectorAll('.cart-item').forEach(item => {
            const price = parseInt(item.dataset.price);
            const count = parseInt(item.querySelector('.count').dataset.count || 1);
            cartData.push({ price, count });
        });
        localStorage.setItem('cartData', JSON.stringify(cartData));
    }

    // + / - обработчики
    cartItems.forEach(item => {
        const plus = item.querySelector('.add');
        const minus = item.querySelector('.minus');
        const countEl = item.querySelector('.count');
        const priceEl = item.querySelector('.price');
        const unitPrice = parseInt(item.dataset.price);

        plus.addEventListener('click', () => {
            let count = parseInt(countEl.dataset.count || 1);
            count++;
            countEl.textContent = count;
            countEl.dataset.count = count;
            priceEl.textContent = `${unitPrice * count} руб.`;

            updateTotalFresh();
            saveCartToStorageFresh();
        });

        minus.addEventListener('click', () => {
            let count = parseInt(countEl.dataset.count || 1);
            if (count > 1) {
                count--;
                countEl.textContent = count;
                countEl.dataset.count = count;
                priceEl.textContent = `${unitPrice * count} руб.`;

                updateTotalFresh();
                saveCartToStorageFresh();
            }
        });
    });

    // === Удаление товара по мусорке ===
    document.querySelectorAll('.cart-item-delete').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            const cartItem = btn.closest('.cart-item');
            if (!cartItem) return;

            if (confirm('Удалить товар из корзины?')) {
                cartItem.classList.add('removing');
                setTimeout(() => {
                    cartItem.remove();
                    updateTotalFresh();
                    saveCartToStorageFresh();
                    showToast(true, 'Товар удалён из корзины');
                }, 400);
            }
        });
    });

    // === Очистка корзины (если есть кнопка clear-cart-btn) ===
    const clearCartBtn = document.getElementById('clear-cart-btn');
    if (clearCartBtn) {
        clearCartBtn.addEventListener('click', () => {
            if (confirm('Вы уверены, что хотите очистить корзину?')) {
                document.querySelectorAll('.cart-item').forEach(item => item.remove());
                localStorage.removeItem('cartData');
                updateTotalFresh();
                showToast(true, 'Корзина очищена');
            }
        });
    }

    // Инициализация
    loadCartFromStorage();
    updateTotalFresh();
});