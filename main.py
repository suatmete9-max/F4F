import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, WebAppInfo
import threading
import os
from flask import Flask, render_template_string

# Yahan apna pura token dalein
TOKEN = '8808458591:AAGzWBqixE7fzX5WurWETaZ_MWt6zf6tYo0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Aapke Render server ka link (Yahan apna sahi render link dalein)
MINI_APP_URL = 'https://f4f.onrender.com/miniapp'

# --- SIDEBAR MENU SETUP ---
commands = [
    BotCommand("start", "🚀 Start Bot"),
    BotCommand("open_app", "🌟 Open Mini App")
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start', 'open_app'])
def send_welcome(message):
    text = f"Welcome {message.from_user.first_name}! 👋\nEarn karna shuru karne ke liye niche app open karein 👇"
    markup = InlineKeyboardMarkup()
    app_button = InlineKeyboardButton(text="🌟 Open App", web_app=WebAppInfo(url=MINI_APP_URL))
    markup.add(app_button)
    bot.send_message(message.chat.id, text, reply_markup=markup)

# --- BEAUTIFUL MINI APP (HTML/CSS & IN-APP ADS) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Premium Tasks App</title>
    
    <!-- Telegram Web App Script -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    
    <!-- AdsGram Web App SDK (Ye ad ko Telegram ke andar chalayega) -->
    <script src="https://sad.adsgram.ai/js/sad.min.js"></script>
    
    <style>
        body {
            margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('https://images.unsplash.com/photo-1511497584788-876760111969?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80') no-repeat center center fixed;
            background-size: cover; color: white; display: flex; flex-direction: column; height: 100vh; overflow-y: auto;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.9); color: #333; border-radius: 20px; padding: 20px; margin: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); text-align: center;
        }
        .balance-amount { font-size: 42px; font-weight: bold; margin: 10px 0; color: #2e7d32; }
        
        /* Task List Style */
        .task-card {
            background: #fff; color: #333; border-radius: 12px; margin: 10px 15px; padding: 15px;
            display: flex; justify-content: space-between; align-items: center;
            border: 2px solid #8d6e63;
        }
        .task-info h4 { margin: 0; font-size: 16px; color: #3e2723; }
        .task-info p { margin: 5px 0 0 0; font-size: 13px; color: #2e7d32; font-weight: bold; }
        
        .task-btn {
            background: linear-gradient(135deg, #ffb74d 0%, #f57c00 100%);
            color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer;
        }
        .task-btn:disabled { background: #ccc; cursor: not-allowed; }

        /* Bottom Nav */
        .bottom-nav {
            margin-top: auto; display: flex; justify-content: space-around; background: #3e2723;
            padding: 15px 0; border-top-left-radius: 20px; border-top-right-radius: 20px; position: sticky; bottom: 0;
        }
        .nav-item { text-align: center; font-size: 12px; color: white; opacity: 0.6; }
        .nav-item.active { opacity: 1; color: #ffb74d; font-weight: bold; }
    </style>
</head>
<body>

    <!-- Balance Section -->
    <div class="glass-card">
        <div style="font-size: 14px; color: #666; font-weight: bold;">TOTAL BALANCE</div>
        <div class="balance-amount" id="balanceDisplay">0.00 <span style="font-size: 20px;">USDT</span></div>
    </div>
    
    <!-- Tasks Header -->
    <h3 style="margin: 10px 15px; text-shadow: 1px 1px 2px black;">Tasks</h3>

    <!-- Task 1 -->
    <div class="task-card" id="task1">
        <div class="task-info">
            <h4>Visit and Wait 15 Seconds</h4>
            <p>+0.20 USDT</p>
        </div>
        <button class="task-btn" onclick="watchAd('task1', 0.20)">Visit</button>
    </div>

    <!-- Task 2 -->
    <div class="task-card" id="task2">
        <div class="task-info">
            <h4>Watch Premium Ad</h4>
            <p>+0.50 USDT</p>
        </div>
        <button class="task-btn" onclick="watchAd('task2', 0.50)">Watch</button>
    </div>

    <!-- Bottom Navigation -->
    <div class="bottom-nav">
        <div class="nav-item active">🏠<br>Home</div>
        <div class="nav-item">☑️<br>Tasks</div>
        <div class="nav-item">👥<br>Referrals</div>
    </div>

    <script>
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();

        let currentBalance = 0.00;

        // AdsGram SDK Initialize karein
        // Yahan 'YAHAN_BLOCK_ID_DALEIN' ki jagah AdsGram dashboard se mila WebApp Ad ka Block ID dalein (sirf numbers hote hain)
        const AdController = window.Adsgram.init({ blockId: "50267" });

        function watchAd(taskId, rewardAmount) {
            // Button disable karein taaki user baar baar click na kare
            let btn = document.querySelector(`#${taskId} .task-btn`);
            btn.innerText = "Loading...";
            btn.disabled = true;

            // In-App Ad Chalana (Ye script Telegram ke andar hi video aur timer chalayegi)
            AdController.show().then((result) => {
                // Ad pura dekhne ke baad ye chalega
                currentBalance += rewardAmount;
                document.getElementById('balanceDisplay').innerHTML = currentBalance.toFixed(2) + ' <span style="font-size: 20px;">USDT</span>';
                
                // Task done
                btn.innerText = "Done";
                btn.style.background = "#4caf50";
                
                // Telegram par notification dena
                window.Telegram.WebApp.showAlert(`Congrats! You earned +${rewardAmount} USDT.`);
            }).catch((result) => {
                // Agar user ne ad 15 sec se pehle close kar diya
                btn.innerText = "Visit";
                btn.disabled = false;
                window.Telegram.WebApp.showAlert("You must watch the full ad to earn rewards!");
            });
        }
    </script>
</body>
</html>
"""

# --- FLASK BACKEND SERVER ---
@app.route('/')
def index():
    return "Bot is Running!"

@app.route('/miniapp')
def render_miniapp():
    return render_template_string(HTML_PAGE)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)