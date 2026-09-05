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
BOT_TOKEN = "8748781038:AAFcbKTnLbMxy3uFtUzGERAWMnkjqCE1V6U"
bot = telebot.TeleBot(BOT_TOKEN)

# 1. O'zingizning kanalingizdagi musiqalar bazasi (file_id larni shu yerga yozib qo'yasiz)
CHANNEL_MUSIC_DATABASE = {
    # "musiqa nomi": "KANALDAGI_AUDIO_FILE_ID_KODI"
}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! Qo'shiq nomini yuboring. Avval kanalimdan, topilmasa Telegram qidiruvidan topib beraman 🎵")

@bot.message_handler(func=lambda message: True)
def handle_music_request(message):
    query = message.text.lower().strip()
    
    # 1-Qadam: Avval o'zingizning kanalingiz bazasidan qidiramiz
    if query in CHANNEL_MUSIC_DATABASE:
        file_id = CHANNEL_MUSIC_DATABASE[query]
        bot.send_audio(
            chat_id=message.chat.id, 
            audio=file_id, 
            caption=f"🎵 Sizning kanalingizdan olindi"
        )
        return

    # 2-Qadam: Kanalda bo'lmasa, Telegram'dagi boshqa musiqa botlari orqali inline qidiramiz
    try:
        msg = bot.reply_to(message, f"🔍 '{message.text}' Telegram bazasidan qidirilmoqda...")
        
        # Ommaviy musiqa botlari (masalan @Vkmusicbot yoki @Melobot kabilar) orqali qidirish uchun inline so'rov
        # Bu yerda bot Telegram'ning global qidiruvidan foydalanib musiqa qidiradi
        results = bot.get_inline_bot_results("@Vkmusicbot", message.text)
        
        if results and results.results:
            # Topilgan birinchi musiqani foydalanuvchiga yuborish
            first_result = results.results[0]
            bot.send_audio(
                chat_id=message.chat.id,
                audio=first_result.audio.audio_url if hasattr(first_result, 'audio') else first_result.id,
                caption=f"🎵 Telegram musiqa bazasidan topildi"
            )
            bot.delete_message(message.chat.id, msg.message_id)
        else:
            bot.edit_message_text(
                f"❌ Afsuski, '{message.text}' na kanalingizdan, na Telegram bazasidan topilmadi.", 
                chat_id=message.chat.id, 
                message_id=msg.message_id
            )
            
    except Exception as e:
        bot.edit_message_text(
            f"❌ Qidirish vaqtida xatolik yuz berdi. (Botda inline qidirish yoqilmagan bo'lishi mumkin)", 
            chat_id=message.chat.id, 
            message_id=msg.message_id
        )

if __name__ == '__main__':
    bot.infinity_polling()
