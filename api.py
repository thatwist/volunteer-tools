import os
from flask import Flask, json, send_from_directory, request
from flask.helpers import safe_join
from telethon.sync import TelegramClient

api = Flask(__name__)
static = safe_join(os.path.dirname(__file__), '')
api.config['JSON_AS_ASCII'] = False

name = 'twist522' 
api_id = '9673715'
api_hash = "c5cb33921c1e5ee10394c58a1f1a3eb1" 

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

@api.route('/search', methods=['GET'])
async def get_results():
  query = request.args.get("query")
  async with TelegramClient(name, api_id, api_hash) as client:
    data = []
    for chat in chats:
      print(f"searching {chat}...")
      async for message in client.iter_messages(entity = chat, search = query):
        #print(dir(message))
        #print(message.sender_id, ':', message.text)
        # todo - this could be a configuration
        # 'id', 'peer_id', 'date', 'message', 'out', 'mentioned', 'media_unread', 'silent', 'post', 'from_scheduled',
        # 'legacy', 'edit_hide', 'pinned', 'from_id', 'fwd_from', 'via_bot_id', 'reply_to', 'media', 'reply_markup',
        # 'entities','views','forwards','replies','edit_date','post_author','grouped_id','restriction_reason','ttl_period'
        # todo - view layer?
        msg = message.to_dict()
        msg_dict = {x: msg[x] for x in ["id", "message", "views", "date"]}
        msg_dict["channel"]=chat
        msg_dict["platform"]="tg-channel"
        msg_dict["category"]="other"
        msg_dict["title"] = msg_dict["message"][0:50]
        msg_dict["description"] = msg_dict["message"][0:200]
        msg_dict["full_description"] = msg_dict["message"]
        msg_id = msg_dict["id"]
        msg_dict["link"]=f"https://t.me/{chat}/{msg_id}"
        data.append(msg_dict)
        #print(msg_dict)
    return json.dumps(data)

@api.route('/')
def _home():
  return send_from_directory(static, 'search.html')

# route static resources
@api.route('/<path:path>')
def _static(path):
  if os.path.isdir(safe_join(static, path)):
    path = os.path.join(path, 'index.html')
  return send_from_directory(static, path)

if __name__ == '__main__':
    api.run(debug=True) # debug for auto-reload
