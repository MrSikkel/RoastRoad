document.addEventListener("DOMContentLoaded", () => {
    const API_URL = "http://127.0.0.1:8000";

    // 1. Session Manager: Run on every page to update auth state in header
    syncUserSession();

    // 2. Route router based on current page elements
    if (document.querySelector(".catalog") || document.querySelector(".offer-items")) {
        loadCatalogProducts();
    }
    
    if (document.querySelector(".item-block")) {
        loadProductDetails();
    }

    if (document.querySelector(".main-content")) {
        loadArticleDetails();
    }

    // === Session Manager Logic ===
    function syncUserSession() {
        const token = localStorage.getItem("token");
        const userDropdown = document.getElementById("userDropdown");
        if (!userDropdown) return;

        const dropdownMenu = userDropdown.nextElementSibling;
        if (!dropdownMenu) return;

        if (token) {
            // User is logged in: swap links
            dropdownMenu.innerHTML = `
                <li><a class="dropdown-item" href="#" id="lk-link">Личный кабинет</a></li>
                <li><a class="dropdown-item" href="#" id="logout-btn">Выйти</a></li>
            `;

            // Bind Log Out
            const logoutBtn = document.getElementById("logout-btn");
            if (logoutBtn) {
                logoutBtn.addEventListener("click", (e) => {
                    e.preventDefault();
                    localStorage.removeItem("token");
                    localStorage.removeItem("userEmail");
                    if (typeof window.showToast === 'function') {
                        window.showToast(true, "Успешный выход из системы");
                    }
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                });
            }

            // Bind LK click
            const lkLink = document.getElementById("lk-link");
            if (lkLink) {
                lkLink.addEventListener("click", (e) => {
                    e.preventDefault();
                    if (typeof window.showToast === 'function') {
                        const email = localStorage.getItem("userEmail") || "Пользователь";
                        window.showToast(true, `Добро пожаловать в личный кабинет, ${email}!`);
                    }
                });
            }
        }
    }

    // === Dynamic Products (Home & Catalog) ===
    async function loadCatalogProducts() {
        const catalogRow = document.querySelector(".catalog .row.g-2");
        const offerItemsRow = document.querySelector(".offer-items");

        try {
            const response = await fetch(`${API_URL}/products?limit=100`);
            if (!response.ok) throw new Error("Failed to fetch products");
            
            const products = await response.json();
            if (products.length === 0) return;

            if (catalogRow && !offerItemsRow) {
                const catalogContainer = document.querySelector(".catalog");
                const rows = catalogContainer.querySelectorAll(".row.g-2");
                
                if (rows.length >= 2) {
                    const coffeeRow = rows[0];
                    const accessoryRow = rows[1];

                    const coffeeProducts = products.filter(p => p.category_id === 1);
                    const accessoryProducts = products.filter(p => p.category_id === 3);

                    if (coffeeProducts.length > 0) {
                        coffeeRow.innerHTML = coffeeProducts.map(p => renderProductCard(p)).join("");
                    }
                    if (accessoryProducts.length > 0) {
                        accessoryRow.innerHTML = accessoryProducts.map(p => renderProductCard(p)).join("");
                    }
                }
            } else if (offerItemsRow) {
                const coffeeProducts = products.filter(p => p.category_id === 1);
                const accessoryProducts = products.filter(p => p.category_id === 3);

                if (coffeeProducts.length > 0) {
                    offerItemsRow.innerHTML = coffeeProducts.map(p => renderProductCard(p)).join("");
                }

                const accessoryItemsRow = document.querySelector(".accessory-items");
                if (accessoryItemsRow && accessoryProducts.length > 0) {
                    accessoryItemsRow.innerHTML = accessoryProducts.map(p => renderProductCard(p)).join("");
                }
            }
        } catch (error) {
            console.error("Error loading products:", error);
        }
    }

    // === Product Description Page Loader ===
    async function loadProductDetails() {
        const urlParams = new URLSearchParams(window.location.search);
        let productId = urlParams.get("id");
        if (!productId) {
            // Default fallback if opened directly without parameter
            productId = "1";
        }

        try {
            // Fetch current product
            const response = await fetch(`${API_URL}/products/${productId}`);
            if (!response.ok) throw new Error("Product not found");
            const p = await response.json();

            // Populate DOM
            const specs = typeof p.specifications === 'string' ? JSON.parse(p.specifications) : p.specifications;
            const type = specs?.type || (p.category_id === 1 ? "Для фильтра" : "Аксессуар");
            const weight = specs?.weight || "250гр";
            const imageSrc = p.images && p.images.length > 0 ? p.images[0] : '../img/item-for-cart.png';

            // Title
            document.title = p.name;

            // Details block elements mapping
            const pictureImg = document.querySelector(".item-block .picture img");
            if (pictureImg) {
                pictureImg.src = imageSrc;
                pictureImg.style.width = "100%";
                pictureImg.style.height = "100%";
                pictureImg.style.objectFit = "contain";
            }

            const hashtag = document.querySelector(".description-block .hashtag");
            if (hashtag) hashtag.textContent = type;

            const title = document.querySelector(".description-block .title");
            if (title) title.textContent = p.name;

            // Update short description
            const shortDesc = document.querySelector(".description-block p.description");
            if (shortDesc) shortDesc.textContent = p.description || "";

            // Update weight & price
            const weightText = document.querySelector(".price-and-size p.description");
            if (weightText) weightText.textContent = weight;

            const priceText = document.querySelector(".price-and-size p.price");
            if (priceText) priceText.textContent = `${Math.round(p.price)}р`;

            // Update full description
            const descriptionTitle = document.querySelector(".description-block .description_title");
            if (descriptionTitle) {
                // Remove existing subsequent sibling paragraphs up until "Доставка:" title
                let sibling = descriptionTitle.nextElementSibling;
                while (sibling && !sibling.textContent.includes("Доставка:")) {
                    const next = sibling.nextElementSibling;
                    sibling.remove();
                    sibling = next;
                }

                // Split long text by paragraphs and insert them
                const paragraphs = (p.description || "Великолепный вкус и высочайшее качество обжарки.").split("\n");
                paragraphs.forEach(text => {
                    if (text.trim() === "") return;
                    const pElement = document.createElement("p");
                    pElement.className = "description";
                    pElement.textContent = text;
                    descriptionTitle.parentNode.insertBefore(pElement, sibling);
                });
            }

            // Bind standard counter button metadata for cart functionality
            const cartBtn = document.querySelector(".description-block .price-and-button .btn-dark");
            if (cartBtn) {
                cartBtn.className = "btn btn-dark cart-btn-add"; // add delegation class
                cartBtn.setAttribute("data-id", p.id);
            }

            // Load similar products
            loadSimilarProducts(p.category_id, p.id);

        } catch (error) {
            console.error("Error loading product details:", error);
        }
    }

    // Load similar products matching current category (excluding current product)
    async function loadSimilarProducts(categoryId, currentId) {
        const sameItemsRow = document.querySelector(".same-items .row.g-2");
        if (!sameItemsRow) return;

        try {
            const response = await fetch(`${API_URL}/products?limit=100`);
            if (!response.ok) return;
            const products = await response.json();
            
            // Filter same category and exclude current
            let similar = products.filter(p => p.category_id === categoryId && p.id !== parseInt(currentId));
            if (similar.length === 0) {
                similar = products.filter(p => p.id !== parseInt(currentId)); // Fallback to other items
            }

            similar = similar.slice(0, 4); // limit to 4
            sameItemsRow.innerHTML = similar.map(p => renderProductCard(p)).join("");

        } catch (err) {
            console.error(err);
        }
    }

    // === Article Description Page Loader ===
    async function loadArticleDetails() {
        const urlParams = new URLSearchParams(window.location.search);
        let articleId = urlParams.get("id");
        if (!articleId) {
            articleId = "1";
        }

        try {
            const response = await fetch(`${API_URL}/articles/${articleId}`);
            if (!response.ok) throw new Error("Article not found");
            const a = await response.json();

            document.title = a.name;

            const tagsList = typeof a.tags === 'string' ? JSON.parse(a.tags) : a.tags;
            const tag = tagsList && tagsList.length > 0 ? tagsList[0] : "#Обучение";
            const imageSrc = a.images && a.images.length > 0 ? a.images[0] : '../img/coffepack1.png';

            const hashtag = document.querySelector(".main-content .hashtag");
            if (hashtag) hashtag.textContent = tag;

            const title = document.querySelector(".main-content .title");
            if (title) title.textContent = a.name;

            const shortDesc = document.querySelector(".main-content .description");
            if (shortDesc) shortDesc.textContent = a.short_description;

            const dateEl = document.querySelector(".attributes .date");
            if (dateEl) dateEl.innerHTML = `<i class="fa-solid fa-calendar-days"></i>  ${formatDate(a.created_at)}`;

            // Body text rendering
            const textOfArticle = document.querySelector(".text-of-article");
            if (textOfArticle) {
                textOfArticle.innerHTML = ""; // Clear static layout

                // Render paragraphs
                const paragraphs = a.content.split("\n");
                paragraphs.forEach((pText, i) => {
                    if (pText.trim() === "") return;
                    const pElement = document.createElement("p");
                    pElement.textContent = pText;
                    textOfArticle.appendChild(pElement);

                    // Insert middle article image after the first paragraph (if available or fallback)
                    if (i === 0) {
                        const img = document.createElement("img");
                        img.src = "../img/article-img.png";
                        img.alt = "";
                        img.style.width = "70%";
                        img.style.display = "block";
                        img.style.margin = "20px 0";
                        textOfArticle.appendChild(img);
                    }
                });
            }

            // Author dynamic block
            const authorImg = document.querySelector(".author img");
            if (authorImg) authorImg.src = "../img/author-image.png";

            const authorName = document.querySelector(".author p");
            if (authorName) authorName.textContent = "Оксана Денисова"; // Default professional author name

            // Load comments
            loadArticleComments(articleId);

            // Load read-too articles
            loadReadTooArticles(a.id);

        } catch (error) {
            console.error("Error loading article details:", error);
        }
    }

    // Load related articles in bottom list
    async function loadReadTooArticles(currentId) {
        const rowGroup = document.querySelector(".main-content .row.g-3");
        if (!rowGroup) return;

        try {
            const response = await fetch(`${API_URL}/articles`);
            if (!response.ok) return;
            const articles = await response.json();

            const related = articles.filter(a => a.id !== currentId).slice(0, 3);
            rowGroup.innerHTML = related.map((a, index) => {
                let tagsList = typeof a.tags === 'string' ? JSON.parse(a.tags) : a.tags;
                let tag = tagsList && tagsList.length > 0 ? tagsList[0] : "#Рецепты";
                let articleId = `article${index + 2}`; // matching user background IDs
                
                return `
                    <div class="col-md-12 col-lg-4 col-sm-12 col-xs-12">
                        <a href="../html's/article.html?id=${a.id}" class="product-link">
                            <div class="article" id="${articleId}">
                                <div class="article-content">
                                    <div class="article-category-tag">${tag}</div>
                                    <div class="article-category-name">${a.name}</div>
                                    <div class="article-category-more">${a.short_description}</div>
                                    <div class="article-datetime col-lg-10 col-md-12 col-sm-12 col-xs-12">
                                        <div class="article-date"><i class="fa-regular fa-lg fa-calendar"></i> ${formatDate(a.created_at)}</div>
                                        <div class="article-time"><i class="fa-regular fa-lg fa-clock"></i> 10 минут на чтение</div>
                                    </div>
                                </div>
                            </div>
                        </a>
                    </div>
                `;
            }).join("");

        } catch (err) {
            console.error(err);
        }
    }

    // Load and write comments
    function loadArticleComments(articleId) {
        const commentsContainer = document.querySelector(".for-centered-comments");
        if (!commentsContainer) return;

        // Fetch comments from localStorage specific to this article or fallback to mock
        const storageKey = `comments_article_${articleId}`;
        let comments = JSON.parse(localStorage.getItem(storageKey));

        if (!comments) {
            // Initial Seed Comments
            comments = [
                {
                    author: "Анастасия",
                    avatar: "../img/author-image.png",
                    text: "Отличная статья! Всё расписано очень доступно и по делу. Раньше таблетка часто ломалась, теперь буду пробовать прессовать от плеча, как рекомендует автор.",
                    likes: 210,
                    timeago: "4 дня назад"
                },
                {
                    author: "Сергей",
                    avatar: "../img/author-image.png",
                    text: "Пользуюсь плоским темпером 58 мм уже год. Сначала было сложно контролировать перекос, но практика всё решает. Спасибо за полезный разбор!",
                    likes: 85,
                    timeago: "1 день назад"
                }
            ];
            localStorage.setItem(storageKey, JSON.stringify(comments));
        }

        renderComments(comments, commentsContainer);

        // Bind comment submit form
        const sendBtn = document.querySelector(".comments .send-button");
        const commentInput = document.querySelector(".comments .input-for-comment");

        if (sendBtn && commentInput) {
            // Clear prior listeners
            const newSendBtn = sendBtn.cloneNode(true);
            sendBtn.parentNode.replaceChild(newSendBtn, sendBtn);

            newSendBtn.addEventListener("click", (e) => {
                e.preventDefault();
                const text = commentInput.value.trim();
                if (!text) {
                    if (typeof window.showToast === 'function') window.showToast(false, "Напишите текст комментария!");
                    return;
                }

                // Check if authenticated
                const email = localStorage.getItem("userEmail") || "Гость";
                const authorName = email.split("@")[0];

                const newComment = {
                    author: authorName.charAt(0).toUpperCase() + authorName.slice(1),
                    avatar: "../img/author-image.png",
                    text: text,
                    likes: 0,
                    timeago: "только что"
                };

                comments.unshift(newComment); // Add to top
                localStorage.setItem(storageKey, JSON.stringify(comments));

                renderComments(comments, commentsContainer);
                commentInput.value = ""; // clear input
                if (typeof window.showToast === 'function') window.showToast(true, "Комментарий успешно добавлен!");
            });
        }
    }

    function renderComments(commentsList, container) {
        container.innerHTML = commentsList.map(c => `
            <div class="example-comment border">
                <div class="name-and-photo">
                    <img src="${c.avatar}" alt="${c.author}" class="comment-author-photo"> ${c.author}
                </div>
                <div class="comment-text">
                    <p>${c.text}</p>
                </div>
                <div class="likes-and-timeago">
                    <div class="likes">
                        <i class="fa-solid fa-thumbs-up"></i> ${c.likes}
                    </div>
                    <div class="timeago">
                        ${c.timeago}
                    </div>
                </div>
            </div>
        `).join("");
    }

    // === Helpers ===
    function renderProductCard(p) {
        let specs = typeof p.specifications === 'string' ? JSON.parse(p.specifications) : p.specifications;
        let type = specs?.type || (p.category_id === 1 ? "Для фильтра" : "Аксессуар");
        let weight = specs?.weight ? `<div class="block-items-weight"><p>${specs.weight}</p></div>` : '';
        let imageSrc = p.images && p.images.length > 0 ? p.images[0] : '../img/coffepack1.png';
        let shortDesc = (p.description || "").split("\n")[0];
        
        return `
            <div class="col-lg-3 col-md-6 col-sm-6 col-xs-12">
                <div class="catalog-block-items p-3 border bg-light">
                    <div class="block-items-img"><img src="${imageSrc}" alt="${p.name}"></div>
                    <div class="block-items-text"> 
                        <div class="block-items-forwhat"><p>${type}</p></div>
                        <div class="block-items-nametag"><p>${p.name}</p></div>
                        <div class="block-items-description"><p>${shortDesc}</p></div>
                        ${weight}
                        <div class="block-items-price"><p>${Math.round(p.price)} Р</p></div>
                    </div>
                    <div class="block-items-buttons">
                        <div class="btn btn-outline-dark see-more-button"><a href="../html's/product_description.html?id=${p.id}">Подробнее</a></div>
                        <div class="btn btn-dark cart-btn-add" data-id="${p.id}"><i class="fas fa-shopping-cart"></i>  В корзину</div>
                    </div>
                </div>
            </div>
        `;
    }

    function formatDate(dateStr) {
        if (!dateStr) return "09.12.2024";
        const date = new Date(dateStr);
        const day = String(date.getDate()).padStart(2, '0');
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const year = date.getFullYear();
        return `${day}.${month}.${year}`;
    }

    // 4. Handle clicks on dynamically rendered "В корзину" buttons using event delegation
    document.addEventListener("click", (e) => {
        const btn = e.target.closest(".cart-btn-add");
        if (btn) {
            const prevCount = parseInt(localStorage.getItem("cartCount")) || 0;
            const currentItemCount = parseInt(document.querySelector(".add-count .count")?.textContent || "1");
            localStorage.setItem("cartCount", prevCount + currentItemCount);
            if (typeof updateCartBadge === 'function') {
                updateCartBadge();
            }
            if (typeof showCartNotification === 'function') {
                showCartNotification();
            }
        }
    });
});
