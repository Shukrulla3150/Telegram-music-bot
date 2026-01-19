import os
import telebot
from yt_dlp import YoutubeDL

# O'z bot tokeningizni qo'ying
BOT_TOKEN = "8584554183:AAEi8LPqEKSXw_pEfYUg8FBmr1NEl8wEb2Y"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Musiqa nomini yozing yoki link yuboring. 🎵")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Qidirilmoqda... 📥")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'default_search': 'ytsearch',
        'quiet': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}" if "http" not in query else query, download=True)
            if 'entries' in info:
                info = info['entries'][0]
            
            file_name = ydl.prepare_filename(info)
            
            with open(file_name, 'rb') as audio:
                bot.send_audio(chat_id, audio, title=info.get('title'))
            
            os.remove(file_name)
            bot.delete_message(chat_id, msg.message_id)
    except Exception:
        bot.edit_message_text("Xato yuz berdi, qaytadan urinib ko'ring.", chat_id, msg.message_id)

if name == "main":
    print("Bot server uchun tayyor! 🚀")
    bot.polling(none_stop=True)
