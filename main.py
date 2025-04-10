import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
import asyncio
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

motivational_messages = [
    # 40+ motivatsion gaplar
    "💪 Siz kuchlisiz. Har bir chekilmagan sigaret bu yutuqdir.",
    "🌿 Bugun chekmagan har bir daqiqa – sog‘lom nafasdir.",
    "🧘‍♂️ Sabrli bo‘ling, siz bunga qodirsiz.",
    "❤️ Sog‘lig‘ingiz sizga rahmat aytadi.",
    "🚫 Sigaret – bu muammo emas, uni tashlashga harakat qilmaslik muammo.",
    "👨‍👩‍👧‍👦 Oila, do‘stlar va o‘zingiz uchun kurashing.",
    "🔥 Har kuni yangi imkoniyat. Bugun sigareta yo‘q!",
    "🎯 Chekish – odat. Uni yengish – jasorat!",
    "🔒 Har bir bardoshli daqiqa – bu g‘alaba.",
    "🕊️ Erkin nafas olish uchun kurashing.",
    "🚀 Har bir chekmaslik qarori – bu oldinga qadam.",
    "⏳ Sabrli bo‘ling – natijalar vaqt bilan keladi.",
    "🙌 Har kuni o‘zingizni g‘alaba uchun tabriklang.",
    "🎈 Chekilmagan sigaret – bu toza havo demakdir.",
    "🧭 To‘g‘ri yo‘ldasiz. Davom eting!",
    "💼 Sog‘lom hayot – bu eng yaxshi investitsiya.",
    "🌈 Yangi tong – yangi imkoniyat!",
    "🌟 Siz boshqacha bo‘lishni tanladingiz – bu qahramonlikdir.",
    "📆 Bugun – yangi tarix boshlanishi.",
    "🎶 Nafasingiz musiqadek bo‘lsin – toza va hayotbaxsh."
] * 2  # 40 dona bo'lishi uchun 20 ta 2 marta takrorlanmoqda

tanbeh_messages = [
    # 40 tanbeh
    "🚭 Nega yana chekdingiz? O‘z sog‘lig‘ingizni o‘ylang!",
    "😔 Bu harakat sizni orqaga tortadi. Yana urinib ko‘ring.",
    "🛑 Har bir sigaret sizni sog‘lig‘ingizdan uzoqlashtiradi.",
    "📉 Yana bir orqaga qadam. Ammo taslim bo‘lmang.",
    "😡 Siz bundan yaxshiroqsiz. O‘zingizga ishonchingizni yo‘qotmang.",
] * 8

reward_messages = [
    # 40 mukofotli gaplar
    "🎉 Ajoyib! Bugun chekmadingiz, davom eting!",
    "🏆 Siz kuchli odamsiz. Bugun g‘alaba siz bilan!",
    "💥 Sizda iroda bor. Har kuni g‘alaba!",
    "🧠 Aql bilan harakat qilish – bu sizning uslubingiz!",
    "🎁 Har bir bardoshli daqiqa – bu sizga sovg‘a!"
] * 8

user_custom_messages = {}
user_achievement = {}
user_smoke_count = {}
user_history = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_custom_messages[chat_id] = []
    user_achievement[chat_id] = 0
    user_smoke_count[chat_id] = 0
    user_history[chat_id] = []

    keyboard = [
        [InlineKeyboardButton("➕ Vaqt qo‘shish", callback_data='addtime')],
        [InlineKeyboardButton("📝 Eslatma qo‘shish", callback_data='addnote')],
        [InlineKeyboardButton("✅ Bugun chekmadim", callback_data='not_smoked')],
        [InlineKeyboardButton("🚬 Chekdim", callback_data='smoked')],
        [InlineKeyboardButton("📅 Tarixim", callback_data='history')],
        [InlineKeyboardButton("📊 Hisobot", callback_data='report')],
        [InlineKeyboardButton("🛑 To‘xtatish", callback_data='stop')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Assalomu alaykum! Men sizga sigaretni tashlashda yordam beradigan motivatsion botman.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data == 'addtime':
        await query.message.reply_text("⏰ Iltimos, vaqtni /addtime HH:MM shaklida yozing.")
    elif query.data == 'addnote':
        await query.message.reply_text("📝 Iltimos, eslatma matnini yozing. /addnote Men kuchliman!")
    elif query.data == 'not_smoked':
        user_achievement[chat_id] = user_achievement.get(chat_id, 0) + 1
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in user_history.get(chat_id, []):
            user_history[chat_id].append(today)
        msg = random.choice(reward_messages)
        await query.message.reply_text(f"✅ Juda yaxshi! {msg}")
    elif query.data == 'smoked':
        user_smoke_count[chat_id] = user_smoke_count.get(chat_id, 0) + 1
        count = user_smoke_count[chat_id]
        baho = max(1, 5 - count)
        msg = random.choice(tanbeh_messages)
        await query.message.reply_text(f"🚬 Bugun {count} marta chekdingiz. Baho: {baho}/5\n{msg}")
    elif query.data == 'history':
        history = user_history.get(chat_id, [])
        msg = "📅 Siz chekmagan kunlar:\n" + "\n".join(history) if history else "🚫 Hozircha tarix yo‘q."
        await query.message.reply_text(msg)
    elif query.data == 'report':
        await query.message.reply_text(
            f"📊 Chekmaslik: {user_achievement.get(chat_id, 0)} marta.\nChekish: {user_smoke_count.get(chat_id, 0)} marta."
        )
    elif query.data == 'stop':
        await query.message.reply_text("🛑 Bot to‘xtatildi.")

async def addtime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Vaqt saqlanmadi (demo).")

async def addnote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    note = ' '.join(context.args)
    if chat_id not in user_custom_messages:
        user_custom_messages[chat_id] = []
    if note:
        user_custom_messages[chat_id].append(note)
        await update.message.reply_text("✅ Eslatma saqlandi!")
    else:
        await update.message.reply_text("❗ Iltimos, eslatma matnini yozing.")

async def periodic_sender(app):
    while True:
        for chat_id in user_custom_messages:
            messages = motivational_messages + user_custom_messages[chat_id]
            msg = random.choice(messages)
            try:
                await app.bot.send_message(chat_id=chat_id, text=msg)
            except Exception as e:
                logging.warning(f"Xatolik: {e}")
        await asyncio.sleep(random.randint(30, 90) * 60)

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CommandHandler("addtime", addtime))
    app.add_handler(CommandHandler("addnote", addnote))

    asyncio.create_task(periodic_sender(app))
    await app.run_polling()

if __name__ == '__main__':
    import sys
    if sys.platform.startswith('win') and sys.version_info >= (3, 8):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(main())
    else:
        loop.run_until_complete(main())
