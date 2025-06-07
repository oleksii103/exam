import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from localization import gb_localization, ua_localization

load_dotenv("token.env")
TOKEN = os.getenv("BOT_TOKEN")

user_ids = set()  # <-- зберігаємо chat_id для розсилки

language_menu = ReplyKeyboardMarkup(
    keyboard=[["🇬🇧 English", "🇺🇦 Українська"]],
    resize_keyboard=True,
    one_time_keyboard=True
)

def get_main_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[lang["Donate"], lang["Portfolio"], lang["Option"]]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_sub_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[lang["BackToMenu"]], [lang["Info"], lang["Help"]]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_options_menu(lang):
    return ReplyKeyboardMarkup(
        keyboard=[[lang["Reset"]], [lang["BackToMenu"]]],
        resize_keyboard=True,
        one_time_keyboard=False
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        context.user_data.clear()
        user_ids.add(update.effective_chat.id)  # Додаємо до списку для розсилки
        await update.message.reply_text(
            "Please select your language / Будь ласка, оберіть мову:",
            reply_markup=language_menu
        )

async def clear_previous_bot_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    msg_id = context.user_data.get("last_bot_message_id")
    if msg_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception as e:
            print(f"Failed to delete message: {e}")
        context.user_data["last_bot_message_id"] = None

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", gb_localization)
    await update.message.reply_text(
        lang["ResetingMes"],
        reply_markup=language_menu
    )
    if update.message:
        context.user_data.clear()

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", gb_localization)
    text = "Choose one option:" if lang == gb_localization else "Оберіть одну з опцій:"
    await update.message.reply_text(text, reply_markup=get_main_menu(lang))

async def show_options_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", gb_localization)
    await update.message.reply_text(lang["OptionMes"], reply_markup=get_options_menu(lang))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    chat_id = update.message.chat_id
    user_ids.add(chat_id)  # також додаємо сюди, якщо ще не був доданий

    if msg == "🇬🇧 English":
        context.user_data["lang"] = gb_localization
        await update.message.reply_text(gb_localization["LocalMes"])
        await show_main_menu(update, context)
        return
    elif msg == "🇺🇦 Українська":
        context.user_data["lang"] = ua_localization
        await update.message.reply_text(ua_localization["LocalMes"])
        await show_main_menu(update, context)
        return

    lang = context.user_data.get("lang")
    if not lang:
        await update.message.reply_text("Please select a language first / Спочатку оберіть мову:")
        return

    if msg in ["💳 Donate", "💳 Донат"]:
        sent_msg = await update.message.reply_text(lang["DonateMes"], parse_mode="Markdown", reply_markup=get_sub_menu(lang))
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    elif msg in ["📁 Portfolio", "📁 Портфоліо"]:
        sent_msg = await update.message.reply_text(lang["PortfolioMes"], parse_mode="Markdown", reply_markup=get_sub_menu(lang))
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    elif msg in ["⚙️ Options", "⚙️ Опції"]:
        await show_options_menu(update, context)

    elif msg in ["🔄 Change Language", "🔄 Змінити мову"]:
        await restart(update, context)

    elif msg in ["🔙 Back to main menu", "🔙 Назад до головного меню"]:
        await clear_previous_bot_message(update, context)
        await show_main_menu(update, context)

    elif msg in ["ℹ️ Info", "ℹ️ Інфо"]:
        sent_msg = await update.message.reply_text(lang["InfoMes"])
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    elif msg in ["❓ Help", "❓ Допомога"]:
        sent_msg = await update.message.reply_text(lang["HelpMes"])
        context.user_data["last_bot_message_id"] = sent_msg.message_id

    else:
        await update.message.reply_text(lang["Error"])

# 🕒 Функція періодичної розсилки
async def broadcast_message(application):
    while True:
        for chat_id in user_ids:
            try:
                await application.bot.send_message(chat_id=chat_id, text="⏰ Нагадування: кожні 90 хвилин!")
            except Exception as e:
                print(f"Помилка при надсиланні повідомлення до {chat_id}: {e}")
        await asyncio.sleep(1 * 60)  # 90 хвилин
 
# 🔁 Після запуску додатку запускаємо розсилку
async def on_startup(application):
    asyncio.create_task(broadcast_message(application))

# 🚀 Запуск бота
app = ApplicationBuilder().token(TOKEN).post_init(on_startup).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling()
