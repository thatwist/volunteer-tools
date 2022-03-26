import os

from dotenv import load_dotenv
from telethon import events, TelegramClient
from telethon.events import NewMessage

from api import date_bucket
from model import Post

from schema import posts_schema
from typesense_utils import init_typesense_client


def telegram_event_to_post(e: NewMessage.Event) -> Post:
    print('telegram_event_to_post')
    return Post(e.message.message[0:69] if e.message.message is not None else None,
                str(e.message.date),
                date_bucket(e.message.date.replace(tzinfo=None)),
                e.message.date.timestamp(),
                "telegram_post",
                e.chat.title,
                "tg-channel",
                e.message.id,
                e.views,
                e.message.message[0:200] if e.message.message is not None else None,
                e.message.message,
                f"https://t.me/{e.chat.title}/{e.message.id}")


if __name__ == '__main__':
    # chat ids
    #    chats = [-1001613584371, -1001601141641]
    # chats = [-1595917579]
    chats = [
       "coor_me",
       "poshuk_znyklyh",
       "VolunteerTalksKyiv",
       "AngelsOfUkraine",
       "ArmyNeeds",
       "medhelpinfo",
       "opitpomoshi",
       "huiiivoiiine",
       "evacuationukraine",
       "UkrzalInfo",
       "v_tylu",
       "pick_up_ukraine"
    ]
    print('before chats')
    load_dotenv()

    print("goo")
    typesense_client = init_typesense_client(os.getenv('TYPESENSE_HOST'),
                                             os.getenv('TYPESENSE_PORT'),
                                             os.getenv('TYPESENSE_PROTOCOL'),
                                             os.getenv('TYPESENSE_API_KEY'))

    with TelegramClient(os.getenv('TG_NAME'), int(os.getenv('API_ID')), os.getenv('API_HASH')) as tg_client:
        print(f"[TELEGRAM][LISTENER] started listening to chats: {chats}")

        print('before async')
        @tg_client.on(events.NewMessage(chats=chats))
        async def new_message_handler(event: NewMessage.Event):
            print('Before post')
            post = telegram_event_to_post(event)
            print('Post ye!')

            if post.is_non_empty_message():
                typesense_client.collections[posts_schema["name"]].documents.import_(post.__dict__)

        print('Before tg_client')
        tg_client.start()
        tg_client.run_until_disconnected()
