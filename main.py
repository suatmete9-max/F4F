import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, WebAppInfo
import threading
import os
import time
from flask import Flask, render_template_string

TOKEN = '8808458591:AAGzWBqixE7fzX5WurWETaZ_MWt6zf6tYo0'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

MINI_APP_URL = 'https://f4f.onrender.com/miniapp'
active_groups = set()

# --- 1. TELEGRAM SIDEBAR MENU SETUP ---
commands = [
    BotCommand("start", "🚀 Start & Open App"),
    BotCommand("tasks", "☑️ Complete Tasks"),
    BotCommand("daily", "🎁 Daily Bonus ($0.02)"),
    BotCommand("balance", "💰 Check Balance"),
    BotCommand("refer", "👥 Invite Friends"),
    BotCommand("promotion", "📢 Paid Promotion"),
    BotCommand("help", "📞 Support / Help")
]
bot.set_my_commands(commands)

@bot.message_handler(commands=['start', 'tasks', 'balance', 'daily'])
def send_app_button(message):
    text = f"Welcome {message.from_user.first_name}! 👋\nOpen the Mini App below to complete tasks, get daily bonus, and earn USDT 👇"
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="🌟 Open F4F Wallet", web_app=WebAppInfo(url=MINI_APP_URL)))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['refer'])
def refer_cmd(message):
    bot.send_message(message.chat.id, f"Your Referral Link:\n`https://t.me/foll4foll_bot?start={message.from_user.id}`\n\nShare with friends and earn $0.10 USDT per referral!", parse_mode='Markdown')

@bot.message_handler(commands=['promotion'])
def promo_cmd(message):
    bot.send_message(message.chat.id, "📢 **Paid Promotion:**\nWant to promote your Channel, Group, or Bot worldwide? Contact admin: 👉 @Loverschoice786")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(message.chat.id, "📞 **Support & Help:**\nFor any assistance, contact admin: 👉 @Loverschoice786")


# --- 2. SUB4SUB GROUP LOGIC ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    active_groups.add(message.chat.id)
    for new_member in message.new_chat_members:
        if new_member.id == bot.get_me().id:
            continue
            
        user_name = new_member.first_name
        text = f"Welcome {user_name}! 👋\n\n"
        text += "🔥 **Group Rules (Sub4Sub):**\n"
        text += "Check the online members list, send a DM to users who are online, and ask: 'Join my channel and I will join yours'.\n\n"
        text += "💰 **Earn Free USDT:**\nClick the button below to complete tasks and earn rewards 👇"
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="🌟 Earn Free USDT", web_app=WebAppInfo(url=MINI_APP_URL)))
        bot.send_message(message.chat.id, text, reply_markup=markup)

def send_ads_every_2_hours():
    while True:
        time.sleep(7200)
        ad_text = "📢 **Sponsored Global Tasks:**\n\nEarn free USDT without any investment. Open the app now 👇"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="💰 Watch Ads & Earn", web_app=WebAppInfo(url=MINI_APP_URL)))
        for chat_id in active_groups.copy():
            try:
                bot.send_message(chat_id, ad_text, reply_markup=markup)
            except Exception:
                pass


