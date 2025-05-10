from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes



TOKEN = "8084005848:AAFru2eyroXl79CwLumjI53_euBIq8icmQc"

# button keyboard
main_menu = ReplyKeyboardMarkup(
    keyboard=[["🔹 option 1", "🔸 option 2", "⚙️ option 3"]],
    resize_keyboard=True,
    one_time_keyboard=False
)

# start command initialization
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "hello i`m your bot 🙂\nChoose one option:",
            reply_markup=main_menu
        )


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("🔄 Reseting Bot...")
        await start(update, context)  

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("restart", restart))

app.run_polling()
