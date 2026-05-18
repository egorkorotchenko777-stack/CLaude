"""
Telegram бот для СтудПрофи Mini App
Запускать: python bot.py
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import os
from dotenv import load_dotenv

load_dotenv()

import database as db
from config import BOT_TOKEN, MINI_APP_URL, ADMIN_IDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ===== FSM STATES =====
class OrderStates(StatesGroup):
    waiting_confirmation = State()

# ===== ГЛАВНОЕ МЕНЮ =====
def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎓 Открыть приложение",
            web_app=WebAppInfo(url=MINI_APP_URL)
        )],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    ])

# ===== КОМАНДЫ =====
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработка /start команды и реферальных ссылок"""
    args = message.text.split()
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""

    # Создаём/получаем пользователя
    user = await db.get_or_create_user(user_id, username, first_name)

    # Обработка реферальной ссылки
    if len(args) > 1:
        try:
            referrer_id = int(args[1])
            if referrer_id != user_id:
                # Проверяем, не добавлен ли уже этот реферал
                existing = await db.get_referrals_count(referrer_id)
                referrals = await db.get_referral_orders_count(referrer_id)

                await db.add_referral(referrer_id, user_id)
                await db.add_bonus(referrer_id, 150, "new_referral")

                logger.info(f"Новый реферал: {user_id} пригласил {referrer_id}")
        except ValueError:
            pass

    await message.answer(
        f"👋 Привет, <b>{first_name}!</b>\n\n"
        f"Добро пожаловать в <b>СтудПрофи</b> — сервис для заказа учебных работ! 🎓\n\n"
        f"<b>Что ты можешь делать:</b>\n"
        f"✅ Зарабатывать бонусы (★)\n"
        f"✅ Приглашать друзей и получать награды\n"
        f"✅ Оформлять заказы прямо в приложении\n"
        f"✅ Тратить бонусы на скидки\n\n"
        f"<b>Нажми кнопку ниже, чтобы открыть приложение!</b>",
        reply_markup=main_menu(),
        parse_mode=ParseMode.HTML
    )

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """Справка"""
    await message.answer(
        f"<b>❓ Помощь</b>\n\n"
        f"<b>Как заработать бонусы:</b>\n"
        f"1️⃣ <b>Приглась друга</b> — +150 ★\n"
        f"2️⃣ <b>Оформи заказ</b> — +100 ★\n"
        f"3️⃣ <b>Подписка на канал</b> — +50 ★\n"
        f"4️⃣ <b>Заказ друга</b> — +300 ★\n\n"
        f"<b>Как потратить:</b>\n"
        f"💸 <b>Скидка</b> — 1 ★ = 1₽\n"
        f"🎁 <b>Подарок</b> — 1000 ★\n\n"
        f"<b>Контакты:</b>\n"
        f"📧 Email: support@studprofy.com\n"
        f"💬 Telegram: @StudProfy",
        parse_mode=ParseMode.HTML
    )

@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Профиль пользователя"""
    user_id = message.from_user.id
    user = await db.get_user(user_id)

    if not user:
        await message.answer("❌ Пользователь не найден. Нажми /start")
        return

    referrals = await db.get_referrals_count(user_id)

    await message.answer(
        f"<b>👤 Твой профиль</b>\n\n"
        f"<b>ID:</b> {user_id}\n"
        f"<b>Бонусы:</b> {user['bonus_points']} ★\n"
        f"<b>Заказов:</b> {user['total_orders']}\n"
        f"<b>Рефералов:</b> {referrals}\n"
        f"<b>Присоединился:</b> {user['created_at'][:10]}",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu()
    )

# ===== CALLBACK ОБРАБОТЧИКИ =====
@router.callback_query(lambda c: c.data == "help")
async def handle_help(callback: types.CallbackQuery):
    await cmd_help(callback.message)
    await callback.answer()

@router.callback_query(lambda c: c.data == "profile")
async def handle_profile(callback: types.CallbackQuery):
    await cmd_profile(callback.message)
    await callback.answer()

# ===== ОБРАБОТКА СООБЩЕНИЙ =====
@router.message()
async def echo(message: types.Message):
    """Эхо для неизвестных команд"""
    await message.answer(
        "Я не понимаю эту команду. 😕\n\n"
        "Используй кнопки меню или введи:\n"
        "/start — главное меню\n"
        "/help — справка\n"
        "/profile — мой профиль",
        reply_markup=main_menu()
    )

# ===== ЗАПУСК БОТА =====
async def main():
    try:
        await db.init_db()
        logger.info("✅ База данных инициализирована")

        logger.info("🤖 Бот запускается...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
