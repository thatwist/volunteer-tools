
posts_schema = {
    'name': 'posts',

    'fields': [
        {'name': 'title', 'type': 'string', 'locale': 'uk'},
        {'name': 'date', 'type': 'string'},
        {'name': 'date_bucket', 'type': 'int32', 'facet': True},
        {'name': 'ts', 'type': 'float'},
        {'name': 'category', 'type': 'string', 'facet': True, 'locale': 'uk'},
        {'name': 'channel', 'type': 'string', 'facet': True},
        {'name': 'platform', 'type': 'string', 'facet': True},
        {'name': 'post_id', 'type': 'int32'},
        {'name': 'views', 'type': 'int32', "optional": True},
        {'name': 'description', 'type': 'string', 'locale': 'uk'},
        {'name': 'message', 'type': 'string', 'locale': 'uk'},
        {'name': 'link', 'type': 'string'},

    ],
    "default_sorting_field": "ts"
}
