import random
import datetime
import json
import matplotlib.pyplot as plt
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from io import BytesIO

# Foydalanuvchi ma'lumotlarini saqlash va olish
USER_DATA_FILE = "user_data.json"

# Webhookni o'chirish uchun yordamchi funksiya
async def remove_webhook(application: Application):
    await application.bot.delete_webhook()
    
# Tanbeh, Maqtov va Motivatsiya so'zlari
REBELLIOUS_PHRASES = [
    "Haqoratli tanbeh 1", "Haqoratli tanbeh 2", "Haqoratli tanbeh 3", 
    "Bu qanday odatsizlik?!", "Haqoratli tanbeh 4"
]
PRAISE_PHRASES = [
    "Ajoyib, buni davom ettir!", "Ajoyib, sen mustahkamsan!", 
    "Bugun juda yaxshi kunni o‘tkazding!", "Tabriklayman, yana bir kun muvaffaqiyat!",
    "Chekmaslikda davom et!"
]
MOTIVATIONAL_PHRASES = [
    "Har bir yangi kun sening yutug‘ing!", "Har bir kichik qadam katta yutuqlarga olib keladi!",
    "O‘z maqsadingga qadam qo‘y!", "Sabr va qat’iyat bilan sen ham muvaffaqiyatga erishasan!"
]

# Foydalanuvchi ma'lumotlari va statistikasi
def save_user_data(user_id, username):
    data = {
        "user_id": user_id,
        "username": username,
        "smoked_days": 0,
        "praises": [],
        "reprimands": [],
        "motivational_notes": [],
        "daily_reasons": [],
        "weekly_report": [],
        "monthly_report": [],
        "yearly_report": {}
    }
    with open(USER_DATA_FILE, "a") as file:
        json.dump(data, file)
        file.write("\n")

def get_user_data(user_id):
    with open(USER_DATA_FILE, "r") as file:
        for line in file.readlines():
            data = json.loads(line)
            if data["user_id"] == user_id:
                return data
    return None

def update_user_data(user_id, data_to_update):
    with open(USER_DATA_FILE, "r") as file:
        lines = file.readlines()
    
    with open(USER_DATA_FILE, "w") as file:
        for line in lines:
            data = json.loads(line)
            if data["user_id"] == user_id:
                data.update(data_to_update)
            json.dump(data, file)
            file.write("\n")

# Bot uchun funksiya: start
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    user_data = get_user_data(user_id)
    if not user_data:
        save_user_data(user_id, username)
    update.message.reply_text(f"Salom {username}, bu bot sizni chekishdan qutqarish uchun yordam beradi!")

# Statistikani yuborish
def show_statistics(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        smoked_days = user_data["smoked_days"]
        praises = ", ".join(user_data["praises"]) if user_data["praises"] else "Hech narsa"
        reprimands = ", ".join(user_data["reprimands"]) if user_data["reprimands"] else "Hech narsa"
        update.message.reply_text(f"Bugungi statistikangiz:\nChekishlar soni: {smoked_days}\n"
                                  f"Ma'qullashlar: {praises}\nTanbehlar: {reprimands}")
    else:
        update.message.reply_text("Sizning ma'lumotlaringiz mavjud emas!")

# Motivatsiya yuborish
def send_motivational_message(update: Update, context: CallbackContext) -> None:
    motivation = random.choice(MOTIVATIONAL_PHRASES)
    update.message.reply_text(motivation)

# Tanbeh yuborish
def send_reprimand(update: Update, context: CallbackContext) -> None:
    reprimand = random.choice(REBELLIOUS_PHRASES)
    update.message.reply_text(reprimand)

# Maqtov yuborish
def send_praise(update: Update, context: CallbackContext) -> None:
    praise = random.choice(PRAISE_PHRASES)
    update.message.reply_text(praise)

# Yillik hisobot
def show_yearly_report(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        update.message.reply_text("Yillik hisobotni ko‘rish uchun, iltimos, oyning raqamini kiriting.")
    else:
        update.message.reply_text("Sizning ma'lumotlaringiz mavjud emas!")

# Oylik hisobotni ko‘rish
def show_monthly_report(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        update.message.reply_text("Oylik hisobotni ko‘rish uchun, iltimos, oy nomini tanlang.")
    else:
        update.message.reply_text("Sizning ma'lumotlaringiz mavjud emas!")

# Kunlik sabablarga oid so'rov
def ask_for_reason(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Bugun chekishning sababi nima? (stress, zerikish, atrof muhit, odat)")

# Kunlik sabablarga oid javobni saqlash
def save_reason(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    reason = update.message.text
    user_data = get_user_data(user_id)
    if user_data:
        user_data["daily_reasons"].append(reason)
        update_user_data(user_id, {"daily_reasons": user_data["daily_reasons"]})
    update.message.reply_text(f"Sizning sababingiz saqlandi: {reason}")

# Haftalik sharh
def send_weekly_report(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        weekly_report = user_data["weekly_report"]
        best_day = max(weekly_report, key=lambda x: x['smoked_count'])  # Eng yaxshi kunni topish
        worst_day = min(weekly_report, key=lambda x: x['smoked_count'])  # Eng yomon kunni topish
        update.message.reply_text(f"Haftalik sharh:\nEng yaxshi kun: {best_day}\nEng yomon kun: {worst_day}")
    else:
        update.message.reply_text("Sizning ma'lumotlaringiz mavjud emas!")

# Grafikalar yuborish
def send_graphics(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)
    if user_data:
        smoked_days = user_data["smoked_days"]
        dates = [str(datetime.date.today() - datetime.timedelta(days=i)) for i in range(smoked_days)]
        values = [random.randint(1, 5) for _ in range(smoked_days)]  # Har kun uchun tasodifiy qiymatlar
        plt.plot(dates, values, marker='o')
        plt.title("Chekish statistikasi")
        plt.xlabel("Kunlar")
        plt.ylabel("Chekish miqdori")
        
        # Rasmni yuborish
        buf = BytesIO()
        plt.savefig(buf, format='PNG')
        buf.seek(0)
        update.message.reply_photo(photo=buf)
    else:
        update.message.reply_text("Sizning ma'lumotlaringiz mavjud emas!")

# Botni ishga tushirish
def main():
    updater = Updater("7576175283:AAGMBGTjsGn--uIsXaSb2re7Tz6xnJ1vUxs")
    dispatcher = updater.dispatcher

    # Komandalar
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("statistika", show_statistics))
    dispatcher.add_handler(CommandHandler("motivatsiya", send_motivational_message))
    dispatcher.add_handler(CommandHandler("tanbeh", send_reprimand))
    dispatcher.add_handler(CommandHandler("maqtov", send_praise))
    dispatcher.add_handler(CommandHandler("yillik_hisobot", show_yearly_report))
    dispatcher.add_handler(CommandHandler("oylik_hisobot", show_monthly_report))
    dispatcher.add_handler(CommandHandler("haftalik_sharh", send_weekly_report))
    dispatcher.add_handler(CommandHandler("grafikalar", send_graphics))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save_reason))
    
    # Pollingni boshlash
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
