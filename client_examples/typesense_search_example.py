import os

import typesense
from dotenv import load_dotenv

from typesense_schema.post import posts_schema
from typesense_utils.typesense_utils import init_typesense_client

if __name__ == '__main__':
    load_dotenv()

    typesense_client = init_typesense_client(os.getenv('TYPESENSE_HOST'),
                                             os.getenv('TYPESENSE_PORT'),
                                             os.getenv('TYPESENSE_PROTOCOL'),
                                             os.getenv('TYPESENSE_API_KEY'))
    posts_collection = posts_schema["name"]

    # show all
    print(typesense_client.collections[posts_collection].documents.export())

    search_parameters = {
        'q': 'киЇв',
        'query_by': 'message'
    }

    # show search results
    print(typesense_client.collections[posts_collection].documents.search(search_parameters))
