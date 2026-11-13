"""Идемпотентное наполнение БД начальными данными (сиды).

Запуск из папки backend (с активированным venv или через полный путь):
    ..\\venv\\Scripts\\python.exe seed.py

Скрипт безопасно запускать несколько раз: он ничего не удаляет, а только
создаёт недостающие записи (get_or_create). Пути картинок — в виде
/media/products/... и /media/articles/... .
"""

from datetime import datetime
from decimal import Decimal

from app.db import SessionLocal
from app.models import Article, Category, Product, Role, User
from app.security import hash_password

ADMIN_EMAIL = "admin@roastroad.ru"
ADMIN_PASSWORD = "admin123"
AUTHOR_EMAIL = "author@roastroad.ru"
AUTHOR_PASSWORD = "author123"

COFFEE = [
    {
        "name": "Натти",
        "short": "Плотный кофе со вкусом жареных орехов, печенья и нуги",
        "description": (
            "Плотный кофе со вкусом жареных орехов, печенья и нуги. "
            "Сбалансированный бленд свежей обжарки для эспрессо."
        ),
        "price": "899.00",
        "specs": {"type": "Для эспрессо", "weight": "250гр"},
        "image": "/media/products/coffepack1.png",
    },
    {
        "name": "Батч брю",
        "short": "Сладкий кофе с нотами ананаса, грейпфрута и вишни в шоколаде",
        "description": (
            "Сладкий кофе с нотами ананаса, грейпфрута и вишни в шоколаде. "
            "Яркий и сочный вариант для заваривания в воронке или капельной кофеварке."
        ),
        "price": "1100.00",
        "specs": {"type": "Для фильтра", "weight": "250гр"},
        "image": "/media/products/coffepack2.png",
    },
    {
        "name": "Кэнди",
        "short": "Плотный кофе с нотами тёмной карамели, цукатов и специй",
        "description": (
            "Плотный кофе с нотами тёмной карамели, цукатов и специй. "
            "Насыщенный вкус, который отлично раскрывается в эспрессо и с молоком."
        ),
        "price": "728.00",
        "specs": {"type": "Для эспрессо", "weight": "250гр"},
        "image": "/media/products/coffepack3.png",
    },
    {
        "name": "Колумбия уила",
        "short": "Сочный кофе с нотами красного яблока, тёмного винограда и какао",
        "description": (
            "Сочный кофе с нотами красного яблока, тёмного винограда и какао. "
            "Универсальный сорт для фильтра и дрип-пакетов."
        ),
        "price": "599.00",
        "specs": {"type": "Дрип-пакеты", "weight": "250гр"},
        "image": "/media/products/coffepack4.png",
    },
]

ACCESSORIES = [
    {
        "name": "Весы whitebird kc803",
        "short": "Весы с таймером и аккумулятором для приготовления кофе",
        "description": (
            "Весы с таймером и аккумулятором для приготовления кофе. "
            "Точность до 0.1 г и встроенный таймер — всё, что нужно для заваривания."
        ),
        "price": "3099.00",
        "specs": {},
        "image": "/media/products/acessorypic1.png",
    },
    {
        "name": "Разравниватель MHV 58.35 мм",
        "short": "Разравниватель для кофе, который сделает экстракцию эспрессо более равномерной",
        "description": (
            "Разравниватель для кофе, который сделает экстракцию эспрессо более "
            "равномерной и стабильной. Подходит для корзин диаметром 58 мм."
        ),
        "price": "2639.00",
        "specs": {},
        "image": "/media/products/acessorypic2.png",
    },
    {
        "name": "Питчер MHV черный",
        "short": "Профессиональный питчер для взбивания молока черного цвета",
        "description": (
            "Профессиональный питчер для взбивания молока черного цвета. "
            "Удобный носик для латте-арта и точная шкала объёма."
        ),
        "price": "3119.00",
        "specs": {},
        "image": "/media/products/acessorypic3.png",
    },
    {
        "name": "Аэропресс GO",
        "short": "Компактная версия Аэропресса — удобного устройства для приготовления кофе",
        "description": (
            "Компактная версия Аэропресса — удобного устройства для приготовления "
            "кофе. Помещается в собственную кружку-чехол, идеален для поездок."
        ),
        "price": "5279.00",
        "specs": {},
        "image": "/media/products/acessorypic4.png",
    },
]

