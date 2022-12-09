
import json
import key_words
import db

# Read base properties 
file = open("settings.json")
configuration = json.load(file)

# Import the client
from telethon import TelegramClient, events, utils
import asyncio
import re

# Define some variables so the code reads easier
# session = os.environ.get('TG_SESSION', 'printer')
api_id = int(configuration['api_id'])
api_hash = configuration['api_hash']


# Use the client in a `with` block. It calls `start/disconnect` automatically.
client = TelegramClient('anon', api_id, api_hash).start()


@client.on(events.NewMessage)
async def new_message(event):
    # Get information about sender 
    sender = await event.get_sender()
    name = utils.get_display_name(sender)
    telegram_from = utils.get_input_user(sender).user_id
    print(name, telegram_from)

    kw_list = db.get_kw_list()
    kw_min_list = db.get_kw_min_list()

    got_text = event.raw_text.lower()
    fin_text = re.sub("[^A-Za-zА-Яа-я0-9 ]+", " ", got_text)
    for i in kw_list:
        if i in got_text:
            for j in kw_min_list:
                if not (j in got_text):
                    db.add_offer(name, telegram_from, fin_text, 'Без источника')
                    break

    # Handler text from sender 


try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
finally:
    client.disconnect()
