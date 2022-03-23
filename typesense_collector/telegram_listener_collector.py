import os
from datetime import datetime

from dotenv import load_dotenv
from telethon import events, TelegramClient
from telethon.events import NewMessage
from model.post import Post

from typesense_schema.post import posts_schema
from typesense_utils.typesense_utils import init_typesense_client

def telegram_event_to_post(event: NewMessage.Event) -> Post:
    return Post(str(event.message.id),
                "telegram",
                event.chat.title,
                event.message.message,
                # todo may throw an exception for private chats
                f"https://t.me/{event.chat.title}/{event.message.id}",
                datetime.timestamp(event.message.date))


if __name__ == '__main__':
    # chat ids
    chats = [-1001613584371, -1001601141641]

    load_dotenv()

    print("goo")
    typesense_client = init_typesense_client(os.getenv('TYPESENSE_HOST'),
                                             os.getenv('TYPESENSE_PORT'),
                                             os.getenv('TYPESENSE_PROTOCOL'),
                                             os.getenv('TYPESENSE_API_KEY'))

    with TelegramClient(os.getenv('TG_NAME'), int(os.getenv('API_ID')), os.getenv('API_HASH')) as tg_client:
        print(f"[TELEGRAM][LISTENER] started listening to chats: {chats}")


        @tg_client.on(events.NewMessage(chats=chats))
        async def new_message_handler(event: NewMessage.Event):
            post = telegram_event_to_post(event)

            if post.is_non_empty_message():
                typesense_client.collections[posts_schema["name"]].documents.import_(post.__dict__)

        tg_client.start()
        tg_client.run_until_disconnected()
