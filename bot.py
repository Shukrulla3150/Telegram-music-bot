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

    if "http" in text:
        msg = bot.send_message(chat_id, "Video ishlov berilmoqda... ⏳")
        download_media(chat_id, text, msg.message_id)
    else:
        msg = bot.send_message(chat_id, "Musiqalar qidirilmoqda... ✨")
        search_music(chat_id, text, msg.message_id)

def download_media(chat_id, url, msg_id):
    ydl_opts = {'format': 'best', 'outtmpl': '%(title)s.%(ext)s', 'quiet': True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            with open(file_path, 'rb') as video:
                bot.send_video(chat_id, video, caption=f"Tayyor!")
            os.remove(file_path)
            bot.delete_message(chat_id, msg_id)
    except Exception:
        bot.edit_message_text("Yuklashda xato bo'ldi.", chat_id, msg_id)

def search_music(chat_id, query, msg_id):
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'default_search': 'ytsearch10', 'quiet': True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch10:{query}", download=False)['entries']
            for entry in results:
                try:
                    file_opts = {'format': 'bestaudio', 'outtmpl': '%(title)s.%(ext)s', 'quiet': True}
                    with YoutubeDL(file_opts) as ydl_down:
                        ydl_down.download([entry['webpage_url']])
                        f_name = ydl_down.prepare_filename(entry)
                        with open(f_name, 'rb') as audio:
                            bot.send_audio(chat_id, audio, title=entry.get('title'))
                        os.remove(f_name)
                except: continue
            bot.delete_message(chat_id, msg_id)
    except Exception:
        bot.edit_message_text("Qidiruvda xato bo'ldi.", chat_id, msg_id)

if __name__ == "__main__":
    print("Bot server uchun tayyor! 🚀")
    bot.polling(none_stop=True)
