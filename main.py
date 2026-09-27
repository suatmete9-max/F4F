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

# Aapke Render server ka link
MINI_APP_URL = 'https://f4f.onrender.com/miniapp'

# Group tracking for 2-hour ads
active_groups = set()

# --- 1. TELEGRAM SIDEBAR MENU SETUP ---
commands = [
    BotCommand("start", "🚀 Start & Open App"),
    BotCommand("tasks", "☑️ Complete Tasks"),
    BotCommand("balance", "💰 Check Balance"),
    BotCommand("refer", "👥 Invite Friends"),
    BotCommand("promotion", "📢 Paid Promotion"),
    BotCommand("help", "📞 Support / Help")
]
bot.set_my_commands(commands)

# --- 2. MENU COMMAND HANDLERS ---
@bot.message_handler(commands=['start', 'tasks', 'balance'])
def send_app_button(message):
    text = f"Welcome {message.from_user.first_name}! 👋\nApne Tasks, Balance aur F4F ke liye niche app open karein 👇"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🌟 Open F4F Wallet", web_app=WebAppInfo(url=MINI_APP_URL)))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['refer'])
def refer_cmd(message):
    bot.send_message(message.chat.id, f"Aapka Referral Link:\n`https://t.me/foll4foll_bot?start={message.from_user.id}`\n\nIse doston ke sath share karein aur $0.10 USDT kamayein!", parse_mode='Markdown')

@bot.message_handler(commands=['promotion'])
def promo_cmd(message):
    bot.send_message(message.chat.id, "📢 **Paid Promotion:**\nAgar aapko apna Channel, Group ya Bot promote karwana hai, toh admin se contact karein: 👉 @Loverschoice786")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "📞 **Support & Help:**\nKisi bhi madad ke liye admin ko message karein: 👉 @Loverschoice786")


# --- 3. SUB4SUB GROUP LOGIC (Welcome & Rules in Hinglish & English) ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    active_groups.add(message.chat.id)
    for new_member in message.new_chat_members:
        user_name = new_member.first_name
        text = f"Welcome {user_name}! 👋\n\n"
        text += "🔥 **Group Rules (Sub4Sub):**\n\n"
        text += "🇮🇳 **Hinglish:** Group member list mein check karein jo log ONLINE hain unhe direct message (DM) karein aur bolein: 'Mera channel join karo, main aapka karunga'.\n\n"
        text += "🇬🇧 **English:** Check the group member list, DM the users who are ONLINE, and ask: 'Join my channel and I will join yours'.\n\n"
        text += "💰 **Free USDT Earn Karein / Earn Free USDT:**\n"
        text += "Niche button par click karke Tasks poore karein aur paise kamayein 👇"
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="🌟 Earn Free USDT", web_app=WebAppInfo(url=MINI_APP_URL)))
        bot.send_message(message.chat.id, text, reply_markup=markup)

# Har 2 ghante mein Group Ad
def send_ads_every_2_hours():
    while True:
        time.sleep(7200) # 2 hours
        ad_text = "📢 **Sponsored Ad / Premium Tasks:**\n\nBina kisi investment ke Free USDT kamane ke liye abhi app open karein 👇"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="💰 Watch Ads & Earn", web_app=WebAppInfo(url=MINI_APP_URL)))
        for chat_id in active_groups.copy():
            try:
                bot.send_message(chat_id, ad_text, reply_markup=markup)
            except Exception:
                pass


