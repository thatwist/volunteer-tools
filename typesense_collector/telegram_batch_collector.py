import os
from datetime import datetime

from dotenv import load_dotenv
from telethon import TelegramClient

from model.post import Post
from telethon.tl.types import Message

from typesense_schema.post import posts_schema
from typesense_utils.typesense_utils import init_typesense_client, delete_collection_if_exists


def telegram_itr_msg_to_post(msg: Message) -> Post:
    return Post(str(msg.id),
                "telegram",
                msg.chat.title,
                msg.message,
                # todo may throw an exception for private chats
                f"https://t.me/{msg.chat.username}/{msg.id}",
                datetime.timestamp(msg.date))


if __name__ == '__main__':

    chats = ["AngelsOfUkraine", "VolunteerTalksKyiv"]
    # chats = [-1001613584371, -1001601141641] # also works with chat IDs

    load_dotenv()

    typesense_client = init_typesense_client(os.getenv('TYPESENSE_HOST'),
                                             os.getenv('TYPESENSE_PORT'),
                                             os.getenv('TYPESENSE_PROTOCOL'),
                                             os.getenv('TYPESENSE_API_KEY'))

    if bool(os.getenv("TYPESENSE_DROP_AND_RECREATE_POSTS")):
        print(f"[TYPESENSE][COLLECTION] Recreating collection: {posts_schema['name']}")
        delete_collection_if_exists(typesense_client, posts_schema['name'])
        typesense_client.collections.create(posts_schema)

    with TelegramClient(os.getenv('TG_NAME'), int(os.getenv('API_ID')), os.getenv('API_HASH')) as tg_client:

        with tg_client.takeout() as takeout:
            for chat in chats:
                iter_msgs = takeout.iter_messages(chat, wait_time=0,
                                                  limit=int(os.getenv("TYPESENSE_BATCH_LOAD_MESSAGE_LIMIT")))

                messages = map(telegram_itr_msg_to_post, iter_msgs)
                non_empty_msgs = filter(lambda x: x.is_non_empty_message(), messages)
                message_dicts = list(map(lambda x: x.__dict__, non_empty_msgs))

                import_result = typesense_client.collections[posts_schema["name"]].documents.import_(message_dicts)

                print(
                    f"[TYPESENSE][IMPORT] from tg channel: {chat}, {len(message_dicts)} messages, result = {import_result}")
