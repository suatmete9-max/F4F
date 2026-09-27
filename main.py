import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import threading
import os
import time
from flask import Flask

# Yahan apna pura token dalein
TOKEN = '8808458591:AAGzWBqixE7fzX5WurWETaZ_MWt6zf6tYo0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# AdsGram ka Direct Link
ADSGRAM_LINK = 'https://f4f.onrender.com//adsgram/reward?userid=[userId]'

active_groups = set()

# --- MAIN MENU KEYBOARD (Niche wala Side bar) ---
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_start = KeyboardButton('🚀 Start')
    btn_join = KeyboardButton('🤝 Join Now')
    btn_ads = KeyboardButton('🎥 Ads Watch')
    btn_ref = KeyboardButton('🔗 Ref & Earn')
    btn_bal = KeyboardButton('💰 Balance')
    btn_sup = KeyboardButton('📞 Support')
    btn_promo = KeyboardButton('📢 Promotional')
    
    markup.add(btn_start, btn_join)
    markup.add(btn_ads, btn_ref, btn_bal)
    markup.add(btn_sup, btn_promo)
    return markup

# --- COMMAND HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = f"Welcome {message.from_user.first_name}! 👋\nNiche diye gaye menu se koi bhi option select karein."
    bot.reply_to(message, text, reply_markup=main_menu())

# --- BUTTON CLICK HANDLERS ---
@bot.message_handler(func=lambda message: True)
def handle_menu_clicks(message):
    chat_id = message.chat.id
    text = message.text

    if text == '🚀 Start':
        bot.send_message(chat_id, "Bot start ho chuka hai! Aap menu ka use kar sakte hain.", reply_markup=main_menu())
        
    elif text == '🤝 Join Now':
        bot.send_message(chat_id, "Hamara official group aur channel join karein:\n👉 [YAHAN GROUP LINK DALEIN]")
        
    elif text == '🎥 Ads Watch':
        text_ad = "Ad dekhne ke liye niche click karein (15 sec) 🎥👇"
        markup = InlineKeyboardMarkup()
        ad_button = InlineKeyboardButton(text="💰 Click Here to Watch Ad", url=ADSGRAM_LINK)
        markup.add(ad_button)
        bot.send_message(chat_id, text_ad, reply_markup=markup)
        
    elif text == '🔗 Ref & Earn':
        bot.send_message(chat_id, f"Aapka Referral Link:\n`https://t.me/foll4foll_bot?start={message.from_user.id}`\n\nIse apne doston ke sath share karein aur earn karein!", parse_mode='Markdown')
        
    elif text == '💰 Balance':
        bot.send_message(chat_id, "Aapka current balance: 0 Credits\n(Note: Ad dekhne aur refer karne par yahan balance update hoga.)")
        
    elif text == '📞 Support':
        bot.send_message(chat_id, "Kisi bhi help ya jankari ke liye hamare admin se baat karein:\n👉 @Loverschoice786")
        
    elif text == '📢 Promotional':
        bot.send_message(chat_id, "Apna Channel, Group ya Bot promote karne ke liye paid promotion available hai.\nMessage karein: 👉 @Loverschoice786")

# --- GROUP JOIN WELCOME & AD (Puraana feature) ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_and_force_ad(message):
    active_groups.add(message.chat.id)
    for new_member in message.new_chat_members:
        user_name = new_member.first_name
        text_welcome = f"Welcome {user_name}! 👋\n\nGroup rules follow karein aur start karne se pehle ad dekhein👇"
        markup = InlineKeyboardMarkup()
        ad_button = InlineKeyboardButton(text="🎥 Watch Ad To Start", url=ADSGRAM_LINK)
        markup.add(ad_button)
        bot.send_message(message.chat.id, text_welcome, reply_markup=markup)

# --- 2-HOUR AD SCHEDULER ---
def send_ads_every_2_hours():
    while True:
        time.sleep(7200) # 2 ghante
        ad_text = "📢 **Sponsored Ad:**\nZaroor dekhein 👇"
        markup = InlineKeyboardMarkup()
        ad_button = InlineKeyboardButton(text="💰 Watch Ad & Earn", url=ADSGRAM_LINK)
        markup.add(ad_button)
        for chat_id in active_groups.copy():
            try:
                bot.send_message(chat_id, ad_text, parse_mode='Markdown', reply_markup=markup)
            except Exception:
                pass

# --- FLASK BACKEND SERVER ---
@app.route('/')
def index():
    return "Bot with Menu is Running 24/7!"

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=send_ads_every_2_hours, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)