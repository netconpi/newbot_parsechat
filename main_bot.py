
# After message checker is running 
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

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


    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

