import os
import requests
from flask import Flask
from threading import Thread
import telebot

# --- 1. RENDER PORT SAKLASH (FLASK) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot faol ishlamoqda!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# --- 2. BOT SOZLAMALARI ---
# Tirnoq ichiga o'zingizning Telegram Bot Tokeningizni qo'ying:
BOT_TOKEN = "8748781038:AAF87OHUwcPRszbSZ4Hl7CcDe_SXSddQUlc"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! Qo'shiq nomini yoki ijrochini yozib yuboring 🎶")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    query = message.text
    msg = bot.reply_to(message, f"🔍 '{query}' bo'yicha izlanmoqda...")
    
    try:
        # Invidious API orqali qidiruv (YouTube blokirovkasini aylanib o'tadi)
        api_url = f"https://api.invidious.io/instances_list"
        instances = requests.get(api_url, timeout=5).json()
        
        # Ochiq serverlardan birini tanlash
        working_instance = "https://invidious.nerdvpn.de"
        search_url = f"{working_instance}/api/v1/search?q={query}&type=video"
        
        response = requests.get(search_url, timeout=10).json()
        
        if not response or len(response) == 0:
            bot.edit_message_text(f"❌ '{query}' bo'yicha hech qanday musiqa topilmadi.", chat_id=message.chat.id, message_id=msg.message_id)
            return

        first_result = response[0]
        title = first_result.get('title', 'Musiqa')
        video_id = first_result.get('videoId')
        
        # Invidious orqali biriktirilgan audio havola
        audio_url = f"{working_instance}/latest_version?id={video_id}&italic=true"
        
        bot.delete_message(message.chat.id, msg.message_id)
        bot.send_audio(
            chat_id=message.chat.id,
            audio=audio_url,
            title=title,
            performer="YouTube Music",
            caption=f"🎵 **{title}**\n\n🤖 @{bot.get_me().username} orqali yuklab olindi."
        )

    except Exception as e:
        bot.edit_message_text(f"❌ Musiqa yuklashda xatolik yuz berdi. Qaytadan urinib ko'ring.", chat_id=message.chat.id, message_id=msg.message_id)

if __name__ == '__main__':
    bot.infinity_polling()