ARTICLES = [
    {
        "name": "Основные правила темперовки",
        "short": "Как сделать правильную кофейную таблетку?",
        "content": (
            "Темперовка — это прессование молотого кофе в портафильтре перед "
            "приготовлением эспрессо. От того, насколько ровной и плотной получится "
            "кофейная таблетка, напрямую зависят равномерность экстракции и вкус.\n\n"
            "Главное правило — прессовать от плеча, держа темпер строго "
            "перпендикулярно корзине. Сначала слегка выровняйте кофе, затем приложите "
            "усилие около 15 килограммов. Поверхность таблетки должна оставаться "
            "ровной, без перекосов.\n\n"
            "Если таблетка ломается или остаётся неровной, вода пойдёт по пути "
            "наименьшего сопротивления, и часть кофе окажется недоэкстрагированной. "
            "Практика и контроль перекоса — залог стабильного результата."
        ),
        "tags": ["#Обучение"],
        "image": "/media/articles/articleback1.png",
        "created_at": datetime(2024, 12, 9),
    },
    {
        "name": "Готовим: флэт уайт",
        "short": "Поговорим о том, что такое «Флэт-уайт», и как его готовить.",
        "content": (
            "Флэт уайт — напиток на основе двойного эспрессо и взбитого молока "
            "с тонким слоем микропены. В отличие от капучино, у него меньше пены "
            "и более выраженный кофейный вкус.\n\n"
            "Для приготовления сварите двойную порцию эспрессо и взбейте молоко "
            "до бархатистой текстуры с тонкой микропеной. Аккуратно влейте молоко "
            "в кофе, удерживая пену, чтобы получить ровную поверхность.\n\n"
            "Идеальный флэт уайт имеет кремообразную консистенцию и температуру "
            "около 60 градусов."
        ),
        "tags": ["#Рецепты"],
        "image": "/media/articles/articleback2.png",
        "created_at": datetime(2024, 12, 9),
    },
    {
        "name": "Вкус кофе: Описание",
        "short": "Поговорим о том, как описывается вкус кофе и как не заблудиться в терминах",
        "content": (
            "Описание вкуса кофе может показаться сложным из-за обилия терминов: "
            "кислотность, сладость, тело, послевкусие. Но разобраться в них проще, "
            "чем кажется.\n\n"
            "Кислотность отвечает за яркость и «живость» напитка, сладость — за "
            "баланс, а тело — за плотность и тактильное ощущение во рту. Дегустаторы "
            "часто ищут знакомые ассоциации: фрукты, ягоды, орехи, какао.\n\n"
            "Попробуйте описывать кофе своими словами, сравнивая его со знакомыми "
            "вкусами, — так вы быстрее научитесь замечать нюансы."
        ),
        "tags": ["#Познаем"],
        "image": "/media/articles/articleback3.png",
        "created_at": datetime(2023, 12, 22),
    },
    {
        "name": "Фильтр cerapotta: традиционная керамика и креативные идеи для чистого кофе по вашему вкусу",
        "short": "Рассказываем о преимуществах японского керамического фильтра",
        "content": (
            "Фильтр Cerapotta — традиционный японский керамический фильтр, который "
            "позволяет заваривать чистый кофе без бумажных фильтров. Пористая "
            "керамика задерживает масла и мелкие частицы, оставляя напиток "
            "прозрачным.\n\n"
            "Керамика не впитывает запахи и легко очищается, а вкус получается "
            "мягким и сбалансированным. Для заваривания достаточно поместить фильтр "
            "на чашку, засыпать кофе и медленно вливать горячую воду.\n\n"
            "Это отличный выбор для тех, кто ценит экологичность и хочет раскрыть "
            "деликатные ноты зерна."
        ),
        "tags": ["#Индустрия"],
        "image": "/media/articles/articleback4.png",
        "created_at": datetime(2024, 2, 15),
    },
]


def get_or_create(db, model, defaults: dict, **filters):
    """Возвращает существующую запись по уникальному ключу или создаёт новую."""
    obj = db.query(model).filter_by(**filters).first()
    if obj is None:
        obj = model(**filters, **defaults)
        db.add(obj)
        db.flush()
    return obj


def seed() -> None:
    db = SessionLocal()
    try:
        # 1. Пользователи
        admin = get_or_create(
            db,
            User,
            {
                "password_hash": hash_password(ADMIN_PASSWORD),
                "first_name": "Администратор",
                "role": Role.admin,
            },
            email=ADMIN_EMAIL,
        )
        author = get_or_create(
            db,
            User,
            {
                "password_hash": hash_password(AUTHOR_PASSWORD),
                "first_name": "Оксана",
                "last_name": "Денисова",
                "role": Role.user,
            },
            email=AUTHOR_EMAIL,
        )

        # 2. Категории
        coffee = get_or_create(db, Category, {"name": "Кофе"}, slug="coffee")
        tea = get_or_create(db, Category, {"name": "Чай"}, slug="tea")
        accessories = get_or_create(
            db, Category, {"name": "Аксессуары"}, slug="accessories"
        )
        syrups = get_or_create(db, Category, {"name": "Сиропы"}, slug="syrups")

        # 3. Товары (кофе и аксессуары)
        for item in COFFEE:
            get_or_create(
                db,
                Product,
                {
                    "category_id": coffee.id,
                    "short_description": item["short"],
                    "description": item["description"],
                    "price": Decimal(item["price"]),
                    "images": [item["image"]],
                    "specifications": item["specs"],
                    "stock": 100,
                    "is_active": True,
                },
                name=item["name"],
            )

        for item in ACCESSORIES:
            get_or_create(
                db,
                Product,
                {
                    "category_id": accessories.id,
                    "short_description": item["short"],
                    "description": item["description"],
                    "price": Decimal(item["price"]),
                    "images": [item["image"]],
                    "specifications": item["specs"],
                    "stock": 100,
                    "is_active": True,
                },
                name=item["name"],
            )

        # 4. Статьи
        for item in ARTICLES:
            get_or_create(
                db,
                Article,
                {
                    "author_id": author.id,
                    "short_description": item["short"],
                    "content": item["content"],
                    "images": [item["image"]],
                    "tags": item["tags"],
                    "created_at": item["created_at"],
                },
                name=item["name"],
            )

        db.commit()

        print("Сиды применены (идемпотентно).")
        print(f"  Админ:      {ADMIN_EMAIL} / {ADMIN_PASSWORD}")
        print(f"  Автор:      {AUTHOR_EMAIL} / {AUTHOR_PASSWORD}")
        print(f"  Категории:  {tea.name}, {syrups.name} — без товаров (заглушки)")
        print(f"  Товары:     {len(COFFEE)} кофе + {len(ACCESSORIES)} аксессуаров")
        print(f"  Статьи:     {len(ARTICLES)}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
