<<<<<<< HEAD
# 🎓 СтудПрофи — Telegram Mini App

Полнофункциональное приложение для Telegram с системой бонусов и рефералов.

## 📋 Структура проекта

```
studprofy/
├── bot.py              # Telegram бот (aiogram)
├── server.py           # FastAPI сервер с API
├── database.py         # SQLite база данных
├── config.py           # Конфигурация и переменные
├── index.html          # Фронтенд Mini App
├── requirements.txt    # Python зависимости
├── .env.example        # Пример переменных окружения
└── README.md           # Этот файл
```

## 🚀 Быстрый старт (локально)

### 1️⃣ Установи зависимости

```bash
pip install -r requirements.txt
```

### 2️⃣ Создай .env файл

```bash
cp .env.example .env
```

Отредактируй `.env` и добавь:
- `BOT_TOKEN` — токен твоего бота от @BotFather
- `ADMIN_IDS` — твой Telegram ID (найди @userinfobot)

### 3️⃣ Запусти бота

```bash
python bot.py
```

### 4️⃣ В отдельном терминале запусти API сервер

```bash
python server.py
```

Сервер будет доступен на `http://localhost:8000`

## 🌍 Деплой на production

### Шаг 1: Разверни фронтенд (index.html)

**Вариант A: Netlify (проще)**
1. Зайди на [netlify.com](https://netlify.com)
2. Sign Up → Connect to Git
3. Загрузи репо или перетащи папку с `index.html`
4. Получишь ссылку вида: `https://твой-сайт.netlify.app`

**Вариант B: GitHub Pages**
1. Создай репо на GitHub
2. Залей `index.html`
3. Settings → Pages → Deploy from branch: main
4. Получишь ссылку: `https://username.github.io/repo`

⚠️ **ВАЖНО: URL должен быть HTTPS!**

### Шаг 2: Разверни сервер API

**Railway.app (рекомендуется, даже бесплатно)**

1. Зайди на [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Выбери свой репо
4. Добавь переменные окружения в Railway:
   - `BOT_TOKEN` 
   - `ADMIN_IDS`
   - `MINI_APP_URL` (ссылка на твой Netlify)

5. Railway автоматически запустит `server.py`
6. Получишь ссылку: `https://твой-проект.railway.app`

### Шаг 3: Обнови переменные окружения

Создай `.env` файл и добавь:

```
BOT_TOKEN=6234567890:ABCDefGHIJKLmnoPQRSTuvWXYZ
ADMIN_IDS=123456789
MINI_APP_URL=https://твой-сайт.netlify.app
SERVER_URL=https://твой-проект.railway.app
DATABASE_FILE=studprofy.db
```

### Шаг 4: Настрой бот в BotFather

1. Открой @BotFather в Telegram
2. `/mybots` → выбери бота → Bot Settings → Menu Button
3. Вставь ссылку на `index.html` (Netlify или GitHub Pages)
4. Теперь в боте появится кнопка 📱 "Открыть приложение"

## 💾 Как работает база данных?

- **SQLite** — встроенная БД (файл `studprofy.db`)
- **Таблицы:**
  - `users` — пользователи (ID, бонусы, заказы)
  - `referrals` — реферальные связи
  - `orders` — заказы студентов
  - `bonus_transactions` — история бонусов

БД создаётся автоматически при первом запуске сервера.

## ⭐ Система бонусов

- **+50 ★** — при регистрации
- **+100 ★** — за заказ
- **+150 ★** — за приглашение друга
- **+300 ★** — за заказ приглашённого друга

**Траты:**
- **100-1000 ★** — скидка на заказ (1 ★ = 1 рубль)
- **1000 ★** — подарок/мерч

## 🔗 API Endpoints

| Метод | Роут | Описание |
|-------|------|---------|
| GET | `/api/user/{user_id}` | Данные пользователя |
| POST | `/api/spend` | Потратить бонусы |
| POST | `/api/order` | Создать заказ |
| GET | `/health` | Проверка сервера |

## 🤖 Команды бота

### Обычные пользователи
- `/start` — главное меню + обработка рефералов
- `/help` — справка
- `/profile` — мой профиль

### Админ команды (только для ADMIN_IDS)
- `/orders` — список всех новых заказов
- `/confirm <order_id>` — подтвердить заказ и начислить +100 ★
- `/stats` — статистика по заказам
- `/bonus <user_id> <amount> <reason>` — добавить бонусы пользователю

## 📱 Mini App функции

- 🏠 **Главная** — баланс, статистика, действия
- 👥 **Рефералы** — копирование ссылки, статистика
- 💳 **Бонусы** — потратить на скидку или подарок
- 📦 **Заказ** — оформить новый заказ
- ⭐ **Как заработать** — все способы заработка

## 🔧 Переменные окружения

| Переменная | Описание | Пример |
|------------|---------|--------|
| `BOT_TOKEN` | Токен бота от @BotFather | `123456:ABC...` |
| `ADMIN_IDS` | ID администраторов (через запятую) | `123456789,987654321` |
| `MINI_APP_URL` | URL фронтенда | `https://site.netlify.app` |
| `SERVER_URL` | URL API сервера | `https://api.railway.app` |
| `DATABASE_FILE` | Путь к БД | `studprofy.db` |

## 🧪 Локальное тестирование

1. Запусти бота: `python bot.py`
2. Запусти сервер: `python server.py`
3. Откройте frontenд: `http://localhost:8000` + замени `SERVER_URL` на `http://localhost:8000`

## 📞 Поддержка

Если возникли вопросы:
- Проверь, установлены ли все зависимости: `pip install -r requirements.txt`
- Убедись, что `BOT_TOKEN` и `ADMIN_IDS` указаны в `.env`
- Проверь логи сервера: `python server.py`

## 🎯 Что дальше?

### Для локального тестирования:
1. Создай бота через @BotFather и получи токен
2. Добавь токен в `.env` файл
3. Запусти: `python bot.py`
4. В другом окне: `python server.py`
5. Тестируй в Telegram

### Для production:
1. Загрузи проект на GitHub
2. Разверни фронтенд на Netlify/GitHub Pages
3. Разверни API на Railway.app
4. Обнови ссылки в BotFather
5. Готово! 🚀

## 📞 Типичные проблемы

**Q: "Бот не отвечает"**
- Проверь `BOT_TOKEN` в `.env`
- Убедись, что `python bot.py` запущен
- Посмотри логи: там должна быть строка "🤖 Бот запускается..."

**Q: "Mini App не загружается"**
- Проверь, что сервер запущен: `python server.py`
- Убедись, что `SERVER_URL` в `index.html` правильный
- Открой DevTools и посмотри ошибки в консоли

**Q: "Бонусы не начисляются"**
- Проверь БД: `sqlite3 studprofy.db`
- Убедись, что API сервер получает запросы от Mini App
- Проверь логи сервера на ошибки

## 📝 Лицензия

MIT — используй свободно! 🎉