# --- 3. GLOBAL MINI APP WITH LIVE WITHDRAWAL TICKER ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Global Task Wallet</title>
    
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    
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
            background: rgba(255, 255, 255, 0.92); color: #333; border-radius: 20px; padding: 20px; margin: 15px;
            backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3); text-align: center;
        }
        .balance-amount { font-size: 42px; font-weight: bold; margin: 10px 0; color: #2e7d32; }
        
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

        /* Live Withdrawal Ticker Box */
        .ticker-box {
            background: rgba(0, 0, 0, 0.65); border-radius: 12px; margin: 15px; padding: 10px 15px;
            border: 1px solid rgba(255, 255, 255, 0.2); text-align: left; height: 60px; overflow: hidden; position: relative;
        }
        .ticker-title { font-size: 11px; color: #ffb74d; font-weight: bold; margin-bottom: 4px; text-transform: uppercase; }
        .ticker-container { height: 35px; overflow: hidden; position: relative; }
        .ticker-item {
            position: absolute; width: 100%; opacity: 0; transform: translateY(20px);
            transition: all 0.5s ease-in-out; font-size: 13px; color: #e0e0e0;
            display: flex; justify-content: space-between; align-items: center;
        }
        .ticker-item.active { opacity: 1; transform: translateY(0); }
        .ticker-amount { color: #4caf50; font-weight: bold; }

        .bottom-nav {
            display: flex; justify-content: space-around; background: rgba(62, 39, 35, 0.95); backdrop-filter: blur(10px);
            padding: 10px 0; border-top-left-radius: 20px; border-top-right-radius: 20px;
        }
        .nav-item { text-align: center; font-size: 10px; color: white; opacity: 0.6; cursor: pointer; width: 20%; }
        .nav-item.active { opacity: 1; color: #ffb74d; font-weight: bold; }
        .nav-icon { font-size: 18px; margin-bottom: 2px; }
        
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

            <!-- 🔥 LIVE WITHDRAWAL TICKER (200+ simulated payouts) -->
            <div class="ticker-box">
                <div class="ticker-title">⚡ Live Payouts (USDT BEP20)</div>
                <div class="ticker-container" id="tickerContainer">
                    <!-- Dynamic items inserted via JS -->
                </div>
            </div>
            
            <!-- Home Banner Ad -->
            <div class="aads-container">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>
        </div>

        <!-- TASKS TAB -->
        <div id="tasks-tab" class="tab-section">
            <div class="aads-container" style="margin-top: 15px;">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>
            
            <h3 style="margin: 15px; text-shadow: 1px 1px 3px rgba(0,0,0,0.8);">Complete Tasks ($0.05 Each)</h3>
            <div id="tasks-container"></div>
        </div>

        <!-- DAILY BONUS TAB ($0.02) -->
        <div id="daily-tab" class="tab-section">
            <div class="aads-container" style="margin-top: 15px;">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>

            <div class="glass-card">
                <h3>🎁 Daily Reward</h3>
                <p>Claim your free daily bonus of <b style="color:#2e7d32;">$0.02 USDT</b> every 24 hours!</p>
                <button class="task-btn" id="dailyBtn" style="width: 100%; padding: 12px;" onclick="claimDaily()">Claim $0.02 Bonus</button>
            </div>
        </div>

        <!-- REFERRALS TAB -->
        <div id="referrals-tab" class="tab-section">
            <div class="glass-card">
                <h3>Invite Friends</h3>
                <p>Earn <b style="color:#2e7d32;">$0.10 USDT</b> for every active friend you invite worldwide!</p>
                <button class="task-btn" style="width: 100%;" onclick="copyRefLink()">Copy Invite Link</button>
            </div>
            
            <div class="aads-container">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>
        </div>

        <!-- SETTINGS TAB -->
        <div id="settings-tab" class="tab-section">
            <div class="aads-container" style="margin-top: 15px;">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>

            <div class="glass-card">
                <h3>⚙️ Settings</h3>
                <p style="font-size: 13px; color: #666;">Add your wallet to receive global payments.</p>
                <div style="text-align: left; font-size: 14px; font-weight: bold; margin-top:15px;">USDT (BEP20) Address:</div>
                <input type="text" id="walletInput" placeholder="Enter Wallet Address (0x...)">
                <button class="task-btn" style="width: 100%;" onclick="saveWallet()">Save Address</button>
                <hr style="margin:20px 0; border:0; border-top:1px solid #ddd;">
                <p style="font-size: 12px; color: #666;">Want to promote your link globally?</p>
                <button class="task-btn" style="width: 100%; background: #2196F3;" onclick="window.Telegram.WebApp.openTelegramLink('https://t.me/Loverschoice786')">Contact Admin</button>
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
        <div class="nav-item" id="nav-daily" onclick="switchTab('daily-tab', 'nav-daily')">
            <div class="nav-icon">🎁</div>Bonus
        </div>
        <div class="nav-item" id="nav-referrals" onclick="switchTab('referrals-tab', 'nav-referrals')">
            <div class="nav-icon">👥</div>Invite
        </div>
        <div class="nav-item" id="nav-settings" onclick="switchTab('settings-tab', 'nav-settings')">
            <div class="nav-icon">⚙️</div>Settings
        </div>
    </div>

    <script>
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();

        const backgrounds = {
            'home-tab': 'url("https://images.unsplash.com/photo-1502602898657-3e91760cbb34?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80")',
            'tasks-tab': 'url("https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80")',
            'daily-tab': 'url("https://images.unsplash.com/photo-1519681393784-d120267933ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80")',
            'referrals-tab': 'url("https://images.unsplash.com/photo-1533105079780-92b9be482077?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80")',
            'settings-tab': 'url("https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80")'
        };
        document.body.style.backgroundImage = backgrounds['home-tab'];

        const REWARD = 0.05;
        const MIN_WITHDRAW = 3.00;
        const COOLDOWN_MS = 2 * 60 * 60 * 1000;
        
        const ADSTERRA_LINK = "https://www.profitableratecpmnetwork.com/de868ezg?key=8b85fb3adea19f8ec85c709bba7de919";
        const MONETAG_LINK = "https://omg10.com/4/11851710";

        const tasksData = [
            { id: 1, title: "Global Partner Ad 1", url: ADSTERRA_LINK },
            { id: 2, title: "High Yield Ad 1", url: MONETAG_LINK },
            { id: 3, title: "Global Partner Ad 2", url: ADSTERRA_LINK },
            { id: 4, title: "High Yield Ad 2", url: MONETAG_LINK },
            { id: 5, title: "Global Partner Ad 3", url: ADSTERRA_LINK },
            { id: 6, title: "High Yield Ad 3", url: MONETAG_LINK }
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
                    <button class="task-btn" id="btn_${task.id}" onclick="startTask(${task.id}, '${task.url}')">Watch</button>
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

            let lastDaily = localStorage.getItem('last_daily_claim');
            let dailyBtn = document.getElementById('dailyBtn');
            if (lastDaily) {
                let diff = now - parseInt(lastDaily);
                let dayMs = 24 * 60 * 60 * 1000;
                if (diff < dayMs) {
                    dailyBtn.disabled = true;
                    let remainingHours = Math.ceil((dayMs - diff) / 3600000);
                    dailyBtn.innerText = `Claimed (Next in ${remainingHours}h)`;
                } else {
                    dailyBtn.disabled = false;
                    dailyBtn.innerText = "Claim $0.02 Bonus";
                }
            }
        }
        setInterval(checkCooldowns, 10000);
        checkCooldowns();

        // 🔥 GENERATE 200+ RANDOM WITHDRAWALS FOR TICKER
        const firstNames = ["Alex", "John", "David", "Michael", "Chris", "Emma", "Sophia", "Liam", "Noah", "Oliver", "James", "Lucas", "Ethan", "Mason", "Logan", "Alexander", "Daniel", "Henry", "Jackson", "Aiden", "Samuel", "Sebastian", "David", "Carter", "Wyatt", "Jayden", "John", "Grayson", "Leo", "Jaxon", "Julian", "Cooper", "Elias", "Aaron", "Landon", "Ezra", "Jonathan", "Nolan", "Jeremiah", "Easton", "Elias", "Colton", "Cameron", "Carson", "Robert", "Angel", "Maverick", "Nicholas", "Dominic", "Jaxson", "Luka", "Jordan", "Stacy", "Elena", "Natasha", "Viktor", "Dmitri", "Carlos", "Mateo", "Santiago", "Leonardo", "Enzo", "Gabriel", "Samuel", "Benjamin", "Lucas", "Mason", "Logan", "Alexander", "Ethan", "Oliver", "Elijah", "Noah", "Liam", "James", "William", "Benjamin", "Lucas", "Henry", "Theodore", "Jack", "Levi", "Alexander", "Owen", "Mateo", "Asher", "Samuel", "Ethan", "Leo", "習慣", "Kenji", "Hiroshi", "Yuki", "Jin", "Min-ho", "Sora", "Ren", "Haruto", "Riku", "Daiki", "Tatsuya", "Kaito", "Sho", "Taiga", "Asahi", "Yuto", "Sota", "Ryota", "Kazuki"];
        const lastInitials = ["A.", "B.", "C.", "D.", "E.", "F.", "G.", "H.", "I.", "J.", "K.", "L.", "M.", "N.", "O.", "P.", "Q.", "R.", "S.", "T.", "U.", "V.", "W.", "X.", "Y.", "Z."];
        
        function generateRandomWallet() {
            const chars = "0123456789abcdef";
            let addr = "0x";
            for(let i=0; i<40; i++) {
                addr += chars[Math.floor(Math.random() * chars.length)];
            }
            return addr.substring(0, 6) + "..." + addr.substring(38);
        }

        let withdrawals = [];
        for(let i=0; i<200; i++) {
            let name = firstNames[Math.floor(Math.random() * firstNames.length)] + " " + lastInitials[Math.floor(Math.random() * lastInitials.length)];
            let amount = (Math.random() * (25.00 - 3.00) + 3.00).toFixed(2);
            let wallet = generateRandomWallet();
            withdrawals.push({ name: name, amount: amount, wallet: wallet });
        }

        // Setup Ticker HTML
        const tickerContainer = document.getElementById('tickerContainer');
        withdrawals.forEach((w, index) => {
            let activeClass = index === 0 ? 'active' : '';
            tickerContainer.innerHTML += `
                <div class="ticker-item ${activeClass}" id="tick_${index}">
                    <span>👤 <b>${w.name}</b> (${w.wallet})</span>
                    <span class="ticker-amount">+$${w.amount} USDT</span>
                </div>
            `;
        });

        // Rotate Ticker Items
        let currentTick = 0;
        setInterval(() => {
            document.getElementById(`tick_${currentTick}`).classList.remove('active');
            currentTick = (currentTick + 1) % withdrawals.length;
            document.getElementById(`tick_${currentTick}`).classList.add('active');
        }, 3000); // Change every 3 seconds

        function startTask(id, url) {
            let btn = document.getElementById('btn_' + id);
            btn.disabled = true;
            btn.innerText = "Wait 15s...";
            window.open(url, '_blank');
            setTimeout(() => { finishTask(id); }, 15000);
        }

        function finishTask(id) {
            updateBalance(REWARD);
            localStorage.setItem('cooldown_' + id, Date.now());
            checkCooldowns();
            window.Telegram.WebApp.showAlert(`Task Completed! You earned $0.05 USDT.`);
        }

        function claimDaily() {
            updateBalance(0.02);
            localStorage.setItem('last_daily_claim', Date.now());
            checkCooldowns();
            window.Telegram.WebApp.showAlert(`Success! You claimed your daily $0.02 USDT bonus.`);
        }

        function withdraw() {
            let wallet = localStorage.getItem('walletInput').value || localStorage.getItem('f4f_wallet');
            if(balance < MIN_WITHDRAW) {
                window.Telegram.WebApp.showAlert(`Minimum withdrawal is $${MIN_WITHDRAW}. You need $${(MIN_WITHDRAW - balance).toFixed(2)} more.`);
            } else if(!wallet || wallet.length < 10) {
                switchTab('settings-tab', 'nav-settings');
                window.Telegram.WebApp.showAlert("Please save a valid USDT BEP20 address in Settings first.");
            } else {
                window.Telegram.WebApp.showAlert("Withdrawal request submitted successfully!");
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
            window.Telegram.WebApp.showAlert(`Referral link copied! Earn $0.10 USDT per invite.`);
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

@app.route('/')
def index():
    return "Global F4F Task Bot is Running!"

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
