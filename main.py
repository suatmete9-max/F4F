import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, WebAppInfo
import threading
import os
import time
from flask import Flask, render_template_string

# Yahan apna pura token dalein
TOKEN = '8808458591:AAGzWBqixE7fzX5WurWETaZ_MWt6zf6tYo0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Aapke Render server ka link (Yahan apna sahi render link dalein)
MINI_APP_URL = 'https://f4f.onrender.com/miniapp'

active_groups = set()

# --- SIDEBAR MENU SETUP ---
commands = [
    BotCommand("start", "🚀 Start Bot"),
    BotCommand("open_app", "🌟 Open Mini App")
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start', 'open_app'])
def send_welcome(message):
    text = f"Welcome {message.from_user.first_name}! 👋\nHamara beautiful Mini App open karne ke liye niche click karein 👇"
    markup = InlineKeyboardMarkup()
    # Ye button Telegram ke andar Mini App kholega
    app_button = InlineKeyboardButton(text="🌟 Open App", web_app=WebAppInfo(url=MINI_APP_URL))
    markup.add(app_button)
    bot.send_message(message.chat.id, text, reply_markup=markup)

# --- BEAUTIFUL MINI APP (HTML/CSS DESIGN) ---
# Ye code bilkul Nut Wallet jaisa premium design aur scenery dega
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Premium Mini App</title>
    <!-- Telegram Web App Script -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            /* Yahan ek beautiful nature/scenery background lagaya gaya hai */
            background: url('https://images.unsplash.com/photo-1511497584788-876760111969?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80') no-repeat center center fixed;
            background-size: cover;
            color: white;
            display: flex;
            flex-direction: column;
            height: 100vh;
            overflow: hidden;
        }
        /* Premium Glass Effect */
        .glass-card {
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 20px;
            margin: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        .balance-title { font-size: 16px; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }
        .balance-amount { font-size: 42px; font-weight: bold; margin: 10px 0; color: #4ade80; }
        
        .btn-primary {
            background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
            color: #111;
            border: none;
            padding: 16px;
            width: 100%;
            border-radius: 15px;
            font-size: 18px;
            font-weight: bold;
            margin-top: 15px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(253, 160, 133, 0.4);
        }
        
        .task-list {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 12px;
            margin-top: 10px;
        }
        .task-btn {
            background: #ff9f43;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 8px;
            font-weight: bold;
        }

        /* Bottom Navigation bar Nut Wallet ki tarah */
        .bottom-nav {
            margin-top: auto;
            display: flex;
            justify-content: space-around;
            background: rgba(0, 0, 0, 0.7);
            padding: 15px 0;
            backdrop-filter: blur(15px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .nav-item { text-align: center; font-size: 12px; opacity: 0.7; }
        .nav-item.active { opacity: 1; color: #f6d365; font-weight: bold; }
        .nav-icon { font-size: 24px; margin-bottom: 5px; }
    </style>
</head>
<body>

    <!-- Balance Section -->
    <div class="glass-card" style="text-align: center; margin-top: 30px;">
        <div class="balance-title">Total Balance</div>
        <div class="balance-amount">0.00 <span style="font-size: 20px; color: white;">USDT</span></div>
    </div>
    
    <!-- Tasks Section -->
    <div class="glass-card">
        <h3 style="margin-top: 0;">Earn Your First USDT</h3>
        <p style="opacity: 0.8; font-size: 14px;">Complete simple tasks, get paid instantly.</p>
        
        <div class="task-list">
            <div>
                <div style="font-weight: bold;">Visit & Wait 15 Sec</div>
                <div style="color: #4ade80; font-size: 12px;">+0.20 USDT</div>
            </div>
            <button class="task-btn" onclick="openAdsGram()">Visit</button>
        </div>
        
        <button class="btn-primary" onclick="openAdsGram()">🎥 Watch Auto Ads</button>
    </div>

    <!-- Bottom Navigation -->
    <div class="bottom-nav">
        <div class="nav-item active">
            <div class="nav-icon">🏠</div>
            Home
        </div>
        <div class="nav-item">
            <div class="nav-icon">☑️</div>
            Tasks
        </div>
        <div class="nav-item">
            <div class="nav-icon">👥</div>
            Referrals
        </div>
    </div>

    <script>
        // Telegram App ko initialize karna
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand(); // App ko full screen karna

        function openAdsGram() {
            // YAHAN APNA ADSGRAM KA LINK DALEIN
            window.location.href = "https://f4f.onrender.com//adsgram/reward?userid=[userId]";
        }
    </script>
</body>
</html>
"""

# --- FLASK BACKEND SERVER ---
@app.route('/')
def index():
    return "Bot is Running!"

# Ye route Telegram Mini App ko HTML page bhejega
@app.route('/miniapp')
def render_miniapp():
    return render_template_string(HTML_PAGE)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)