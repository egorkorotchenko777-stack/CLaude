"""
Админ команды для управления заказами
Добавь это в bot.py для админов
"""
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
import database as db
from config import ADMIN_IDS

admin_router = Router()

@admin_router.message(Command("orders"))
async def cmd_orders(message: Message):
    """Список всех неподтвержденных заказов"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Доступ только для администраторов")
        return

    orders = await db.get_orders()
    pending = [o for o in orders if o['status'] == 'pending']

    if not pending:
        await message.answer("✅ Нет новых заказов")
        return

    text = "<b>📦 Новые заказы:</b>\n\n"
    for order in pending[:10]:  # Показываем последние 10
        text += f"<b>ID:</b> {order['order_id']}\n"
        text += f"<b>Пользователь:</b> {order['user_id']}\n"
        text += f"<b>Описание:</b>\n{order['description']}\n"
        text += f"<b>Дата:</b> {order['created_at'][:10]}\n"
        text += f"<b>Статус:</b> {order['status']}\n"
        text += "─" * 30 + "\n\n"

    await message.answer(text, parse_mode="HTML")

@admin_router.message(Command("confirm"))
async def cmd_confirm(message: Message):
    """Подтвердить заказ (аргумент: ID заказа)
    Пример: /confirm 5
    """
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Доступ только для администраторов")
        return

    args = message.text.split()
    if len(args) < 2:
        await message.answer("❌ Использование: /confirm <order_id>")
        return

    try:
        order_id = int(args[1])
        await db.confirm_order(order_id)
        await message.answer(f"✅ Заказ #{order_id} подтверждён! Пользователь получит +100 бонусов")
    except (ValueError, Exception) as e:
        await message.answer(f"❌ Ошибка: {e}")

@admin_router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Статистика пользователей"""
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Доступ только для администраторов")
        return

    # Получаем статистику из БД
    orders = await db.get_orders()
    total_orders = len(orders)
    confirmed = len([o for o in orders if o['status'] == 'confirmed'])
    pending = len([o for o in orders if o['status'] == 'pending'])

    text = (
        f"<b>📊 Статистика:</b>\n\n"
        f"📦 Всего заказов: {total_orders}\n"
        f"✅ Подтверждённых: {confirmed}\n"
        f"⏳ В обработке: {pending}\n"
    )

    await message.answer(text, parse_mode="HTML")

@admin_router.message(Command("bonus"))
async def cmd_add_bonus(message: Message):
    """Добавить бонусы пользователю
    Использование: /bonus <user_id> <amount> <reason>
    Пример: /bonus 123456789 500 manual_bonus
    """
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Доступ только для администраторов")
        return

    args = message.text.split(maxsplit=3)
    if len(args) < 3:
        await message.answer("❌ Использование: /bonus <user_id> <amount> <reason>")
        return

    try:
        user_id = int(args[1])
        amount = int(args[2])
        reason = args[3] if len(args) > 3 else "manual"

        await db.add_bonus(user_id, amount, reason)
        await message.answer(f"✅ Пользователю {user_id} добавлено {amount} ★\nПричина: {reason}")
    except ValueError:
        await message.answer("❌ Ошибка: неверный формат")
