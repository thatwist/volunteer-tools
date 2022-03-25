from facebook_scraper import get_posts

for post in get_posts('groups/rovno.online', pages=1):
    print(post['text'][:50])
