# volunteer-tools

Aggregated search tools, originally developed for volunteering needs in Ukraine-Russia war

## how to run

install requirements

    pip3 install -r requirements.txt
    
create telegram api keys

create `.env` file with following contents

    TG_NAME=<tg-user-name>
    API_ID=..
    API_HASH=..
    
    TYPESENSE_HOST=..
    TYPESENSE_PORT=..
    TYPESENSE_PROTOCOL=http or https
    TYPESENSE_API_KEY=..

    TYPESENSE_DROP_AND_RECREATE_POSTS=true or false
    TYPESENSE_BATCH_LOAD_MESSAGE_LIMIT= how many messages to load from each chat

run api:
    
    python api.py

run typesense (version with cyrillic fix): 

     docker run -p 8108:8108 -v/tmp/data:/data typesense/typesense:0.23.0.rc8  --data-dir /data --api-key=Hu52dwsas2AdxdE


## Typesense collector
[telegram to typesense: batch collector ](typesense_collector/telegram_listener_collector.py)

[telegram to typesense: listener collector ](typesense_collector/telegram_batch_collector.py)
 
## client examples 

Examples for telegram/typesense/etc clients: 

- how to find telegram chat id (required for listener collector) 
- how to search in typesense (required for future API) 

## to clean some old documents

    curl -H "X-TYPESENSE-API-KEY: <api-key>" -X DELETE "https://typesense.uall.me:8108/collections/posts/documents?q=*&filter_by=ts:<1645734541"
