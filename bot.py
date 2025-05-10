import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["🔹 option 1", "🔸 option 2", "⚙️ option 3"],
        ["🔄 Reset"]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

sub_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["🔙 Back to main menu"],
        ["ℹ️ Info", "❓ Help"]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Hello, I’m your bot 🙂\nChoose one option:",
            reply_markup=main_menu
        )

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("🔄 Reseting Bot...")
        await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == "🔹 option 1":
        await update.message.reply_text("You selected Option 1 🔹", reply_markup=sub_menu)
    elif msg == "🔸 option 2":
        await update.message.reply_text("You selected Option 2 🔸", reply_markup=sub_menu)
    elif msg == "⚙️ option 3":
        await update.message.reply_text("You selected Option 3 ⚙️", reply_markup=sub_menu)
    elif msg == "🔄 Reset":
        await restart(update, context)
    elif msg == "🔙 Back to main menu":
        await start(update, context)
    elif msg == "ℹ️ Info":
        await update.message.reply_text("ℹ️ This is some information.")
    elif msg == "❓ Help":
        await update.message.reply_text("❓ This is the help section.")
    else:
        await update.message.reply_text("⚠️ Unknown command. Please choose from the menu.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

app.run_polling()
