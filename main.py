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

# --- ADVANCED MINI APP (6 Tasks, Settings, 2-Hour Timer, USDT BEP20) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Premium Tasks App</title>
    
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://sad.adsgram.ai/js/sad.min.js"></script>
    
    <style>
        body {
            margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('https://images.unsplash.com/photo-1511497584788-876760111969?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80') no-repeat center center fixed;
            background-size: cover; color: white; display: flex; flex-direction: column; height: 100vh; overflow: hidden;
        }
        .main-content { flex-grow: 1; overflow-y: auto; padding-bottom: 20px; }
        .tab-section { display: none; }
        .tab-section.active { display: block; }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.95); color: #333; border-radius: 20px; padding: 20px; margin: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); text-align: center;
        }
        .balance-amount { font-size: 42px; font-weight: bold; margin: 10px 0; color: #2e7d32; }
        
        .task-card {
            background: #fff; color: #333; border-radius: 12px; margin: 10px 15px; padding: 15px;
            display: flex; justify-content: space-between; align-items: center; border: 2px solid #8d6e63;
        }
        .task-info h4 { margin: 0; font-size: 15px; color: #3e2723; }
        .task-info p { margin: 5px 0 0 0; font-size: 13px; color: #2e7d32; font-weight: bold; }
        
        .task-btn {
            background: linear-gradient(135deg, #ffb74d 0%, #f57c00 100%);
            color: white; border: none; padding: 10px 15px; border-radius: 8px; font-weight: bold; cursor: pointer; min-width: 80px;
        }
        .task-btn:disabled { background: #ccc; cursor: not-allowed; color: #666; }

        input[type="text"] {
            width: 90%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #ccc; font-size: 14px;
        }

        .bottom-nav {
            display: flex; justify-content: space-around; background: #3e2723;
            padding: 10px 0; border-top-left-radius: 20px; border-top-right-radius: 20px;
        }
        .nav-item { text-align: center; font-size: 11px; color: white; opacity: 0.6; cursor: pointer; width: 25%; }
        .nav-item.active { opacity: 1; color: #ffb74d; font-weight: bold; }
        .nav-icon { font-size: 20px; margin-bottom: 3px; }
        
        /* A-ADS Banner */
        .aads-container { margin: 10px 15px; text-align: center; border-radius: 12px; overflow: hidden; background: white; }
    </style>
</head>
<body>

    <div class="main-content">
        <!-- HOME TAB -->
        <div id="home-tab" class="tab-section active">
            <div class="glass-card">
                <div style="font-size: 14px; color: #666; font-weight: bold;">TOTAL BALANCE</div>
                <div class="balance-amount" id="balanceDisplay">0.00 <span style="font-size: 20px;">USDT</span></div>
                <button class="task-btn" style="width: 100%; margin-top: 10px; padding: 15px;" onclick="withdraw()">Withdraw Funds (Min $3)</button>
            </div>
            
            <!-- A-ADS Banner -->
            <div class="aads-container">
                <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598' style='border:0px; padding:0; width:100%; height:60px; overflow:hidden; background-color: transparent;'></iframe>
            </div>
        </div>

        <!-- TASKS TAB (6 Ads with 2-hour gap) -->
        <div id="tasks-tab" class="tab-section">
            <h3 style="margin: 15px; text-shadow: 1px 1px 2px black;">Complete Tasks ($0.05 Each)</h3>
            <div id="tasks-container"></div>
        </div>

        <!-- REFERRALS TAB -->
        <div id="referrals-tab" class="tab-section">
            <div class="glass-card">
                <h3>Invite Friends</h3>
                <p>Earn <b style="color:#2e7d32;">$0.10 USDT</b> for every active friend you invite!</p>
                <button class="task-btn" style="width: 100%;" onclick="copyRefLink()">Copy Invite Link</button>
            </div>
        </div>

        <!-- SETTINGS TAB -->
        <div id="settings-tab" class="tab-section">
            <div class="glass-card">
                <h3>⚙️ Settings</h3>
                <p style="font-size: 13px; color: #666;">Add your wallet to receive payments.</p>
                <div style="text-align: left; font-size: 14px; font-weight: bold; margin-top:15px;">USDT (BEP20) Address:</div>
                <input type="text" id="walletInput" placeholder="Enter Wallet Address (0x...)">
                <button class="task-btn" style="width: 100%;" onclick="saveWallet()">Save Address</button>
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
        <div class="nav-item" id="nav-settings" onclick="switchTab('settings-tab', 'nav-settings')">
            <div class="nav-icon">⚙️</div>Settings
        </div>
    </div>

    <script>
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();

        // Constants
        const REWARD = 0.05;
        const MIN_WITHDRAW = 3.00;
        const COOLDOWN_MS = 2 * 60 * 60 * 1000; // 2 hours
        const ADSGRAM_BLOCK = "50267";

        // Ad Links
        const ADSTERRA_LINK = "https://www.profitableratecpmnetwork.com/de868ezg?key=8b85fb3adea19f8ec85c709bba7de919";
        const MONETAG_LINK = "https://omg10.com/4/11851710";
        
        let AdController = null;
        try { AdController = window.Adsgram.init({ blockId: ADSGRAM_BLOCK }); } catch(e) {}

        const tasksData = [
            { id: 1, title: "Premium Sponsor Ad 1", type: "link", url: ADSTERRA_LINK },
            { id: 2, title: "High Yield Ad 1", type: "link", url: MONETAG_LINK },
            { id: 3, title: "Video Reward Ad 1", type: "adsgram", url: "" },
            { id: 4, title: "Premium Sponsor Ad 2", type: "link", url: ADSTERRA_LINK },
            { id: 5, title: "High Yield Ad 2", type: "link", url: MONETAG_LINK },
            { id: 6, title: "Video Reward Ad 2", type: "adsgram", url: "" }
        ];

        // Load saved balance
        let balance = parseFloat(localStorage.getItem('f4f_balance')) || 0.00;
        document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px;">USDT</span>';

        // Load wallet
        document.getElementById('walletInput').value = localStorage.getItem('f4f_wallet') || "";

        function updateBalance(amount) {
            balance += amount;
            localStorage.setItem('f4f_balance', balance.toFixed(2));
            document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px;">USDT</span>';
        }

        // Generate Task UI
        const tasksContainer = document.getElementById('tasks-container');
        tasksData.forEach(task => {
            tasksContainer.innerHTML += `
                <div class="task-card" id="taskCard_${task.id}">
                    <div class="task-info">
                        <h4>${task.title}</h4>
                        <p>+$0.05 USDT</p>
                    </div>
                    <button class="task-btn" id="btn_${task.id}" onclick="startTask(${task.id}, '${task.type}', '${task.url}')">Watch</button>
                </div>
            `;
        });

        // Cooldown Timer Logic
        function checkCooldowns() {
            let now = Date.now();
            tasksData.forEach(task => {
                let savedTime = localStorage.getItem('cooldown_' + task.id);
                let btn = document.getElementById('btn_' + task.id);
                if (savedTime) {
                    let diff = now - parseInt(savedTime);
                    if (diff < COOLDOWN_MS) {
                        btn.disabled = true;
                        let remainingMin = Math.ceil((COOLDOWN_MS - diff) / 60000);
                        btn.innerText = `Wait ${remainingMin}m`;
                    } else {
                        btn.disabled = false;
                        btn.innerText = "Watch";
                        localStorage.removeItem('cooldown_' + task.id);
                    }
                }
            });
        }
        setInterval(checkCooldowns, 10000); // Check every 10 sec
        checkCooldowns(); // Check on load

        function startTask(id, type, url) {
            let btn = document.getElementById('btn_' + id);
            btn.disabled = true;
            btn.innerText = "Wait 15s...";

            if (type === 'link') {
                window.open(url, '_blank');
                setTimeout(() => { finishTask(id); }, 15000);
            } else if (type === 'adsgram') {
                if(AdController) {
                    AdController.show().then(() => { finishTask(id); }).catch(() => {
                        btn.disabled = false; btn.innerText = "Watch";
                        window.Telegram.WebApp.showAlert("You closed the ad early!");
                    });
                } else {
                    window.Telegram.WebApp.showAlert("AdsGram not ready. Try other tasks.");
                    btn.disabled = false; btn.innerText = "Watch";
                }
            }
        }

        function finishTask(id) {
            updateBalance(REWARD);
            localStorage.setItem('cooldown_' + id, Date.now()); // Start 2-hour timer
            checkCooldowns();
            window.Telegram.WebApp.showAlert(`Task Complete! You earned $0.05 USDT.`);
        }

        function withdraw() {
            let wallet = localStorage.getItem('f4f_wallet');
            if(balance < MIN_WITHDRAW) {
                window.Telegram.WebApp.showAlert(`Minimum withdrawal is $${MIN_WITHDRAW}. You need $${(MIN_WITHDRAW - balance).toFixed(2)} more.`);
            } else if(!wallet || wallet.length < 10) {
                switchTab('settings-tab', 'nav-settings');
                window.Telegram.WebApp.showAlert("Please save a valid USDT BEP20 address in Settings first.");
            } else {
                window.Telegram.WebApp.showAlert("Withdrawal Request Submitted! It will be reviewed by admin.");
                // Yahan aage admin ko message bhejne ka API lag sakta hai
                balance -= MIN_WITHDRAW;
                localStorage.setItem('f4f_balance', balance.toFixed(2));
                document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px;">USDT</span>';
            }
        }

        function saveWallet() {
            let wallet = document.getElementById('walletInput').value;
            if (wallet.length > 10) {
                localStorage.setItem('f4f_wallet', wallet);
                window.Telegram.WebApp.showAlert("USDT BEP20 Address Saved Successfully!");
            } else {
                window.Telegram.WebApp.showAlert("Please enter a valid wallet address.");
            }
        }

        function copyRefLink() {
            let userId = window.Telegram.WebApp.initDataUnsafe?.user?.id || "USER_ID";
            let link = `https://t.me/foll4foll_bot?start=${userId}`;
            navigator.clipboard.writeText(link);
            window.Telegram.WebApp.showAlert(`Referral link copied! \nInvite friends to earn $0.10 USDT each.`);
        }

        function switchTab(tabId, navId) {
            document.querySelectorAll('.tab-section').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            document.getElementById(navId).classList.add('active');
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