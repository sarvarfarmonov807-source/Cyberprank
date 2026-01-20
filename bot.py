import asyncio
import logging
import json
import sqlite3
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# =====================
# BASIC CONFIG
# =====================
BOT_TOKEN = "7571428035:AAH4Yhe8q7ZCeqegnhC0gcyv-Jdb3O5gdNg"  # keyin ENV qilamiz
ADMIN_IDS = {7115743590}

# =====================
# FILES
# =====================
CONFIG_PATH = Path("config.json")
DB_PATH = Path("users.db")

# =====================
# LOGGING
# =====================
logging.basicConfig(level=logging.INFO)

# =====================
# DATABASE
# =====================
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_seen TEXT,
    last_active TEXT
)
""")
conn.commit()

def save_user(user: Message):
    now = datetime.utcnow().isoformat()
    cursor.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user.from_user.id,)
    )
    exists = cursor.fetchone()

    if exists:
        cursor.execute(
            "UPDATE users SET last_active = ?, username = ? WHERE user_id = ?",
            (now, user.from_user.username, user.from_user.id)
        )
    else:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (user.from_user.id, user.from_user.username, now, now)
        )
    conn.commit()

def get_stats():
    cursor.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]

    today = datetime.utcnow().date().isoformat()
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE last_active LIKE ?",
        (f"{today}%",)
    )
    today_active = cursor.fetchone()[0]

    return total, today_active

# =====================
# CONFIG JSON
# =====================
def load_config():
    if not CONFIG_PATH.exists():
        return {"video_quality": "480p", "mode": "test", "pranks_enabled": False}
    return json.load(open(CONFIG_PATH))

def save_config(data):
    json.dump(data, open(CONFIG_PATH, "w"), indent=2)

config = load_config()

# =====================
# BOT INIT
# =====================
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# =====================
# KEYBOARDS
# =====================
def main_menu(user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎭 Pranklar", callback_data="pranks")
    kb.button(text="ℹ️ Maʼlumot", callback_data="info")
    if user_id in ADMIN_IDS:
        kb.button(text="⚙️ Admin Panel", callback_data="admin")
    kb.adjust(2)
    return kb.as_markup()

def back_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Orqaga", callback_data="back")
    return kb.as_markup()

def admin_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Statistika", callback_data="stats")
    kb.button(text="🎛 Sozlamalar", callback_data="settings")
    kb.button(text="⬅️ Orqaga", callback_data="back")
    kb.adjust(1)
    return kb.as_markup()

# =====================
# HANDLERS
# =====================
@dp.message(CommandStart())
async def start_handler(message: Message):
    save_user(message)
    await message.answer(
        "👾 <b>CyberPrankUz</b>\n\n"
        "Ko‘ngilochar prank platforma.\n"
        "Hozircha test rejimida.\n\n"
        "Menyudan tanlang 👇",
        reply_markup=main_menu(message.from_user.id)
    )

@dp.message()
async def track_activity(message: Message):
    save_user(message)

@dp.callback_query(F.data == "admin")
async def admin_panel(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("Ruxsat yo‘q", show_alert=True)
        return
    await call.message.edit_text(
        "⚙️ <b>Admin Panel</b>",
        reply_markup=admin_menu()
    )

@dp.callback_query(F.data == "stats")
async def stats_handler(call: CallbackQuery):
    total, today = get_stats()
    await call.message.edit_text(
        "📊 <b>Statistika</b>\n\n"
        f"👤 Jami foydalanuvchilar: <b>{total}</b>\n"
        f"📅 Bugungi aktivlar: <b>{today}</b>",
        reply_markup=admin_menu()
    )

@dp.callback_query(F.data == "pranks")
async def pranks_handler(call: CallbackQuery):
    if not config["pranks_enabled"]:
        await call.answer("Pranklar hozircha o‘chirilgan", show_alert=True)
        return
    await call.message.edit_text(
        "🎭 Pranklar tez orada qo‘shiladi.",
        reply_markup=back_kb()
    )

@dp.callback_query(F.data == "info")
async def info_handler(call: CallbackQuery):
    await call.message.edit_text(
        "ℹ️ <b>CyberPrankUz</b>\n\n"
        "Barcha funksiyalar foydalanuvchi roziligi bilan ishlaydi.",
        reply_markup=back_kb()
    )

@dp.callback_query(F.data == "back")
async def back_handler(call: CallbackQuery):
    await call.message.edit_text(
        "👾 <b>CyberPrankUz</b>\n\n"
        "Menyudan tanlang 👇",
        reply_markup=main_menu(call.from_user.id)
    )

# =====================
# START
# =====================
async def main():
    print("🚀 CyberPrankUz statistika bilan ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
