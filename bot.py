import os
import telebot
from yt_dlp import YoutubeDL

# Bot tokeningiz
BOT_TOKEN = "7759868843:AAEnX1SjC6vG8_tG61L7rKIs_rYtWwL2u70"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Menga Instagram, YouTube yoki TikTok linkini yuboring (Video/Audio yuklayman) yoki musiqa nomini yozing (10 tagacha variant topaman). 🎵")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    chat_id = message.chat.id

    # Agar xabar link bo'lsa (Instagram, YT, TikTok)
    if "http" in text:
        msg = bot.send_message(chat_id, "Video ishlov berilmoqda... ⏳")
        download_media(chat_id, text, msg.message_id)
    # Agar xabar shunchaki matn bo'lsa (Musiqa qidirish)
    else:
        msg = bot.send
