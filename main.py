import os
import threading
import time
from flask import Flask, render_template_string
import telebot
from telebot.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

# Railway ke environment variable se token lene ke liye
TOKEN = os.environ.get('TOKEN', '')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

MINI_APP_URL = 'https://f4f-production-0321.up.railway.app/'
active_groups = set()

# --- 1. TELEGRAM SIDEBAR MENU SETUP ---
commands = [
    BotCommand('start', '🚀 Start & Open App'),
    BotCommand('tasks', '☑️ Complete Tasks ($0.05)'),
    BotCommand('jointasks', '📢 Join Channels ($0.03)'),
    BotCommand('daily', '🎁 Daily Bonus ($0.02)'),
    BotCommand('balance', '💰 Check Balance'),
    BotCommand('refer', '👥 Invite Friends'),
    BotCommand('promotion', '📢 Paid Promotion'),
    BotCommand('help', '📞 Support / Help'),
]
try:
  bot.set_my_commands(commands)
except Exception as e:
  print(f'Commands set karne mein error: {e}')


@bot.message_handler(
    commands=[
        'start',
        'tasks',
        'jointasks',
        'balance',
        'daily',
        'refer',
        'promotion',
        'help',
    ]
)
def handle_commands(message):
  cmd = message.text.split()[0]

  if cmd == '/refer':
    bot.send_message(
        message.chat.id,
        f'Your Referral Link:\n`https://t.me/foll4foll_bot?start={message.from_user.id}`\n\nShare'
        ' with friends and earn $0.10 USDT per referral!',
        parse_mode='Markdown',
    )
  elif cmd == '/promotion':
    bot.send_message(
        message.chat.id,
        '📢 **Paid Promotion:**\nWant to promote your Channel, Group, or Bot'
        ' worldwide? Contact admin: 👉 @Loverschoice786',
    )
  elif cmd == '/help':
    bot.send_message(
        message.chat.id,
        '📞 **Support & Help:**\nFor any assistance, contact admin: 👉'
        ' @Loverschoice786',
    )
  else:
    text = (
        f'Welcome {message.from_user.first_name}! 👋\nOpen the Nut Wallet below'
        ' to complete tasks, join channels, and earn USDT 👇'
    )
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='🌰 Open Nut Wallet', web_app=WebAppInfo(url='https://f4f-production-0321.up.railway.app')
        )
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)


# --- 2. SUB4SUB GROUP LOGIC ---
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
  active_groups.add(message.chat.id)
  for new_member in message.new_chat_members:
    try:
      if new_member.id == bot.get_me().id:
        continue
    except Exception:
      pass

    user_name = new_member.first_name
    text = f'Welcome {user_name}! 👋\n\n'
    text += '🔥 **Group Rules (Sub4Sub):**\n'
    text += (
        'Check the online members list, send a DM to users who are online, and'
        " ask: 'Join my channel and I will join yours'.\n\n"
    )
    text += '💰 **Earn Free USDT:**\nClick the button below to complete tasks and earn rewards 👇'

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='🌟 Earn Free USDT', web_app=WebAppInfo(url='https://f4f-production-0321.up.railway.app')
        )
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)


def send_ads_every_2_hours():
  while True:
    time.sleep(7200)
    ad_text = (
        '📢 **Sponsored Global Tasks:**\n\nEarn free USDT without any'
        ' investment. Open Nut Wallet now 👇'
    )
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(
            text='💰 Watch Ads & Earn', web_app=WebAppInfo(url='https://f4f-production-0321.up.railway.app')
        )
    )
    for chat_id in active_groups.copy():
      try:
        bot.send_message(chat_id, ad_text, reply_markup=markup)
      except Exception:
        pass


