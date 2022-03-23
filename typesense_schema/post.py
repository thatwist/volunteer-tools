posts_schema = {
    'name': 'posts',
    'fields': [
        # Document's `id` field must be a string.
        {'name': 'id', 'type': 'string'},
        {'name': 'platform', 'type': 'string'},
        {'name': 'platform_channel', 'type': 'string', 'locale': 'uk'},
        {'name': 'message', 'type': 'string', 'locale': 'uk'},
        {'name': 'link', 'type': 'string'},
        {'name': 'ts', 'type': 'float'},
    ],
    "default_sorting_field": "ts"
}
