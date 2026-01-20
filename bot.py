import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# =====================
# CONFIG
# =====================
BOT_TOKEN = "7571428035:AAGZZpcS_z_xCgmf-9nB02m-EgnuyMGVxuI"
ADMIN_IDS = {7115743590}  # admin telegram ID lar (raqam)

# =====================
# LOGGING
# =====================
logging.basicConfig(level=logging.INFO)

# =====================
# BOT INIT
# =====================
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# =====================
# KEYBOARDS
# =====================
def main_menu(user_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎭 Pranklar", callback_data="pranks")
    kb.button(text="ℹ️ Maʼlumot", callback_data="info")
    if user_id in ADMIN_IDS:
        kb.button(text="⚙️ Admin Panel", callback_data="admin")
    kb.adjust(2)
    return kb.as_markup()

def back_button():
    kb = InlineKeyboardBuilder()
    kb.button(text="⬅️ Orqaga", callback_data="back")
    return kb.as_markup()

def admin_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="📊 Bot holati", callback_data="status")
    kb.button(text="⬅️ Orqaga", callback_data="back")
    kb.adjust(1)
    return kb.as_markup()

# =====================
# HANDLERS
# =====================
@dp.message(CommandStart())
async def start_handler(message: Message):
    text = (
        "👾 <b>CyberPrankUz</b>\n\n"
        "Ko‘ngilochar prank platforma.\n"
        "Hozircha test rejimida ishlayapti.\n\n"
        "Pastdagi menyudan tanlang 👇"
    )
    await message.answer(text, reply_markup=main_menu(message.from_user.id))


@dp.callback_query(F.data == "pranks")
async def pranks_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "🎭 <b>Pranklar</b>\n\n"
        "Hozircha pranklar yo‘q.\n"
        "Tez orada qo‘shiladi 👨‍💻",
        reply_markup=back_button()
    )


@dp.callback_query(F.data == "info")
async def info_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "ℹ️ <b>CyberPrankUz haqida</b>\n\n"
        "• Pranklar foydalanuvchi roziligi bilan ishlaydi\n"
        "• Video / audio / effektlar (keyin)\n"
        "• Test rejimi\n\n"
        "Muammo yoki takliflar bo‘lsa admin bilan bog‘laning.",
        reply_markup=back_button()
    )


@dp.callback_query(F.data == "admin")
async def admin_handler(call: CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("Ruxsat yo‘q", show_alert=True)
        return
    await call.answer()
    await call.message.edit_text(
        "⚙️ <b>Admin Panel</b>",
        reply_markup=admin_menu()
    )


@dp.callback_query(F.data == "status")
async def status_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "📊 <b>Bot holati</b>\n\n"
        "✅ Bot ishlayapti\n"
        "🧪 Rejim: Test\n"
        "🎭 Pranklar: 0",
        reply_markup=admin_menu()
    )


@dp.callback_query(F.data == "back")
async def back_handler(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "👾 <b>CyberPrankUz</b>\n\n"
        "Pastdagi menyudan tanlang 👇",
        reply_markup=main_menu(call.from_user.id)
    )

# =====================
# START
# =====================
async def main():
    print("🚀 CyberPrankUz (aiogram 3) ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