# --- 3. MINI APP WITH ANTI-CHEAT & CLEAN JOIN SYSTEM ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Nut Wallet - Task & Earn USDT</title>
    
    <meta property="og:title" content="Nut Wallet - Earn Free USDT on Telegram">
    <meta property="og:description" content="Complete simple tasks, join channels for $0.03, claim daily $0.02 bonus, and earn $0.10 USDT per referral!">
    <meta property="og:image" content="https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80">
    <meta property="og:url" content="https://f4f-production-0321.up.railway.app/">
    <meta property="og:type" content="website">

    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    
    <style>
        body {
            margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80') no-repeat center center fixed;
            background-size: cover; color: #3e2723; display: flex; flex-direction: column; height: 100vh; overflow: hidden;
        }
        .main-content { flex-grow: 1; overflow-y: auto; padding-bottom: 30px; }
        .tab-section { display: none; animation: fadeIn 0.3s ease-in-out; }
        .tab-section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
        
        .nut-wood-card {
            background: linear-gradient(135deg, #f5d6b0 0%, #d4a373 100%);
            border: 4px solid #5c3a21; border-radius: 24px;
            padding: 20px; margin: 15px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4); text-align: center;
        }
        .balance-amount { font-size: 38px; font-weight: bold; margin: 6px 0; color: #1b4d3e; text-shadow: 1px 1px 0px rgba(255,255,255,0.4); }
        
        .task-card {
            background: #fff8eb; border: 3px solid #6f4e37; border-radius: 16px;
            margin: 10px 15px; padding: 14px 16px; display: flex; justify-content: space-between; align-items: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .task-info h4 { margin: 0; font-size: 15px; color: #3e2723; font-weight: bold; }
        .task-info p { margin: 4px 0 0 0; font-size: 13px; color: #2e7d32; font-weight: bold; }
        
        .btn-nut {
            background: linear-gradient(135deg, #588157 0%, #3a5a40 100%);
            color: white; border: 2px solid #283618; padding: 10px 18px; border-radius: 12px;
            font-weight: bold; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.3); text-transform: uppercase; font-size: 13px;
        }
        .btn-nut:disabled { background: #b0bec5; border-color: #78909c; color: #455a64; cursor: not-allowed; }

        input[type="text"] {
            width: 90%; padding: 12px; margin: 10px 0; border-radius: 12px; border: 2px solid #6f4e37;
            font-size: 14px; background: #fffdf9; text-align: center; color: #3e2723; font-weight: bold;
        }

        .ticker-box {
            background: rgba(62, 39, 35, 0.92); border: 3px solid #5c3a21; border-radius: 16px;
            margin: 15px; padding: 10px 15px; text-align: left; height: 55px; overflow: hidden; position: relative;
            box-shadow: 0 6px 15px rgba(0,0,0,0.3);
        }
        .ticker-title { font-size: 11px; color: #f4a261; font-weight: bold; margin-bottom: 2px; text-transform: uppercase; letter-spacing: 0.5px; }
        .ticker-container { height: 32px; overflow: hidden; position: relative; }
        .ticker-item {
            position: absolute; width: 100%; opacity: 0; transform: translateY(15px);
            transition: all 0.5s ease-in-out; font-size: 12px; color: #fff;
            display: flex; justify-content: space-between; align-items: center;
        }
        .ticker-item.active { opacity: 1; transform: translateY(0); }
        .ticker-amount { color: #a3cef1; font-weight: bold; }

        .bottom-nav {
            display: flex; justify-content: space-around; background: #3b2219; border-top: 4px solid #5c3a21;
            padding: 8px 0; border-top-left-radius: 20px; border-top-right-radius: 20px;
            box-shadow: 0 -5px 15px rgba(0,0,0,0.4);
        }
        .nav-item { text-align: center; font-size: 10px; color: #d7ccc8; cursor: pointer; width: 20%; font-weight: 600; }
        .nav-item.active { color: #ffb703; font-weight: bold; text-shadow: 0 0 8px rgba(255,183,3,0.6); }
        .nav-icon { font-size: 18px; margin-bottom: 2px; }
        
        .aads-container { margin: 10px 15px; text-align: center; border-radius: 14px; overflow: hidden; background: #fff8eb; border: 3px solid #6f4e37; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    </style>
</head>
<body>

    <div class="main-content">

        <!-- HOME TAB -->
        <div id="home-tab" class="tab-section active">
            <div class="nut-wood-card">
                <div style="font-size: 13px; color: #5c3a21; font-weight: bold; letter-spacing: 0.5px;">TOTAL BALANCE</div>
                <div class="balance-amount" id="balanceDisplay">0.00 <span style="font-size: 20px; color: #2d6a4f;">USDT</span></div>
                <div style="display: flex; gap: 10px; margin-top: 15px;">
                    <button class="btn-nut" style="flex: 1;" onclick="withdraw()">Withdraw ($3+)</button>
                    <button class="btn-nut" style="flex: 1; background: linear-gradient(135deg, #4ea8de 0%, #0077b6 100%); border-color: #03045e;" onclick="switchTab('referrals-tab', 'nav-referrals')">Invite ($0.10)</button>
                </div>
            </div>

            <div class="aads-container">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>

            <div class="ticker-box">
                <div class="ticker-title">⚡ Live Payouts (USDT BEP20)</div>
                <div class="ticker-container" id="tickerContainer"></div>
            </div>
        </div>

        <!-- TASKS TAB ($0.05) -->
        <div id="tasks-tab" class="tab-section">
            <div class="aads-container" style="margin-top: 15px;">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>
            
            <div class="nut-wood-card" style="padding: 12px; margin: 15px;">
                <h3 style="margin: 0; color: #3e2723;">Watch & Earn ($0.05 Each)</h3>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: #5c3a21;">Complete partner tasks with anti-cheat protection!</p>
            </div>
            <div id="tasks-container"></div>
        </div>

        <!-- CHANNEL JOIN TASKS TAB ($0.03) -->
        <div id="join-tab" class="tab-section">
            <div class="aads-container" style="margin-top: 15px;">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>
            
            <div class="nut-wood-card" style="padding: 12px; margin: 15px;">
                <h3 style="margin: 0; color: #3e2723;">Join Channels & Earn ($0.03)</h3>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: #5c3a21;">Join below and verify to claim your reward instantly!</p>
            </div>
            <div id="join-tasks-container"></div>
        </div>

        <!-- DAILY BONUS TAB ($0.02) -->
        <div id="daily-tab" class="tab-section">
            <div class="aads-container" style="margin-top: 15px;">
              <iframe data-aa='2456598' src='//acceptable.a-ads.com/2456598/?size=Adaptive' style='border:0; padding:0; width:70%; height:auto; overflow:hidden; display:block; margin:auto'></iframe>
            </div>

            <div class="nut-wood-card">
                <h3>🎁 Daily Reward</h3>
                <p style="color: #5c3a21;">Claim your free daily bonus of <b style="color:#2d6a4f;">$0.02 USDT</b> every 24 hours!</p>
                <button class="btn-nut" id="dailyBtn" style="width: 100%; padding: 12px;" onclick="claimDaily()">Claim $0.02 Bonus</button>
            </div>
        </div>

        <!-- REFERRALS TAB ($0.10) -->
        <div id="referrals-tab" class="tab-section">
            <div class="nut-wood-card">
                <h3>Invite Friends</h3>
                <p style="color: #5c3a21;">Earn <b style="color:#2d6a4f;">$0.10 USDT</b> for every active friend you invite worldwide!</p>
                <button class="btn-nut" style="width: 100%;" onclick="copyRefLink()">Copy Invite Link</button>
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

            <div class="nut-wood-card">
                <h3>⚙️ Settings</h3>
                <p style="font-size: 13px; color: #5c3a21;">Add your wallet to receive global payments.</p>
                <div style="text-align: left; font-size: 13px; font-weight: bold; margin-top:10px; color:#3e2723;">USDT (BEP20) Address:</div>
                <input type="text" id="walletInput" placeholder="Enter Wallet Address (0x...)">
                <button class="btn-nut" style="width: 100%; margin-top: 5px;" onclick="saveWallet()">Save Address</button>
                <hr style="margin:15px 0; border:0; border-top:2px dashed #b08968;">
                <p style="font-size: 12px; color: #5c3a21;">Want to promote your link globally?</p>
                <button class="btn-nut" style="width: 100%; background: linear-gradient(135deg, #4ea8de 0%, #0077b6 100%); border-color: #03045e;" onclick="window.Telegram.WebApp.openTelegramLink('https://t.me/Loverschoice786')">Contact Admin</button>
            </div>
        </div>

    </div>

    <!-- Bottom Navigation -->
    <div class="bottom-nav">
        <div class="nav-item active" id="nav-home" onclick="switchTab('home-tab', 'nav-home')">
            <div class="nav-icon">🌰</div>Home
        </div>
        <div class="nav-item" id="nav-tasks" onclick="switchTab('tasks-tab', 'nav-tasks')">
            <div class="nav-icon">📋</div>Tasks
        </div>
        <div class="nav-item" id="nav-join" onclick="switchTab('join-tab', 'nav-join')">
            <div class="nav-icon">📢</div>Join $0.03
        </div>
        <div class="nav-item" id="nav-referrals" onclick="switchTab('referrals-tab', 'nav-referrals')">
            <div class="nav-icon">🐿️</div>Invite
        </div>
        <div class="nav-item" id="nav-settings" onclick="switchTab('settings-tab', 'nav-settings')">
            <div class="nav-icon">⚙️</div>Settings
        </div>
    </div>

    <script>
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();

        const TASK_REWARD = 0.05;
        const JOIN_REWARD = 0.03;
        const MIN_WITHDRAW = 3.00;
        const COOLDOWN_MS = 2 * 60 * 60 * 1000;
        
        const ADSTERRA_LINK = "https://www.profitableratecpmnetwork.com/de868ezg?key=8b85fb3adea19f8ec85c709bba7de919";
        const MONETAG_LINK = "https://omg10.com/4/11851710";
        const MAIN_JOIN_URL = "https://t.me/a2zdownloader";

        const tasksData = [
            { id: 1, title: "Global Partner Ad 1", url: ADSTERRA_LINK },
            { id: 2, title: "High Yield Ad 1", url: MONETAG_LINK },
            { id: 3, title: "Global Partner Ad 2", url: ADSTERRA_LINK },
            { id: 4, title: "High Yield Ad 2", url: MONETAG_LINK }
        ];

        const channelJoinTasks = [
            { id: 1, title: "Join Official Channel Slot 1" },
            { id: 2, title: "Join Community Group Slot 2" },
            { id: 3, title: "Join Crypto Updates Slot 3" },
            { id: 4, title: "Join Partner Channel Slot 4" },
            { id: 5, title: "Join Support Bot Slot 5" },
            { id: 6, title: "Join Announcement Slot 6" },
            { id: 7, title: "Join VIP Channel Slot 7" },
            { id: 8, title: "Join Global Group Slot 8" },
            { id: 9, title: "Join Network Slot 9" },
            { id: 10, title: "Join Bonus Channel Slot 10" }
        ];

        let balance = parseFloat(localStorage.getItem('f4f_balance')) || 0.00;
        document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px; color: #2d6a4f;">USDT</span>';
        document.getElementById('walletInput').value = localStorage.getItem('f4f_wallet') || "";

        function updateBalance(amount) {
            balance += amount;
            localStorage.setItem('f4f_balance', balance.toFixed(2));
            document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px; color: #2d6a4f;">USDT</span>';
        }

        const tasksContainer = document.getElementById('tasks-container');
        tasksData.forEach(task => {
            tasksContainer.innerHTML += `
                <div class="task-card" id="taskCard_${task.id}">
                    <div class="task-info">
                        <h4>${task.title}</h4>
                        <p>+$0.05 USDT</p>
                    </div>
                    <button class="btn-nut" id="btn_${task.id}" onclick="startTask(${task.id}, '${task.url}')">Watch</button>
                </div>
            `;
        });

        const joinContainer = document.getElementById('join-tasks-container');
        channelJoinTasks.forEach(jTask => {
            let isCompleted = localStorage.getItem('jointask_' + jTask.id) === 'completed';
            let btnText = isCompleted ? "Completed" : "Join ($0.03)";
            let btnDisabled = isCompleted ? "disabled" : "";

            joinContainer.innerHTML += `
                <div class="task-card" id="joinCard_${jTask.id}">
                    <div class="task-info">
                        <h4>${jTask.title}</h4>
                        <p style="color:#1b4d3e;">+$0.03 USDT</p>
                    </div>
                    <button class="btn-nut" id="joinBtn_${jTask.id}" ${btnDisabled} onclick="startJoinTask(${jTask.id})">${btnText}</button>
                </div>
            `;
        });

        function startJoinTask(id) {
            let btn = document.getElementById('joinBtn_' + id);
            btn.disabled = true;
            btn.innerText = "Verify (5s)...";
            
            window.open(MAIN_JOIN_URL, '_blank');

            let timeLeft = 5;
            let timer = setInterval(() => {
                timeLeft--;
                if(timeLeft > 0) {
                    btn.innerText = `Verify (${timeLeft}s)...`;
                } else {
                    clearInterval(timer);
                    updateBalance(JOIN_REWARD);
                    localStorage.setItem('jointask_' + id, 'completed');
                    btn.innerText = "Completed";
                    window.Telegram.WebApp.showAlert(`Success! You earned $0.03 USDT.`);
                }
            }, 1000);
        }

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
                    dailyBtn.innerText = `Claimed (${remainingHours}h left)`;
                } else {
                    dailyBtn.disabled = false;
                    dailyBtn.innerText = "Claim $0.02 Bonus";
                }
            }
        }
        setInterval(checkCooldowns, 10000);
        checkCooldowns();

        const firstNames = ["Alex", "John", "David", "Michael", "Chris", "Emma", "Sophia", "Liam", "Noah", "Oliver", "James", "Lucas", "Ethan", "Mason", "Logan", "Alexander", "Daniel", "Henry", "Jackson", "Aiden", "Samuel", "Sebastian", "Carter", "Wyatt", "Jayden", "Grayson", "Leo", "Jaxon", "Julian", "Cooper", "Elias", "Aaron", "Landon", "Ezra", "Jonathan", "Nolan", "Easton", "Colton", "Cameron", "Carson", "Robert", "Angel", "Maverick", "Nicholas", "Dominic", "Jaxson", "Luka", "Jordan", "Stacy", "Elena", "Natasha", "Viktor", "Dmitri", "Carlos", "Mateo", "Santiago", "Enzo", "Gabriel", "Benjamin", "Jack", "Levi", "Owen", "Asher", "Kenji", "Hiroshi", "Yuki", "Jin", "Min-ho", "Sora", "Ren", "Haruto", "Riku", "Daiki", "Kaito", "Sho", "Taiga", "Asahi", "Yuto", "Sota", "Ryota", "Kazuki"];
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
        for(let i=0; i<100; i++) {
            let name = firstNames[Math.floor(Math.random() * firstNames.length)] + " " + lastInitials[Math.floor(Math.random() * lastInitials.length)];
            let amount = (Math.random() * (25.00 - 3.00) + 3.00).toFixed(2);
            let wallet = generateRandomWallet();
            withdrawals.push({ name: name, amount: amount, wallet: wallet });
        }

        const tickerContainer = document.getElementById('tickerContainer');
        withdrawals.forEach((w, index) => {
            let activeClass = index === 0 ? 'active' : '';
            tickerContainer.innerHTML += `
                <div class="ticker-item ${activeClass}" id="tick_${index}">
                    <span>🌰 <b>${w.name}</b> (${w.wallet})</span>
                    <span class="ticker-amount">+$${w.amount} USDT</span>
                </div>
            `;
        });

        let currentTick = 0;
        setInterval(() => {
            document.getElementById(`tick_${currentTick}`).classList.remove('active');
            currentTick = (currentTick + 1) % withdrawals.length;
            document.getElementById(`tick_${currentTick}`).classList.add('active');
        }, 3000);

        function startTask(id, url) {
            let btn = document.getElementById('btn_' + id);
            btn.disabled = true;
            btn.innerText = "Wait 15s...";
            window.open(url, '_blank');
            setTimeout(() => { finishTask(id); }, 15000);
        }

        function finishTask(id) {
            updateBalance(TASK_REWARD);
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
            let wallet = localStorage.getItem('f4f_wallet');
            if(balance < MIN_WITHDRAW) {
                window.Telegram.WebApp.showAlert(`Minimum withdrawal is $${MIN_WITHDRAW}. You need $${(MIN_WITHDRAW - balance).toFixed(2)} more.`);
            } else if(!wallet || wallet.length < 10) {
                switchTab('settings-tab', 'nav-settings');
                window.Telegram.WebApp.showAlert("Please save a valid USDT BEP20 address in Settings first.");
            } else {
                window.Telegram.WebApp.showAlert("Withdrawal request submitted successfully!");
                balance -= MIN_WITHDRAW;
                localStorage.setItem('f4f_balance', balance.toFixed(2));
                document.getElementById('balanceDisplay').innerHTML = balance.toFixed(2) + ' <span style="font-size: 20px; color: #2d6a4f;">USDT</span>';
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
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
  return 'Nut Wallet Bot is Running!'


@app.route('/miniapp')
def render_miniapp():
  return render_template_string(HTML_PAGE)


def run_bot():
  bot.infinity_polling(none_stop=True)


if __name__ == '__main__':
  # Bot aur Ads ko background thread mein chalu karna
  threading.Thread(target=run_bot, daemon=True).start()
  threading.Thread(target=send_ads_every_2_hours, daemon=True).start()

  # Railway ke port par Flask server run karna
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)