# --- 4. ADVANCED BEAUTIFUL MINI APP ---
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
            transition: background-image 0.8s ease-in-out;
            background-size: cover; background-position: center; background-attachment: fixed;
            color: white; display: flex; flex-direction: column; height: 100vh; overflow: hidden;
        }
        .main-content { flex-grow: 1; overflow-y: auto; padding-bottom: 20px; }
        .tab-section { display: none; animation: fadeIn 0.5s; }
        .tab-section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.90); color: #333; border-radius: 20px; padding: 20px; margin: 15px;
            backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); text-align: center;
        }
        .balance-amount { font-size: 42px; font-weight: bold; margin: 10px 0; color: #2e7d32; text-shadow: 1px 1px 0px rgba(0,0,0,0.1); }
        
        .task-card {
            background: rgba(255, 255, 255, 0.95); color: #333; border-radius: 12px; margin: 10px 15px; padding: 15px;
            display: flex; justify-content: space-between; align-items: center; border: 2px solid rgba(141, 110, 99, 0.5);
        }
        .task-info h4 { margin: 0; font-size: 15px; color: #3e2723; }
        .task-info p { margin: 5px 0 0 0; font-size: 13px; color: #2e7d32; font-weight: bold; }
        
        .task-btn {
            background: linear-gradient(135deg, #ffb74d 0%, #f57c00 100%);
            color: white; border: none; padding: 10px 15px; border-radius: 8px; font-weight: bold; cursor: pointer; min-width: 80px;
        }
        .task-btn:disabled { background: #ccc; cursor: not-allowed; color: #666; }

        input[type="text"] { width: 90%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #ccc; font-size: 14px; }

        .bottom-nav {
            display: flex; justify-content: space-around; background: rgba(62, 39, 35, 0.95); backdrop-filter: blur(10px);
            padding: 10px 0; border-top-left-radius: 20px; border-top-right-radius: 20px;
        }
        .nav-item { text-align: center; font-size: 11px; color: white; opacity: 0.6; cursor: pointer; width: 25%; }
        .nav-item.active { opacity: 1; color: #ffb74d; font-weight: bold; }
        .nav-icon { font-size: 20px; margin-bottom: 3px; }
        
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
            
            <div class="aads-container">
                <!-- BEGIN AADS AD UNIT 2456598 -->
                <div id="frame" style="width: 100%;margin: auto;position: relative; z-index: 99998; margin-top: 15px;">
                  <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive'
                          style='border:0; padding:0; width:70%; height:auto; overflow:hidden;display: block;margin: auto'></iframe>
                </div>
                <!-- END AADS AD UNIT 2456598 -->
            </div>
        </div>

        <!-- TASKS TAB -->
        <div id="tasks-tab" class="tab-section">
            <h3 style="margin: 15px; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);">Complete Tasks ($0.05 Each)</h3>
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
                <hr style="margin:20px 0; border:0; border-top:1px solid #ddd;">
                <p style="font-size: 12px; color: #666;">Want to promote your own link/group here?</p>
                <button class="task-btn" style="width: 100%; background: #2196F3;" onclick="window.Telegram.WebApp.openTelegramLink('https://t.me/Loverschoice786')">Contact Admin for Promotion</button>
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

        // 🖼️ DYNAMIC BEAUTIFUL BACKGROUNDS (Different for each tab)
        const backgrounds = {
            'home-tab': 'url("https://images.unsplash.com/photo-1499856871958-5b9627545d1a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")', // Paris Cityscape
            'tasks-tab': 'url("https://images.unsplash.com/photo-1501785888041-af3ef285b470?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")', // Swiss Alps Lake
            'referrals-tab': 'url("https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")', // Santorini Greece
            'settings-tab': 'url("https://images.unsplash.com/photo-1542051812871-757508122268?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80")' // Kyoto Japan
        };
        
        // Initial Background
        document.body.style.backgroundImage = backgrounds['home-tab'];

        const REWARD = 0.05;
        const MIN_WITHDRAW = 3.00;
        const COOLDOWN_MS = 2 * 60 * 60 * 1000;
        const ADSGRAM_BLOCK = "50267";
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

        let balance = parseFloat(localStorage.getItem('f4f_balance')) || 0.00;
        document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px;">USDT</span>';
        document.getElementById('walletInput').value = localStorage.getItem('f4f_wallet') || "";

        function updateBalance(amount) {
            balance += amount;
            localStorage.setItem('f4f_balance', balance.toFixed(2));
            document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px;">USDT</span>';
        }

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
        setInterval(checkCooldowns, 10000);
        checkCooldowns();

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
            localStorage.setItem('cooldown_' + id, Date.now());
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
            
            document.body.style.backgroundImage = backgrounds[tabId];
        }
    </script>
</body>
</html>
"""

# --- FLASK BACKEND SERVER ---
@app.route('/')
def index():
    return "F4F Master Bot is Running!"

@app.route('/miniapp')
def render_miniapp():
    return render_template_string(HTML_PAGE)

def run_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=send_ads_every_2_hours, daemon=True).start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)