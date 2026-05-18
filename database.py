import aiosqlite
import asyncio
from config import DATABASE_FILE
from datetime import datetime

async def init_db():
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                bonus_points INTEGER DEFAULT 0,
                total_orders INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                subscribed BOOLEAN DEFAULT 0
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (referrer_id) REFERENCES users(user_id),
                FOREIGN KEY (referred_id) REFERENCES users(user_id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                description TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        await db.execute('''
            CREATE TABLE IF NOT EXISTS bonus_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')

        await db.commit()

# ===== ПОЛЬЗОВАТЕЛИ =====
async def get_or_create_user(user_id: int, username: str = "", first_name: str = ""):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        user = await db.execute(
            'SELECT * FROM users WHERE user_id = ?',
            (user_id,)
        )
        user = await user.fetchone()

        if not user:
            await db.execute(
                'INSERT INTO users (user_id, username, first_name, bonus_points) VALUES (?, ?, ?, ?)',
                (user_id, username, first_name, 50)  # 50 бонусов при регистрации
            )
            await db.execute(
                'INSERT INTO bonus_transactions (user_id, amount, reason) VALUES (?, ?, ?)',
                (user_id, 50, 'welcome_bonus')
            )
            await db.commit()
            return await get_user(user_id)

        return user

async def get_user(user_id: int):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        db.row_factory = aiosqlite.Row
        user = await db.execute(
            'SELECT * FROM users WHERE user_id = ?',
            (user_id,)
        )
        return await user.fetchone()

# ===== БОНУСЫ =====
async def add_bonus(user_id: int, amount: int, reason: str):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute(
            'UPDATE users SET bonus_points = bonus_points + ? WHERE user_id = ?',
            (amount, user_id)
        )
        await db.execute(
            'INSERT INTO bonus_transactions (user_id, amount, reason) VALUES (?, ?, ?)',
            (user_id, amount, reason)
        )
        await db.commit()

async def spend_bonus(user_id: int, amount: int) -> bool:
    async with aiosqlite.connect(DATABASE_FILE) as db:
        user = await get_user(user_id)
        if not user or user['bonus_points'] < amount:
            return False

        await db.execute(
            'UPDATE users SET bonus_points = bonus_points - ? WHERE user_id = ?',
            (amount, user_id)
        )
        await db.execute(
            'INSERT INTO bonus_transactions (user_id, amount, reason) VALUES (?, ?, ?)',
            (user_id, -amount, 'spent')
        )
        await db.commit()
        return True

# ===== РЕФЕРАЛЫ =====
async def add_referral(referrer_id: int, referred_id: int):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        await db.execute(
            'INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)',
            (referrer_id, referred_id)
        )
        await db.commit()

async def get_referrals_count(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_FILE) as db:
        cursor = await db.execute(
            'SELECT COUNT(*) FROM referrals WHERE referrer_id = ?',
            (user_id,)
        )
        result = await cursor.fetchone()
        return result[0] if result else 0

async def get_referral_orders_count(user_id: int) -> int:
    async with aiosqlite.connect(DATABASE_FILE) as db:
        cursor = await db.execute(
            '''SELECT COUNT(*) FROM orders
               WHERE user_id IN (
                   SELECT referred_id FROM referrals WHERE referrer_id = ?
               ) AND status = 'confirmed'
            ''',
            (user_id,)
        )
        result = await cursor.fetchone()
        return result[0] if result else 0

# ===== ЗАКАЗЫ =====
async def create_order(user_id: int, description: str) -> int:
    async with aiosqlite.connect(DATABASE_FILE) as db:
        cursor = await db.execute(
            'INSERT INTO orders (user_id, description, status) VALUES (?, ?, ?)',
            (user_id, description, 'pending')
        )
        await db.execute(
            'UPDATE users SET total_orders = total_orders + 1 WHERE user_id = ?',
            (user_id,)
        )
        await db.commit()
        return cursor.lastrowid

async def get_orders(user_id: int = None):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        db.row_factory = aiosqlite.Row
        if user_id:
            cursor = await db.execute(
                'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,)
            )
        else:
            cursor = await db.execute(
                'SELECT * FROM orders ORDER BY created_at DESC'
            )
        return await cursor.fetchall()

async def confirm_order(order_id: int):
    async with aiosqlite.connect(DATABASE_FILE) as db:
        order = await db.execute(
            'SELECT user_id FROM orders WHERE order_id = ?',
            (order_id,)
        )
        order = await order.fetchone()
        if order:
            user_id = order[0]
            await db.execute(
                'UPDATE orders SET status = ? WHERE order_id = ?',
                ('confirmed', order_id)
            )
            await add_bonus(user_id, 100, 'order_confirmed')
            await db.commit()
