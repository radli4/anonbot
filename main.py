import telebot
import os
from flask import Flask, request

# Bot tokeningizni bu yerga joylang yoki Render Variables’dan oling
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "YOUR_BOT_TOKEN"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

# Oddiy buyruq handler (masalan: /start)
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Salom! Bot ishlayapti 🚀")

# Yana boshqa message handler'lar qo‘shishingiz mumkin
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Webhook so‘rovlarini qabul qiluvchi endpoint
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Foydalanuvchi brauzerdan kirsa ko‘rsatish uchun
@app.route('/', methods=['GET'])
def index():
    return "Bot server ishlayapti!", 200

# Flask ilovasini ishga tushurish
if __name__ == '__main__':
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
