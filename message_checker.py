
import json
import key_words

# Read base properties 
file = open("settings.json")
configuration = json.load(file)

# Import the client
from telethon import TelegramClient, events, utils
import asyncio

# Define some variables so the code reads easier
# session = os.environ.get('TG_SESSION', 'printer')
api_id = int(configuration['api_id'])
api_hash = configuration['api_hash']


# Use the client in a `with` block. It calls `start/disconnect` automatically.
client = TelegramClient('anon', api_id, api_hash).start()


@client.on(events.NewMessage)
async def new_message(event):
    # Get information about sender 
    sender = sender = await event.get_sender()
    name = utils.get_display_name(sender)
    telegram_from = utils.get_input_user(sender).user_id
    print(name, telegram_from)

    got_text = event.raw_text.lower()
    for i in key_words.kwrd:
        if i in got_text:
            await client.send_message('me', f'@{name}; \ntg://user?id={telegram_from} \ntext: {got_text}')
            break

    # Handler text from sender 


try:
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()
finally:
    client.disconnect()
