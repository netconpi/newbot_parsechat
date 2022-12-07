
from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        "Привет! Добро пожаловать в Трекер-предложений."
        " Для добавления в список рассылки напиши: /add_me",
    )

