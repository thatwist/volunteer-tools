import typesense
from typesense.exceptions import ObjectNotFound
import logging

logger = logging.getLogger(__name__)

def init_typesense_client(host, port, protocol, api_key):
    return typesense.Client({
        'nodes': [{
            'host': host,
            'port': port,
            'protocol': protocol
        }],
        'api_key': api_key,
        'connection_timeout_seconds': 2
    })


def delete_collection_if_exists(typesense_client, collection):
    print(f"deleting collection {collection}")
    try:
        typesense_client.collections[collection].delete()
    except ObjectNotFound:
        logger.warn(f"{collection} not found")
        pass
