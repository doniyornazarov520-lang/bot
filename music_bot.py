import os
from flask import Flask
from threading import Thread
import telebot

# --- RENDER PORT SAKLASH ---
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

# --- BOT SOZLAMALARI ---
BOT_TOKEN = "8748781038:AAF7JEXn5DcAI9YNgS2BCGkBOZoL3HwGcMA"
bot = telebot.TeleBot(BOT_TOKEN)

# Kanalingizdagi musiqalar bazasi (Nomi va file_id kodi)
CHANNEL_MUSIC_DATABASE = {
    "tosh": "KANALDAGI_AUDIO_FILE_ID_SHU_YERGA_YOZILADI",
    "bad times": "KANALDAGI_AUDIO_FILE_ID_SHU_YERGA_YOZILADI"
}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! Kanaldagi qo'shiq nomini yuboring 🎶")

@bot.message_handler(func=lambda message: True)
def search_local_music(message):
    query = message.text.lower().strip()
    
    if query in CHANNEL_MUSIC_DATABASE:
        file_id = CHANNEL_MUSIC_DATABASE[query]
        bot.send_audio(
            chat_id=message.chat.id, 
            audio=file_id, 
            caption=f"🎵 Kanalingizdan olindi"
        )
    else:
        bot.reply_to(
            message, 
            f"❌ '{message.text}' bazada topilmadi.\n\n💡 *Eslatma:* Qo'shiqni botga yuborib `file_id` olib, koddagi `CHANNEL_MUSIC_DATABASE` ga qo'shib qo'ying."
        )

if __name__ == '__main__':
    bot.infinity_polling()
