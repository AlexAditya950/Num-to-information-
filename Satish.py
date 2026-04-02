import requests
import json
import logging
import asyncio
import io
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== CONFIGURATION ====================

API_BASE = "https://source-code-api.vercel.app/?num="
BOT_TOKEN = "7107142138:AAExraW37E8AVrDXTJ4MAo3hTRAHKKcnvl4"

REQUIRED_CHANNEL_ID_1 = "@num9663"
JOIN_LINK_1 = "https://t.me/num9663"

REQUIRED_CHANNEL_ID_2 = -1003814864736 
JOIN_LINK_2 = "https://t.me/num9663"

OWNER_ID = 8429473345 

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) Gecko/117.0 Firefox/117.0",
    "Accept": "application/json",
    "Referer": "https://anish-axploits.vercel.app/",
    "Connection": "keep-alive"
}

# ==================== BOT SETUP ====================
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ==================== HELPER FUNCTIONS ====================

def log_user_message(user, text):
    user_id = str(user.id)
    username = user.username if user.username else "N/A"
    first_name = user.first_name if user.first_name else "N/A"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{current_time}] ID:{user_id} @{username} ({first_name}) | MSG: {text}\n"
    try:
        with open("messages.log", "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        logging.error(f"Error logging message: {e}") 

def save_user_data(user):
    user_id = str(user.id)
    username = user.username if user.username else "N/A"
    first_name = user.first_name if user.first_name else "N/A"
    data_line = f"{user_id},{username},{first_name}\n"
    try:
        # User ko save karne se pehle check karein ki wo pehle se hai ya nahi
        existing_ids = set()
        if os.path.exists("user_data.txt"):
            with open("user_data.txt", "r", encoding="utf-8") as f:
                existing_ids = {line.split(',')[0].strip() for line in f if line.strip()}
        
        if user_id not in existing_ids:
            with open("user_data.txt", "a", encoding="utf-8") as f:
                f.write(data_line)
    except Exception as e:
        logging.error(f"Error saving user data: {e}")

async def is_user_member_of_both_chats(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> bool:
    try:
        m1 = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL_ID_1, user_id=user_id)
        m2 = await context.bot.get_chat_member(chat_id=REQUIRED_CHANNEL_ID_2, user_id=user_id)
        valid = ['member', 'administrator', 'creator']
        return m1.status in valid and m2.status in valid
    except:
        return False

# ==================== ADMIN COMMANDS ====================

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ *Access Denied*.", parse_mode='Markdown')
        return
    if not context.args:
        await update.message.reply_text("📝 Use: `/broadcast Hello Users`", parse_mode='Markdown')
        return
    
    if not os.path.exists("user_data.txt"):
        await update.message.reply_text("❌ Database file (user_data.txt) not found.")
        return

    msg = " ".join(context.args)
    success, fail = 0, 0
    
    with open("user_data.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    sending_msg = await update.message.reply_text(f"⏳ Sending to {len(lines)} users...")

    for line in lines:
        if not line.strip(): continue
        try:
            target_id = line.split(',')[0].strip()
            await context.bot.send_message(chat_id=int(target_id), text=msg, parse_mode='Markdown')
            success += 1
            await asyncio.sleep(0.2) # Rate limit protection
        except:
            fail += 1
            
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=sending_msg.message_id,
        text=f"📢 **Broadcast Finished**\n\n✅ Sent: {success}\n❌ Failed: {fail}"
    )

async def send_user_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    if os.path.exists("user_data.txt"):
        with open("user_data.txt", "rb") as f:
            await update.message.reply_document(document=f, caption="✅ *Current User Database*")
    else:
        await update.message.reply_text("❌ No user data found yet.")

async def send_message_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    if os.path.exists("messages.log"):
        with open("messages.log", "rb") as f:
            await update.message.reply_document(document=f, caption="💰 *Search History Logs*")
    else:
        await update.message.reply_text("❌ No logs found yet.")

# ==================== HANDLERS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user_data(update.effective_user)
    user_name = update.effective_user.first_name or "User"
    
    if await is_user_member_of_both_chats(context, user_id):
        keyboard = [[KeyboardButton("📞 ENTER NUMBER")]]  
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)  
        await update.message.reply_text(f"👋 Hello *{user_name}*!\n\nWELCOME TO THE NETWORK WORLD OF THE SATISH", reply_markup=reply_markup, parse_mode='Markdown')
    else:
        keyboard = [[InlineKeyboardButton("Join Channel", url=JOIN_LINK_1)], [InlineKeyboardButton("Join Group", url=JOIN_LINK_2)]]
        await update.message.reply_text(f"Hello *{user_name}*\n\nJoin both channels to use the bot.", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if text: log_user_message(update.effective_user, text)
    
    # Check if joined
    if not await is_user_member_of_both_chats(context, user_id):
        await start(update, context)
        return

    if text == "📞 ENTER NUMBER":
        await update.message.reply_text("📤 *Send Your 10-digit Number:*", parse_mode='Markdown')  
    elif text.isdigit() and len(text) == 10:
        await process_request(update, context)
    else:
        # Agar user ne join kar rakha hai but invalid input diya
        await update.message.reply_text("❌ Please send a valid 10-digit number.")

# ==================== PROCESS REQUEST ====================

async def process_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    number = update.message.text.strip()
    processing_msg = await update.message.reply_text("🔍 *Searching Database...*", parse_mode='Markdown')  
    
    try:
        response = requests.get(f"{API_BASE}{number}", headers=HEADERS, timeout=30)
        data = response.json()
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=processing_msg.message_id)

        if not data:
            await update.message.reply_text(f"⚠️ No data found for {number}.")
            return

        # 1. JSON FILE GENERATE
        json_content = json.dumps(data, indent=4, ensure_ascii=False)
        json_file = io.BytesIO(json_content.encode('utf-8'))
        json_file.name = f"result_{number}.json"

        # 2. TEXT REPORT FORMATTING
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records = data if isinstance(data, list) else [data]
        
        report = "🛡️ **WELCOME TO THE NETWORK WORLD OF THE SATISH** 🛡️\n\n"
        report += f"🎯 **TARGET**: `{number}`\n"
        
        for i, r in enumerate(records, 1):
            report += f"👤 **NAME**: {r.get('name', 'N/A')}\n"
            report += f"👨‍👦 **FATHER**: {r.get('father_name', 'N/A')}\n"
            report += f"🏠 **ADDRESS**: {r.get('address', 'N/A')}\n"
            if 'alt_mobile' in r: report += f"📞 **ALT NO**: {r.get('alt_mobile', 'N/A')}\n"
            if i < len(records): report += "--------------------------------\n"

        report += f"\n⏰ **TIME**: {current_time}\n"
        report += f"🗃️ **RECORDS**: {len(records)}\n"
        report += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        report += "🔐 **END OF REPORT**"

        # 3. SEND ALL
        await update.message.reply_document(document=json_file, caption="📂 **JSON Data File**", parse_mode='Markdown')
        await update.message.reply_text(report, parse_mode='Markdown')
        await update.message.reply_text("Note:- Open file for id 🆔 number or more information")

    except Exception as e:
        await update.message.reply_text(f"❌ System Error: {str(e)}")

# ==================== MAIN ====================

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("broadcast", broadcast)) 
    application.add_handler(CommandHandler("userlist", send_user_list)) 
    application.add_handler(CommandHandler("laxmi", send_message_log)) 
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🚀 Bot is live with Fixed Admin Commands...")
    application.run_polling()

if __name__ == "__main__":
    main()

