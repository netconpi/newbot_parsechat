

import requests
import json
import db
import time

file = open("settings.json")
configuration = json.load(file)

TOKEN = configuration['bot_token']
mailing = db.get_mailing_list()

while 1:
    message = db.build_message()

    for i in mailing:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={i}&text={message}"
        print(requests.get(url).json())

    time.sleep(10)

