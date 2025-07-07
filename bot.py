
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

TOKEN = '8187799175:AAFJ8QqVJrV7_qEgPQ6_cD3pxJ1IZF7xyY8'
bot = telebot.TeleBot(TOKEN)

# user_id ga asoslangan foydalanuvchilarni bog'lash
users = {}  # anonymous_user_id: original_user_id
conversations = {}  # original_user_id: anonymous_user_id

@bot.message_handler(commands=['start'])
def handle_start(message):
    args = message.text.split()
    user_id = message.from_user.id
    username = message.from_user.first_name or "Foydalanuvchi"

    if len(args) > 1:
        ref_id = int(args[1])
        if ref_id != user_id:
            # xabar yuborish original egasiga
            text = f"📩 Sizga anonim xabar yozishmoqchi.\nYozing!"
            users[user_id] = ref_id  # kimga yozmoqda
            conversations[ref_id] = user_id  # suhbat davom ettirish uchun

            bot.send_message(user_id, "✉️ Xabaringizni yozing, u anonim tarzda yuboriladi.")
            bot.send_message(ref_id, f"📨 Yangi anonim xabar keldi!", reply_markup=reply_button(user_id))

    # har doim shaxsiy havola yuboriladi
    link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    bot.send_message(user_id, f"👋 {username}, botga xush kelibsiz!\nSizning shaxsiy havolangiz:\n{link}")

def reply_button(reply_to_id):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("✏️ Javob yozish", callback_data=f"reply:{reply_to_id}")
    markup.add(button)
    return markup

@bot.message_handler(func=lambda m: m.from_user.id in users)
def forward_anonymous_message(message):
    anon_id = message.from_user.id
    original_id = users.get(anon_id)

    if original_id:
        bot.send_message(original_id, f"📩 Yangi anonim xabar:\n{message.text}", reply_markup=reply_button(anon_id))
        bot.send_message(anon_id, "✅ Xabaringiz yuborildi!")

@bot.callback_query_handler(func=lambda call: call.data.startswith("reply:"))
def handle_reply(call):
    from_user = call.from_user.id
    anon_id = int(call.data.split(":")[1])

    conversations[from_user] = anon_id
    bot.send_message(from_user, "✏️ Javobingizni yozing, u anonim tarzda yuboriladi.")
    bot.answer_callback_query(call.id, "Endi javob yozishingiz mumkin.")

@bot.message_handler(func=lambda m: m.from_user.id in conversations)
def handle_reply_message(message):
    from_user = message.from_user.id
    to_user = conversations.get(from_user)

    if to_user:
        bot.send_message(to_user, f"📨 Yangi anonim javob:\n{message.text}", reply_markup=reply_button(from_user))
        bot.send_message(from_user, "✅ Javobingiz yuborildi!")

bot.polling()
