"""
FastAPI сервер для Telegram Mini App
Запускать: python server.py
"""
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import hmac
import hashlib
import json
from urllib.parse import unquote
import os
from dotenv import load_dotenv

load_dotenv()

import database as db
from config import ADMIN_IDS, BOT_TOKEN

app = FastAPI(title="СтудПрофи API")

# CORS для Telegram WebApp
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== ПРОВЕРКА ПОДПИСИ TELEGRAM =====
def verify_telegram_data(init_data: str) -> dict | None:
    """Проверяет, что данные пришли от настоящего Telegram"""
    try:
        data = dict(item.split("=", 1) for item in unquote(init_data).split("&"))
        received_hash = data.pop("hash", None)
        if not received_hash:
            return None

        data_check = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
        secret = hmac.new("WebAppData".encode(), BOT_TOKEN.encode(), hashlib.sha256).digest()
        expected = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()

        if hmac.compare_digest(received_hash, expected):
            user_data = json.loads(data.get("user", "{}"))
            return user_data
        return None
    except Exception:
        return None

# ===== МОДЕЛИ =====
class SpendRequest(BaseModel):
    user_id: int
    amount: int
    reason: str

class OrderRequest(BaseModel):
    user_id: int
    type: str
    topic: str
    uni: str
    deadline: str = ""
    extra: str = ""

# ===== РОУТЫ =====

@app.get("/api/user/{user_id}")
async def get_user_data(user_id: int, x_telegram_init_data: str = Header(default="")):
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    referrals = await db.get_referrals_count(user_id)
    referral_orders = await db.get_referral_orders_count(user_id)

    return {
        "balance": user["bonus_points"],
        "referrals": referrals,
        "orders": user["total_orders"],
        "saved": referral_orders * 300 + referrals * 150,
        "refLink": f"https://t.me/StudProfyBot?start={user_id}"
    }

@app.post("/api/spend")
async def spend_bonuses(req: SpendRequest, x_telegram_init_data: str = Header(default="")):
    success = await db.spend_bonus(req.user_id, req.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Недостаточно бонусов")
    return {"ok": True}

@app.post("/api/order")
async def create_order(req: OrderRequest, x_telegram_init_data: str = Header(default="")):
    description = (
        f"Тип: {req.type}\n"
        f"Тема: {req.topic}\n"
        f"Учебное заведение: {req.uni}\n"
        f"Дедлайн: {req.deadline}\n"
        f"Доп. требования: {req.extra}"
    )
    order_id = await db.create_order(req.user_id, description)
    await db.add_bonus(req.user_id, 100, "order_created")
    return {"ok": True, "order_id": order_id}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import asyncio
    asyncio.run(db.init_db())
    uvicorn.run(app, host="0.0.0.0", port=8000)
