import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "SIZNING_BOT_TOKENINGIZ"
ADMIN_ID = 123456789  # O'z Telegram ID raqamingizni yozing

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchilar harakatlarini saqlash uchun bazacha (xotirada)
USER_LOGS = []

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    # Foydalanuvchi ma'lumotlarini qayd etish
    user_info = {
        "id": message.from_user.id,
        "name": message.from_user.full_name,
        "username": message.from_user.username or "Mavjud emas",
        "time": message.date.strftime("%Y-%m-%d %H:%M:%S")
    }
    USER_LOGS.append(user_info)

    # Mini App ochish tugmasi
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🚀 RealSync Mini App'ni Ochish",
        web_app=types.WebAppInfo(url="https://SIZNING-RENDER-HAVOLANGIZ.onrender.com")
    )
    
    # Admin panel tugmasi (faqat sizga ko'rinadi)
    if message.from_user.id == ADMIN_ID:
        builder.row(types.InlineKeyboardButton(text="🛠 Admin Panel (Kuzatuv)", callback_data="admin_panel"))

    builder.adjust(1)

    await message.answer(
        f"Salom, {message.from_user.first_name}!\n"
        "✨ **RealSync** olamiga xush kelibsiz.\n"
        "Quyidagi tugma orqali mukammal dizaynli ilovamizga kiring:",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "admin_panel")
async def admin_panel_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Bu bo'lim faqat admin uchun!", show_alert=True)
        return

    log_text = "📊 **Oxirgi kirgan foydalanuvchilar va harakatlar:**\n\n"
    if not USER_LOGS:
        log_text += "Hozircha hech kim kirmadi."
    else:
        for log in USER_LOGS[-10:]: # Oxirgi 10 tasi
            log_text += f"👤 {log['name']} (@{log['username']})\n⏰ Vaqt: {log['time']}\n-------------------\n"

    await callback.message.edit_text(log_text, parse_mode="Markdown")
    await callback.answer()

if __name__ == "__main__":
    import asyncio
    logging.basicConfig(level=logging.INFO)
    print("Bot va Admin Panel ishga tushdi...")
    asyncio.run(dp.start_polling(bot))
