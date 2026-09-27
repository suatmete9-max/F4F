import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, WebAppInfo
import threading
import os
from flask import Flask, render_template_string

# Yahan apna pura token dalein
TOKEN = '8808458591:AAGzWBqixE7fzX5WurWETaZ_MWt6zf6tYo0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Aapke Render server ka link
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

# --- BEAUTIFUL MINI APP WITH WORKING TABS ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Premium Tasks App</title>
    
    <!-- Telegram Web App Script -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    
    <!-- AdsGram Web App SDK -->
    <script src="https://sad.adsgram.ai/js/sad.min.js"></script>
    
    <style>
        body {
            margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('https://images.unsplash.com/photo-1511497584788-876760111969?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80') no-repeat center center fixed;
            background-size: cover; color: white; display: flex; flex-direction: column; height: 100vh; overflow: hidden;
        }
        .main-content {
            flex-grow: 1; overflow-y: auto; padding-bottom: 20px;
        }
        .tab-section { display: none; } /* Default hide tabs */
        .tab-section.active { display: block; } /* Show active tab */
        
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
            display: flex; justify-content: space-around; background: #3e2723;
            padding: 15px 0; border-top-left-radius: 20px; border-top-right-radius: 20px;
        }
        .nav-item { text-align: center; font-size: 12px; color: white; opacity: 0.6; cursor: pointer; width: 33%; }
        .nav-item.active { opacity: 1; color: #ffb74d; font-weight: bold; }
        .nav-icon { font-size: 20px; margin-bottom: 5px; }
    </style>
</head>
<body>

    <div class="main-content">
        <!-- HOME TAB -->
        <div id="home-tab" class="tab-section active">
            <div class="glass-card">
                <div style="font-size: 14px; color: #666; font-weight: bold;">TOTAL BALANCE</div>
                <div class="balance-amount" id="balanceDisplay">0.00 <span style="font-size: 20px;">USDT</span></div>
            </div>
            <div class="glass-card">
                <h3>Welcome to F4F!</h3>
                <p>Complete tasks to earn USDT directly to your wallet.</p>
                <button class="task-btn" onclick="switchTab('tasks-tab', 'nav-tasks')">Go to Tasks</button>
            </div>
        </div>

        <!-- TASKS TAB -->
        <div id="tasks-tab" class="tab-section">
            <h3 style="margin: 15px; text-shadow: 1px 1px 2px black;">Available Tasks</h3>
            
            <div class="task-card" id="task1">
                <div class="task-info">
                    <h4>Visit and Wait 15 Seconds</h4>
                    <p>+0.20 USDT</p>
                </div>
                <button class="task-btn" onclick="watchAd('task1', 0.20)">Visit</button>
            </div>

            <div class="task-card" id="task2">
                <div class="task-info">
                    <h4>Watch Premium Ad</h4>
                    <p>+0.50 USDT</p>
                </div>
                <button class="task-btn" onclick="watchAd('task2', 0.50)">Watch</button>
            </div>
        </div>

        <!-- REFERRALS TAB -->
        <div id="referrals-tab" class="tab-section">
            <div class="glass-card">
                <h3>Invite Friends</h3>
                <p>Earn 2.00 USDT for every active friend you invite!</p>
                <button class="task-btn" onclick="window.Telegram.WebApp.showAlert('Referral system coming soon!')">Copy Invite Link</button>
            </div>
        </div>
    </div>

    <!-- Bottom Navigation -->
    <div class="bottom-nav">
        <div class="nav-item active" id="nav-home" onclick="switchTab('home-tab', 'nav-home')">
            <div class="nav-icon">🏠</div>Home
        </div>
        <div class="nav-item" id="nav-tasks" onclick="switchTab('tasks-tab', 'nav-tasks')">
            <div class="nav-icon">☑️</div>Tasks
        </div>
        <div class="nav-item" id="nav-referrals" onclick="switchTab('referrals-tab', 'nav-referrals')">
            <div class="nav-icon">👥</div>Referrals
        </div>
    </div>

    <script>
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();

        let currentBalance = 0.00;

        // Aapki photo ke hisaab se Block ID 50267 set kar diya gaya hai
        const AdController = window.Adsgram.init({ blockId: "50267" });

        // TABS SWITCH KARNE KA FUNCTION
        function switchTab(tabId, navId) {
            // Hide all tabs
            document.querySelectorAll('.tab-section').forEach(tab => tab.classList.remove('active'));
            // Remove active class from all nav items
            document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
            
            // Show selected tab and highlight nav item
            document.getElementById(tabId).classList.add('active');
            document.getElementById(navId).classList.add('active');
        }

        // AD DEKHNE KA FUNCTION
        function watchAd(taskId, rewardAmount) {
            let btn = document.querySelector(`#${taskId} .task-btn`);
            btn.innerText = "Loading...";
            btn.disabled = true;

            AdController.show().then((result) => {
                currentBalance += rewardAmount;
                document.getElementById('balanceDisplay').innerHTML = currentBalance.toFixed(2) + ' <span style="font-size: 20px;">USDT</span>';
                btn.innerText = "Done";
                btn.style.background = "#4caf50";
                window.Telegram.WebApp.showAlert(`Congrats! You earned +${rewardAmount} USDT.`);
            }).catch((error) => {
                btn.innerText = "Visit";
                btn.disabled = false;
                // AdsGram block error show karega agar active nahi hoga
                window.Telegram.WebApp.showAlert("Ad failed or closed early. Please check your AdsGram dashboard.");
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