import json
import logging
from pathlib import Path
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Загружаем конфигурацию
with open("bot/config.json", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config["token"]

# Пути к контенту
ABOUT_PATH = Path(config["content"]["about"])
TEAM_PATH = Path(config["content"]["team"])
RESOURCES_PATH = Path(config["content"]["resources"])
JOURNAL_PATH = Path(config["content"]["journal"])

# Включаем логгирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я бот, связанный с проектной практикой.\n\n"
        "Доступные команды:\n"
        "/about — О проекте\n"
        "/team — Участники\n"
        "/resources — Полезные материалы\n"
        "/progress — Журнал прогресса"
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ABOUT_PATH.read_text(encoding="utf-8")
    await update.message.reply_text(text)

async def team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = json.loads(TEAM_PATH.read_text(encoding="utf-8"))
    text = "👥 Участники проекта:\n\n" + "\n".join(
        [f"• {member['name']} — {member['role']}" for member in data]
    )
    await update.message.reply_text(text)

async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = RESOURCES_PATH.read_text(encoding="utf-8")
    await update.message.reply_text("📚 Полезные ресурсы:\n\n" + text)

async def progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = JOURNAL_PATH.read_text(encoding="utf-8")
    await update.message.reply_text("🗓 Журнал прогресса:\n\n" + text)

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("team", team))
    app.add_handler(CommandHandler("resources", resources))
    app.add_handler(CommandHandler("progress", progress))

    app.run_polling()

if __name__ == "__main__":
    main()
