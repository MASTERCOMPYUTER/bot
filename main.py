import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import asyncio
import random
from datetime import datetime

# Tokenni shu yerga yozing
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Logging
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

motivational_messages = [
    "💪 Siz kuchlisiz. Har bir chekilmagan sigaret bu yutuqdir.",
    "🌿 Bugun chekmagan har bir daqiqa – sog‘lom nafasdir.",
    "🧘‍♂️ Sabrli bo‘ling, siz bunga qodirsiz.",
    "❤️ Sog‘lig‘ingiz sizga rahmat aytadi.",
    "🚫 Sigaret – bu muammo emas, uni tashlashga harakat qilmaslik muammo.",
    "👨‍👩‍👧‍👦 Oila, do‘stlar va o‘zingiz uchun kurashing.",
    "🔥 Har kuni yangi imkoniyat. Bugun sigareta yo‘q!",
    "🎯 Chekish – odat. Uni yengish – jasorat!",
    "🔒 Har bir bardoshli daqiqa – bu g‘alaba.",
    "🕊️ Erkin nafas olish uchun kurashing."
]

tanbeh_messages = [
    "🚭 Nega yana chekdingiz? O‘z sog‘lig‘ingizni o‘ylang!",
    "😔 Bu harakat sizni orqaga tortadi. Yana urinib ko‘ring.",
    "🛑 Har bir sigaret sizni sog‘lig‘ingizdan uzoqlashtiradi.",
    "📉 Yana bir orqaga qadam. Ammo taslim bo‘lmang.",
    "😡 Siz bundan yaxshiroqsiz. O‘zingizga ishonchingizni yo‘qotmang."
]

reward_messages = [
    "🎉 Ajoyib! Bugun chekmadingiz, davom eting!",
    "🏆 Siz kuchli odamsiz. Bugun g‘alaba siz bilan!",
    "💥 Sizda iroda bor. Har kuni g‘alaba!",
    "🧠 Aql bilan harakat qilish – bu sizning uslubingiz!",
    "🎁 Har bir bardoshli daqiqa – bu sizga sovg‘a!"
]

user_achievement = {}
user_smoke_count = {}
user_history = {}

# Start komandasi
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    chat_id = message.chat.id
    user_achievement[chat_id] = 0
    user_smoke_count[chat_id] = 0
    user_history[chat_id] = []

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅ Bugun chekmadim", callback_data="not_smoked")],
        [InlineKeyboardButton("🚬 Chekdim", callback_data="smoked")],
        [InlineKeyboardButton("📅 Tarixim", callback_data="history")],
        [InlineKeyboardButton("📊 Hisobot", callback_data="report")]
    ])

    await message.answer("Assalomu alaykum! Men sizga sigaretni tashlashda yordam beradigan motivatsion botman.", reply_markup=keyboard)

# Tugmalar uchun ishlovchi
@dp.callback_query_handler(lambda c: c.data in ["not_smoked", "smoked", "history", "report"])
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    chat_id = callback_query.from_user.id

    if data == "not_smoked":
        user_achievement[chat_id] = user_achievement.get(chat_id, 0) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in user_history.get(chat_id, []):
            user_history[chat_id].append(today)
        msg = random.choice(reward_messages)
        await bot.send_message(chat_id, f"✅ Juda yaxshi! {msg}")

    elif data == "smoked":
        user_smoke_count[chat_id] = user_smoke_count.get(chat_id, 0) + 1
        count = user_smoke_count[chat_id]
        baho = max(1, 5 - count)
        tanbeh = random.choice(tanbeh_messages)
        await bot.send_message(chat_id, f"🚬 Siz bugun {count} marta chekdingiz. Baho: {baho}/5\n{tanbeh}")

    elif data == "history":
        history = user_history.get(chat_id, [])
        if history:
            text = "📅 Siz chekmagan kunlar:\n" + "\n".join(history)
        else:
            text = "🚫 Hozircha tarix yo‘q."
        await bot.send_message(chat_id, text)

    elif data == "report":
        count = user_achievement.get(chat_id, 0)
        smoked = user_smoke_count.get(chat_id, 0)
        await bot.send_message(chat_id, f"📊 Siz hozirgacha {count} marta sigareta chekmadingiz, {smoked} marta chekdingiz. Harakatda davom eting!")

# Doimiy motivatsiya yuborish
async def periodic_sender():
    while True:
        for chat_id in user_achievement:
            msg = random.choice(motivational_messages)
            try:
                await bot.send_message(chat_id, msg)
            except Exception as e:
                logging.warning(f"Xabar yuborishda xatolik: {e}")
        await asyncio.sleep(3600)  # Har 1 soatda

async def on_startup(_):
    asyncio.create_task(periodic_sender())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
