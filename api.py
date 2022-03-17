import os
import flask
from flask import Flask, send_from_directory, request
import json
from flask.helpers import safe_join
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api = Flask(__name__)
static = safe_join(os.path.dirname(__file__), '')
api.config['JSON_AS_ASCII'] = False

tg_name = os.getenv('TG_NAME')
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

chats=[
    "poshuk_znyklyh",
    "VolunteerTalksKyiv",
    "AngelsOfUkraine",
    "ArmyNeeds",
    "medhelpinfo",
    "opitpomoshi",
    "huiiivoiiine",
    "evacuationukraine",
    "UkrzalInfo"
]

async def teleQuery(query = None, limit = None):
  async with TelegramClient(tg_name, api_id, api_hash) as client:
    data = []
    for chat in chats:
      print(f"searching {chat}...")
      async for message in client.iter_messages(entity = chat, search = query, limit = limit):
        #print(dir(message))
        #print(message.sender_id, ':', message.text)
        # todo - this could be a configuration
        # 'id', 'peer_id', 'date', 'message', 'out', 'mentioned', 'media_unread', 'silent', 'post', 'from_scheduled',
        # 'legacy', 'edit_hide', 'pinned', 'from_id', 'fwd_from', 'via_bot_id', 'reply_to', 'media', 'reply_markup',
        # 'entities','views','forwards','replies','edit_date','post_author','grouped_id','restriction_reason','ttl_period'
        # todo - view layer?
        msg = message.to_dict()
        if not msg.get("message"):
          continue
        msg_dict = {x: msg[x] for x in ["id", "message", "views", "date"]}
        msg_dict["channel"]=chat
        msg_dict["ts"]=msg_dict["date"].timestamp()
        msg_dict["platform"]="tg-channel"
        msg_dict["category"]="other"
        msg_dict["post_id"] = msg_dict["id"]
        msg_dict["title"] = msg_dict["message"][0:50]
        msg_dict["description"] = msg_dict["message"][0:200]
        msg_dict["full_description"] = msg_dict["message"]
        msg_id = msg_dict["id"]
        msg_dict["link"]=f"https://t.me/{chat}/{msg_id}"
        msg_dict.pop("id")
        data.append(msg_dict)
        #print(msg_dict)
    return data

async def teleDump():
  data = await teleQuery(query = None, limit = 100)
  with open("dump.json",'w') as f:
    f.write(json.dumps(data, indent=4, sort_keys=True, default=str, ensure_ascii=False))

def dump():
  import asyncio
  loop = asyncio.get_event_loop()
  loop.run_until_complete(teleDump())

@api.route('/search', methods=['GET'])
async def get_results():
  query = request.args.get("query")
  data = await teleQuery(query)
  return flask.json.dumps(data)

@api.route('/')
def _home():
  return send_from_directory(static, 'search.html')

# route static resources
@api.route('/<path:path>')
def _static(path):
  if os.path.isdir(safe_join(static, path)):
    path = os.path.join(path, 'search.html')
  return send_from_directory(static, path)

if __name__ == '__main__':
    api.run(debug=True) # debug for auto-reload
