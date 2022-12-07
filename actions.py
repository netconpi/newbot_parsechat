
from telegram import Update
from telegram.ext import ContextTypes

import db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Just message reply on cmd /start with small instrct. """

    await update.message.reply_text(
        "Привет! Добро пожаловать в Трекер-предложений."
        " Для добавления в список рассылки напиши: /add_me",
    )



async def addme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        "Я направил запрос на добавления тебя в рассылку"
        " Если его подтвердит владелец бота, то ты сможешь"
        f" получать рассылку \n\t"
        f"Ваш ID: {update.message.from_user.id}\n\t"
        f"Имя: {update.message.from_user.first_name}"
    )

    db.add_me(update.message.from_user.id)


