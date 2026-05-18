# 🔧 Полная инструкция по настройке СтудПрофи

## ❗ Что нужно ДО НАЧАЛА

1. **Аккаунт Telegram** — для создания бота
2. **Python 3.9+** — на твоем компьютере
3. **Git** — для загрузки проекта
4. **Аккаунт GitHub** (опционально) — для автоматического деплоя

## 📱 Шаг 1: Создай Telegram бота

### 1.1 Создай бота через @BotFather

1. Открой Telegram → поиск → `@BotFather`
2. Нажми `/start`
3. Нажми `/newbot`
4. Следуй инструкциям:
   - Название: `СтудПрофи` (или твое)
   - Username: `StudProfyBot` (уникальное имя)
5. **Скопируй токен!** Он будет вида:
   ```
   6234567890:ABCDefGHIJKLmnoPQRSTuvWXYZ123456789
   ```

### 1.2 Получи свой ID в Telegram

1. Открой `@userinfobot`
2. Он тебе напишет твой ID (число вида `123456789`)
3. Скопируй этот ID

## 💻 Шаг 2: Локальная установка

### 2.1 Склонируй проект

```bash
git clone https://github.com/твое-имя/StudProfy.git
cd StudProfy
```

### 2.2 Создай `.env` файл

Открой текстовый редактор и создай файл `.env`:

```env
BOT_TOKEN=6234567890:ABCDefGHIJKLmnoPQRSTuvWXYZ123456789
ADMIN_IDS=123456789
MINI_APP_URL=http://localhost:8000
SERVER_URL=http://localhost:8000
DATABASE_FILE=studprofy.db
```

**Замени значения:**
- `BOT_TOKEN` — токен от @BotFather
- `ADMIN_IDS` — твой ID из @userinfobot

### 2.3 Установи зависимости

```bash
pip install -r requirements.txt
```

### 2.4 Запусти приложение

**Терминал 1 — Бот:**
```bash
python bot.py
```

Должна вывести:
```
🤖 Бот запускается...
```

**Терминал 2 — API сервер:**
```bash
python server.py
```

Должна вывести:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2.5 Тестируй в Telegram

1. Открой Telegram
2. Найди своего бота (тот что создал)
3. Нажми `/start`
4. Должна появиться кнопка "🎓 Открыть приложение"
5. Нажми на неё — откроется Mini App

## 🌍 Шаг 3: Деплой на production

### 3.1 Раздели приложение на фронтенд и бэкенд

#### A) Фронтенд на Netlify

1. Зайди на [netlify.com](https://netlify.com)
2. Sign Up → Логин через GitHub (если есть)
3. **Вариант 1:** Drag and Drop
   - Создай папку `frontend` с файлом `index.html`
   - Перетащи на Netlify
   - Получишь URL: `https://твой-сайт.netlify.app`

4. **Вариант 2:** Git Deploy
   - Создай GitHub репо с твоим проектом
   - На Netlify: "New site from Git"
   - Выбери репо
   - Deploy!

#### B) Бэкенд на Railway

1. Зайди на [railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub"
3. Авторизуйся через GitHub
4. Выбери свой репо
5. Добавь переменные окружения:
   - Нажми на проект
   - Variables → Add Variable
   - Добавь:
     ```
     BOT_TOKEN=6234567890:ABCDefGHIJKLmnoPQRSTuvWXYZ123456789
     ADMIN_IDS=123456789
     MINI_APP_URL=https://твой-сайт.netlify.app
     SERVER_URL=https://твой-проект.railway.app
     DATABASE_FILE=studprofy.db
     ```
6. Railway автоматически запустит `server.py`
7. Получишь URL вида: `https://твой-проект.railway.app`

### 3.2 Настрой бота в BotFather

1. Открой `@BotFather`
2. `/mybots` → выбери бота
3. Bot Settings → Menu Button
4. Вставь ссылку:
   ```
   https://твой-сайт.netlify.app
   ```

### 3.3 Обнови `.env` на production

На Railway обнови переменные:

```env
BOT_TOKEN=6234567890:ABCDefGHIJKLmnoPQRSTuvWXYZ123456789
ADMIN_IDS=123456789
MINI_APP_URL=https://твой-сайт.netlify.app
SERVER_URL=https://твой-проект.railway.app
DATABASE_FILE=studprofy.db
```

## ✅ Проверка что всё работает

### Локально:

1. ✅ Бот отвечает на `/start`
2. ✅ Кнопка "Открыть приложение" появляется
3. ✅ Mini App загружается и показывает баланс (0 бонусов)
4. ✅ Можешь перейти на другие экраны (Рефералы, Заказ и т.д.)
5. ✅ При оформлении заказа появляется уведомление

### На production:

1. ✅ Бот работает в Telegram
2. ✅ Mini App открывается через кнопку
3. ✅ Данные сохраняются в БД
4. ✅ Видишь бонусы после заказа

## 🚀 Что дальше?

### Дополни приложение:

1. **Платежи** — добавь интеграцию с Яндекс.Касса или Stripe
2. **Уведомления** — отправляй уведомления при новых заказах
3. **Аналитика** — отслеживай статистику заказов
4. **Подписка на канал** — обязательная подписка для использования

### Для пользователей:

1. **Деньги на вывод** — позволь переводить бонусы в реальные деньги
2. **История заказов** — показывай все прошлые заказы
3. **Рейтинги** — рейтинги авторов работ
4. **Живой чат** — поддержка в реальном времени

## 🆘 Если что-то сломалось

### Бот не запускается:
```bash
python -c "import aiogram; print('✅ aiogram installed')"
python -c "from config import BOT_TOKEN; print(f'✅ BOT_TOKEN: {BOT_TOKEN[:20]}...')"
```

### Сервер не запускается:
```bash
python -c "import fastapi; print('✅ fastapi installed')"
python server.py --reload
```

### БД не работает:
```bash
rm studprofy.db  # Удали старую БД
python -c "import asyncio; import database as db; asyncio.run(db.init_db())"
```

### Проверь логи:

**Логи бота:**
```bash
python bot.py 2>&1 | tee bot.log
```

**Логи сервера:**
```bash
python server.py 2>&1 | tee server.log
```

## 📚 Полезные ссылки

- [Aiogram документация](https://docs.aiogram.dev/)
- [FastAPI документация](https://fastapi.tiangolo.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram WebApp документация](https://core.telegram.org/bots/webapps)

## 💬 Контакт для поддержки

Если возникли проблемы:
1. Проверь консоль на ошибки
2. Посмотри в README.md
3. Создай Issue на GitHub

---

**Готово!** 🎉 Теперь у тебя есть полностью рабочее приложение!
