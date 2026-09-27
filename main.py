import telebot
import threading
import os
from flask import Flask

# Yahan apna Bot Token daalein
TOKEN = '8808458591:AAGzWBqixE7fzX5WurWETaZ_MWt6zf6tYo0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- 1. TELEGRAM BOT KA CODE ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_and_promote(message):
    for new_member in message.new_chat_members:
        user_name = new_member.first_name
        
        promo_text = f"Welcome {user_name}! 👋\n\n"
        promo_text += "🔥 **Group Rules & Sub4Sub:**\n"
        promo_text += "Member list mein check karein jo log ONLINE hain unhe direct message karein ('Mera channel join karo, main aapka karunga').\n\n"
        promo_text += "👇 **Admin Ka Channel Zaroor Join Karein:**\n"
        promo_text += "👉 [YAHAN APNE CHANNEL KA LINK DAALEIN]\n"
        
        bot.send_message(message.chat.id, promo_text, parse_mode='Markdown')

# --- 2. FLASK BACKEND SERVER (Render ke liye zaroori) ---
@app.route('/')
def index():
    return "Bot is Alive and Running 24/7!"

# Bot ko background thread mein chalane ke liye function
def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Bot ko background mein start karna
    threading.Thread(target=run_bot).start()
    # Web server ko start karna
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
