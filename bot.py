import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# =====================
# CONFIG
# =====================
BOT_TOKEN = "7571428035:AAGZZpcS_z_xCgmf-9nB02m-EgnuyMGVxuI"
ADMIN_IDS = [7115743590]  # admin telegram ID lar (raqam)

# =====================
# LOGGING
# =====================
logging.basicConfig(level=logging.INFO)

# =====================
# BOT INIT
# =====================
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# =====================
# KEYBOARDS
# =====================
def main_menu(user_id: int):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🎭 Pranklar", callback_data="pranks"),
        InlineKeyboardButton("ℹ️ Maʼlumot", callback_data="info"),
    )
    if user_id in ADMIN_IDS:
        kb.add(InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin"))
    return kb

def admin_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("📊 Bot holati", callback_data="status"),
        InlineKeyboardButton("⬅️ Orqaga", callback_data="back"),
    )
    return kb

# =====================
# HANDLERS
# =====================
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    text = (
        "👾 <b>CyberPrankUz</b>\n\n"
        "Bu bot ko‘ngilochar prank platforma.\n"
        "Hozircha test rejimida ishlayapti.\n\n"
        "Pastdagi menyudan tanlang 👇"
    )
    await message.answer(text, reply_markup=main_menu(message.from_user.id), parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == "pranks")
async def pranks_handler(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "🎭 <b>Pranklar</b>\n\n"
        "Hozircha pranklar yo‘q.\n"
        "Tez orada qo‘shiladi 👨‍💻",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("⬅️ Orqaga", callback_data="back")
        ),
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data == "info")
async def info_handler(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "ℹ️ <b>CyberPrankUz haqida</b>\n\n"
        "• Pranklar foydalanuvchi roziligi bilan ishlaydi\n"
        "• Video / audio / effektlar (keyin)\n"
        "• Test rejimi\n\n"
        "Muammo yoki takliflar bo‘lsa admin bilan bog‘laning.",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("⬅️ Orqaga", callback_data="back")
        ),
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data == "admin")
async def admin_handler(call: types.CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("Ruxsat yo‘q", show_alert=True)
        return
    await call.answer()
    await call.message.edit_text(
        "⚙️ <b>Admin Panel</b>",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data == "status")
async def status_handler(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "📊 <b>Bot holati</b>\n\n"
        "✅ Bot ishlayapti\n"
        "🧪 Rejim: Test\n"
        "🎭 Pranklar: 0",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

@dp.callback_query_handler(lambda c: c.data == "back")
async def back_handler(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "👾 <b>CyberPrankUz</b>\n\n"
        "Pastdagi menyudan tanlang 👇",
        reply_markup=main_menu(call.from_user.id),
        parse_mode="HTML"
    )

# =====================
# START
# =====================
if __name__ == "__main__":
    print("🚀 CyberPrankUz bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
