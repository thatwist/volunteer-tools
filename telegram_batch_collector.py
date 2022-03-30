import os
import logging

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import Message

from schema import posts_schema
from model import Post
from api import date_bucket
from typesense_utils import init_typesense_client, delete_collection_if_exists


def telegram_itr_msg_to_post(m: Message) -> Post:

    return Post(title = m.message[0:69] if m.message is not None else None,
                date = str(m.date),
                date_bucket = date_bucket(m.date.replace(tzinfo=None)),
                ts = m.date.timestamp(),
                category = "other",
                channel = m.chat.username,
                channel_id = m.chat.id,
                channel_title = m.chat.title if hasattr(m.chat, 'title') else m.chat.username,
                platform = "tg-channel",
                post_id = m.id,
                views = m.views,
                description = m.message[0:200] if m.message is not None else None,
                message = m.message,
                link = f"https://t.me/{m.chat.username}/{m.id}",
                author = m.post_author
                )

from itertools import islice

# to batch collection into buckets, typesense timeouts on importing big collections
def batcher(iterable, batch_size):
    iterator = iter(iterable)
    while batch := list(islice(iterator, batch_size)):
        yield batch

if __name__ == '__main__':

    # chats = [-1001613584371, -1001601141641]  the other way is to specify chats ids
    chats = [
        "andriysadovyi", 
        "AngelsOfUkraine",
        "ArmyNeeds",
        "avtodopomaga",
        "bazuwork",
        "boguslav_sos",
        "burlv",
        "chornamary", 
        "DMYTROLUNIN", 
        "DzvinokDruguBot", 
        "evacuationukraine",
        "gruz_200_rus", 
        "help_cv",
        "helptoukrainegroup",
        "HelpTranskarpatiaLodging",
        "helpvolonter",
        "helpzakarpattia",
        "Hotovyi_do_vsioho_bot",
        "house_cv",
        "huiiivoiiine",
        "ihor_terekhov", 
        "khersonskaODA", 
        "khm_gov_ua", 
        "khmelnytskaODA", 
        "kiber_oborona_ua",
        "kozytskyy_maksym_official", 
        "lobbyx",
        "lobbyxIT",
        "luhanskaVTSA", 
        "Lviv_help",
        "lviv_stryi",
        "mariupolrada", 
        "medhelpinfo",
        "medlogistic",
        "nampodorozi_bot",
        "neruhomistrus", 
        "opitpomoshi",
        "palyanycya_zp",
        "pavlokyrylenko_donoda", 
        "pick_up_ukraine",
        "pidvezu_cv", 
        "poshuk_znyklyh",
        "realtor_cv", 
        "rentCV", 
        "rf200_now", 
        "saveua_bot",
        "shostka_volunteer_center",
        "sm_vca", 
        "stop_russian_war_bot",
        "synegubov", 
        "ternopilskaODA", 
        "UAhelpinfo",
        "uajobnow",
        "ukr_emigration",
        "UkrzalInfo",
        "uzhvolunteer",
        "v_tylu", 
        "valanteruparus141",
        "vin_sleep", 
        "vinnytskaODA", 
        "VollunteerUA",
        "volonteri_ua",
        "volonterniko",
        "volontery_kh",
        "volovodii",
        "VolunteerCountry",
        "VolunteersHotlineBot",
        "VolunteerTalks",
        "VolunteerTalksBrovary",
        "VolunteerTalksCherkasy",
        "VolunteerTalksChernihiv",
        "VolunteerTalksChernivtsi",
        "VolunteerTalksDnipro",
        "VolunteerTalksDrohobych",
        "VolunteerTalksGorishniPlavni",
        "VolunteerTalksIF",
        "VolunteerTalksIrpin", 
        "VolunteerTalksKamianske",
        "VolunteerTalksKharkiv",
        "VolunteerTalksKherson",
        "VolunteerTalksKhmelnytskyi",
        "VolunteerTalksKramatorsk",
        "VolunteerTalksKremenchuk",
        "VolunteerTalksKrp",
        "VolunteerTalksKryvyiRih",
        "VolunteerTalksKyiv",
        "VolunteerTalksLutsk",
        "VolunteerTalksLviv",
        "VolunteerTalksMariupol",
        "VolunteerTalksMelitopol",
        "VolunteerTalksMykolaiv",
        "VolunteerTalksOdesa",
        "VolunteerTalksOleksandriia", 
        "VolunteerTalksOstroh", 
        "VolunteerTalksPoltava",
        "VolunteerTalksRivne",
        # "VolunteerTalksRozdilna", # there is some problem with this one
        "VolunteerTalksShid",
        "VolunteerTalksSumy",
        "VolunteerTalksTernopil",
        "VolunteerTalksUzhgorod",
        "VolunteerTalksVin",
        "VolunteerTalksZhytomyr",
        "VolunteerTalksZmerynka",
        "VolunteerTalksZP",
        "volynskaODA", 
        "vszu_ua",
        "winwin_realty",
        "zak_help", 
        # "zevolunteers", # same story
        "Zhyvytskyy", 
    ]

    load_dotenv()

    typesense_client = init_typesense_client(os.getenv('TYPESENSE_HOST'),
                                             os.getenv('TYPESENSE_PORT'),
                                             os.getenv('TYPESENSE_PROTOCOL'),
                                             os.getenv('TYPESENSE_API_KEY'))

    logging.getLogger().setLevel(logging.INFO)

    if (os.getenv("TYPESENSE_DROP_AND_RECREATE_POSTS").lower() == "true"):
        print(f"[TYPESENSE][COLLECTION] Recreating collection: {posts_schema['name']}")
        delete_collection_if_exists(typesense_client, posts_schema['name'])
        typesense_client.collections.create(posts_schema)

    with TelegramClient(os.getenv('TG_NAME'), int(os.getenv('API_ID')), os.getenv('API_HASH')) as tg_client:
        with tg_client.takeout() as takeout:
            for chat in chats:
                print(f"scraping chat '{chat}'")
                last_post = typesense_client.collections["posts"].documents.search(search_parameters =
                        {"q" : "*",
                         "filter_by": f"channel:={chat}",
                         "include_fields": "post_id",
                         "page": 1,
                         "per_page": 1,
                         "limit_hits": 1,
                         "sort_by": "post_id:desc"})
                if len(last_post["hits"]) > 0:
                    last_id = last_post["hits"][0]["document"]["post_id"]
                else:
                    last_id = 0
                print(f"will scrape starting from msg_id={last_id}")

                iter_msgs = takeout.iter_messages(chat,
                                                  wait_time=0,
                                                  limit=int(os.getenv("TYPESENSE_BATCH_LOAD_MESSAGE_LIMIT")),
                                                  min_id=last_id
                                                  )
                all_messages = list(filter(lambda post: (len(post.message) if post.message is not None else 0) >= 50,
                                           map(telegram_itr_msg_to_post, iter_msgs)))
                if len(all_messages) > 0:
                    for messages in batcher(all_messages, 100):
                        non_empty_msgs = list(filter(lambda x: x.is_non_empty_message(), messages))
                        message_dicts = list(map(lambda x: x.__dict__, non_empty_msgs))
                        import_result = typesense_client.collections["posts"].documents.import_(message_dicts, params={"batch_size": 50})
                        print(
                            f"[TYPESENSE][IMPORT] from tg channel: {chat}, {len(non_empty_msgs)} messages,"
                            + f"result = {import_result[:10]}....")
                else:
                    print("nothing to scrape, all set")

