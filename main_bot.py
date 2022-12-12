
# After message checker is running 
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

import json
import actions

# Read base properties 
file = open("settings.json")
configuration = json.load(file)



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(configuration['bot_token']).build()

    application.add_handler(
        CommandHandler(
            'start', 
            actions.start,
        )
    )

    application.add_handler(
        CommandHandler(
            'add_me', 
            actions.addme,
        )
    )

    # Check actions.py | block: remove/add user

    addremove_user = ConversationHandler(
        entry_points=[CommandHandler('user_admin', actions.start_admin)],
        states={
            actions.SELECT_UU: [
                MessageHandler(
                    filters.COMMAND,
                    actions.command_called,
                )
            ],
            actions.ACTION_UU: [
                CallbackQueryHandler(actions.delete_user, pattern="^Delete$"),
                CallbackQueryHandler(actions.close, pattern="^Close$"),
                CallbackQueryHandler(actions.add_accs, pattern="^Add_Accses$"),
            ]
        },
        fallbacks=[CommandHandler('close', actions.close_all)],
    )

    application.add_handler(addremove_user)

    # Check actions.py | block: remove/add keywords (kw)

    addremove_keyword = ConversationHandler(
        entry_points=[CommandHandler('kw', actions.selector_kw_type)],
        states={
            actions.SELECT_KW_TP: [
                CallbackQueryHandler(actions.mins_edit, pattern="^minus_type$"),
                CallbackQueryHandler(actions.key_edit, pattern="^key_type$"),
                CallbackQueryHandler(actions.close, pattern="^Close$"),
            ],
            actions.ACT_KW: [
                CallbackQueryHandler(actions.add_kw, pattern="^add_word$"),
                CallbackQueryHandler(actions.remove_kw, pattern="^remove_word$"),
                CallbackQueryHandler(actions.view_kw, pattern="^view_word$"),
                CallbackQueryHandler(actions.close, pattern="^Close$"),
            ],
            actions.VIEW_L_KW: [
                CallbackQueryHandler(actions.next_page, pattern="^next_pg$"),
                CallbackQueryHandler(actions.prev_page, pattern="^prev_pg$"),
                CallbackQueryHandler(actions.close, pattern="^Close$"),
            ],
            actions.ADD_PROC_KW: [
                MessageHandler(filters.TEXT, actions.record_word),
            ],
            actions.REMOVE_PROV_KW: [
                MessageHandler(filters.TEXT, actions.rec_rm_word),
            ],
            actions.CONFIRM_KW: [
                CallbackQueryHandler(actions.confirm_kw, pattern="^conf$"),
                CallbackQueryHandler(actions.forget_kw, pattern="^forget$"),
            ]
        },
        fallbacks=[CommandHandler('close', actions.close_all)],
    )

    application.add_handler(addremove_keyword)

    application.add_handler(
        MessageHandler(
            (filters.COMMAND & filters.Regex("^/contact_[0-9]+$")),
            actions.contact,
        )
    )


    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

