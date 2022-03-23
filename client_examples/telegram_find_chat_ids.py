import os

from dotenv import load_dotenv
from telethon import TelegramClient

# works only if you are subscribed to the channel
if __name__ == '__main__':
    load_dotenv()

    channels_to_find = ["ВОЛОНТЕРИ | ЛЬВІВ", "DDOS атака на СЕПАРІВ (Кібер-Козаки)"]

    tg_name = os.getenv('TG_NAME')
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')

    with TelegramClient(tg_name, api_id, api_hash) as client:
        for dialog in client.iter_dialogs():
            if dialog.name in channels_to_find:
                print(dialog.name, "HAD IS = ", dialog.id)
