import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv("token.env")
TOKEN = os.getenv("BOT_TOKEN")

# Клавіатура вибору мови
language_menu = ReplyKeyboardMarkup(
    keyboard=[
        ["🇬🇧 English", "🇺🇦 Українська"]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Головне меню залежно від мови
def get_main_menu(lang):
    if lang == "uk":
        return ReplyKeyboardMarkup(
            keyboard=[
                ["💳 Донат", "📁 Портфоліо", "⚙️ Опція 3"],
                ["🔄 Скинути"]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    return ReplyKeyboardMarkup(
        keyboard=[
            ["💳 Donate", "📁 Portfolio", "⚙️ option 3"],
            ["🔄 Reset"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

# Субменю залежно від мови
def get_sub_menu(lang):
    if lang == "uk":
        return ReplyKeyboardMarkup(
            keyboard=[
                ["🔙 Назад до головного меню"],
                ["ℹ️ Інфо", "❓ Допомога"]
            ],
            resize_keyboard=True,
            one_time_keyboard=False
        )
    return ReplyKeyboardMarkup(
        keyboard=[
            ["🔙 Back to main menu"],
            ["ℹ️ Info", "❓ Help"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        context.user_data.clear()
        await update.message.reply_text(
            "Please select your language / Будь ласка, оберіть мову:",
            reply_markup=language_menu
        )

# Очистка попереднього повідомлення бота
async def clear_previous_bot_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    msg_id = context.user_data.get("last_bot_message_id")

    if msg_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"Failed to delete message: {e}")
        context.user_data["last_bot_message_id"] = None

# Перезапуск
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        context.user_data.clear()
        await update.message.reply_text(
            "🔄 Resetting Bot...\nPlease select your language again:" if update.effective_user.language_code == "en"
            else "🔄 Скидання бота...\nБудь ласка, оберіть мову ще раз:",
            reply_markup=language_menu
        )

# Вивід головного меню
async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    text = "Choose one option:" if lang == "en" else "Оберіть одну з опцій:"
    await update.message.reply_text(text, reply_markup=get_main_menu(lang))

# Обробка повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    # Вибір мови
    if msg == "🇬🇧 English":
        context.user_data["lang"] = "en"
        await update.message.reply_text("Language set to English 🇬🇧")
        await show_main_menu(update, context)
        return
    elif msg == "🇺🇦 Українська":
        context.user_data["lang"] = "uk"
        await update.message.reply_text("Мову встановлено: Українська 🇺🇦")
        await show_main_menu(update, context)
        return

    lang = context.user_data.get("lang")
    if not lang:
        await update.message.reply_text("Please select a language first / Спочатку оберіть мову:")
        return

    chat_id = update.message.chat_id

    if msg in ["💳 Donate", "💳 Донат"]:
        donate_text = (
            "💳 *Support the project*\n"
            "You can donate to the following card:\n\n"
            "`1234 5678 9012 3456`\n\n"
            "Thank you for your support! 🙏"
            if lang == "en" else
            "💳 *Підтримайте проєкт*\n"
            "Ви можете надіслати донат на цю картку:\n\n"
            "`1234 5678 9012 3456`\n\n"
            "Дякуємо за вашу підтримку! 🙏"
        )
        sent_msg = await update.message.reply_text(donate_text, parse_mode="Markdown", reply_markup=get_sub_menu(lang))
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    elif msg in ["📁 Portfolio", "📁 Портфоліо"]:
        portfolio_text = (
            "📁 *My Portfolio*\nCheck out my work here:\nhttps://your-portfolio-link.com"
            if lang == "en" else
            "📁 *Моє портфоліо*\nОзнайомтеся з моїми роботами тут:\nhttps://your-portfolio-link.com"
        )
        sent_msg = await update.message.reply_text(portfolio_text, parse_mode="Markdown", reply_markup=get_sub_menu(lang))
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    elif msg in ["⚙️ option 3", "⚙️ Опція 3"]:
        sent_msg = await update.message.reply_text(
            "You selected Option 3 ⚙️" if lang == "en" else "Ви обрали Опцію 3 ⚙️",
            reply_markup=get_sub_menu(lang)
        )
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    elif msg in ["🔄 Reset", "🔄 Скинути"]:
        context.user_data.clear()
        await restart(update, context)

    elif msg in ["🔙 Back to main menu", "🔙 Назад до головного меню"]:
        await clear_previous_bot_message(update, context)
        await show_main_menu(update, context)

    elif msg in ["ℹ️ Info", "ℹ️ Інфо"]:
        sent_msg = await update.message.reply_text(
            "ℹ️ This is some information." if lang == "en" else "ℹ️ Це інформація."
        )
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    elif msg in ["❓ Help", "❓ Допомога"]:
        sent_msg = await update.message.reply_text(
            "❓ This is the help section." if lang == "en" else "❓ Це розділ допомоги."
        )
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    else:
        await update.message.reply_text(
            "⚠️ Unknown command. Please choose from the menu." if lang == "en"
            else "⚠️ Невідома команда. Будь ласка, оберіть з меню."
        )

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling()
