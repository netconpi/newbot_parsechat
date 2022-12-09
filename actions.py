
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

import db


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Just message reply on cmd /start with small instrct. """

    await update.message.reply_text(
        "Привет! Добро пожаловать в Трекер-предложений."
        " Для добавления в список рассылки напиши: /add_me",
    )




# TODO: Get mail

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# TODO: Add/Remove allowed_users


async def addme(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.message.reply_text(
        "Я направил запрос на добавления тебя в рассылку"
        " Если его подтвердит владелец бота, то ты сможешь"
        f" получать рассылку \n\t"
        f"Ваш ID: {update.message.from_user.id}\n\t"
        f"Имя: {update.message.from_user.first_name}"
    )

    db.add_me(update.message.from_user.id)

ACTION_UU, SELECT_UU, CONFIRM_UU = range(3)

async def start_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    garanted, req_users = db.get_all_users()
    txt_users = ""

    txt_users += "\n\t📥 Список запросов: \n\t"
    for i in req_users:
        txt_users += f"/edit_{i[0]} \n\t"

    txt_users += "💳 Список доступов: \n\t"
    for i in garanted:
        txt_users += f"/edit_{i[0]}\n\t"

    await update.message.reply_text(
        "Выберите пользователя из списка: "
        f"{txt_users}"
        "⚠️ Для отмены операции выбери любого пользователя, а потом отмени!"
    )

    return SELECT_UU


async def command_called(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.text[1:].split('_')[-1]
    # print(user_id)

    # TODO: If req
    # TODO: If garanted 

    if db.checkuser_status(user_id):
        keyboard = [
            [
                InlineKeyboardButton("Удалить доступ", callback_data="Delete"),
                InlineKeyboardButton("Закрыть", callback_data="Close"),
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton("Отклонить", callback_data="Delete"),
                InlineKeyboardButton("Дать доступ", callback_data="Add_Accses"),
            ],
            [
                InlineKeyboardButton("Закрыть", callback_data="Close"),
            ]
        ]

    await update.message.reply_text(
        "Мы нашли данного пользователя: ",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    context.user_data['telegram_id'] = user_id

    return ACTION_UU


async def delete_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Операция успешно выполнена! ")
    db.remove_from_list(context.user_data['telegram_id'])
    return ConversationHandler.END


async def add_accs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Операция успешно выполнена! ")
    db.add_accs(context.user_data['telegram_id'])
    return ConversationHandler.END


async def close(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Пока!")
    return ConversationHandler.END

async def close_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    update.message.reply_text("Операция завершена")
    return ConversationHandler.END


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# TODO: Add/Remove keywords
ADD_KW, REMOVE_KW, ACT_KW, CONFIRM_KW, ADD_PROC_KW, REMOVE_PROV_KW = range(6)


# TODO: ask action type: remove or add or view
async def kw_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    keyboard = [
        [
            InlineKeyboardButton("Добавить слово", callback_data="add_word"),
            InlineKeyboardButton("Удалить слово", callback_data="remove_word"),
        ],
        [
            InlineKeyboardButton("Посмотреть слова", callback_data="view_word"),
            InlineKeyboardButton("Закрыть", callback_data="Close"),
        ]
    ]
    
    await update.message.reply_text(
        "Редактирование ключевых слов: "
        "\nВыберите, что вы хотите выполнить? ",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return ACT_KW


# TODO: what if add
async def add_kw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Отправь мне слово, а я его добавлю: ")
    context.user_data['proc_kw'] = {'action': 'add', 'word': ''}
    return ADD_PROC_KW


async def record_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    txt_user = update.message.text
    context.user_data['proc_kw']['word'] = txt_user

    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data="conf"),
            InlineKeyboardButton("Забыть", callback_data="forget"),
        ],
    ]

    await update.message.reply_text(
        "Я получил от тебя слово: \n\t"
        f"Ты действительно хочешь добавить {txt_user} "
        "в список ключевых слов?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return CONFIRM_KW


# TODO: what if remove
async def remove_kw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="ID! Направь ID, а я его удалю!: \n"
        f"{db.get_kw()}"
    )
    context.user_data['proc_kw'] = {'action': 'remove', 'word': ''}
    return REMOVE_PROV_KW


async def rec_rm_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    txt_user = update.message.text
    context.user_data['proc_kw']['word'] = db.get_word(txt_user)

    keyboard = [
        [
            InlineKeyboardButton("Да", callback_data="conf"),
            InlineKeyboardButton("Забыть", callback_data="forget"),
        ],
    ]

    await update.message.reply_text(
        "Я получил от тебя слово: \n\t"
        f"Ты действительно хочешь удалить {context.user_data['proc_kw']['word']} "
        "из списока ключевых слов?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    return CONFIRM_KW

# TODO: what if just view?
async def view_kw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"{db.get_kw()}")
    return ConversationHandler.END

# TODO: Comm methods
async def confirm_kw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Хорошо! Я выполнил данную операцию. Крайний срок внесения изменений 20 секунд")
    
    if context.user_data['proc_kw']['action'] == "add":
        db.add_kw(context.user_data['proc_kw']['word'])
    elif context.user_data['proc_kw']['action'] == "remove":
        db.remove_kw(context.user_data['proc_kw']['word'])
    
    return ConversationHandler.END

async def forget_kw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Ничего небыло! Все забыл <3")
    return ConversationHandler.END

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    txt_user = update.message.text[1:].split('_')[-1]
    await update.message.reply_text(
        f"<a href='https://web.telegram.org/k/#{txt_user}'>Написать!</a>",
        parse_mode='HTML',
    )

