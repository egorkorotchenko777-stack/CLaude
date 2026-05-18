import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(","))) if os.getenv("ADMIN_IDS") else []

# Приложение
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://your-site.netlify.app")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")

# Бонусы
BONUS_FOR_SUBSCRIBE = 50
BONUS_FOR_OWN_ORDER = 100
BONUS_FOR_REFERRAL = 150
BONUS_FOR_REFERRAL_ORDER = 300

# База данных
DATABASE_FILE = os.getenv("DATABASE_FILE", "studprofy.db")

# Требуемый канал для подписки (если нужно)
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", "")
