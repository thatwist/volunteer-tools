from dataclasses import dataclass

@dataclass
class Post:
    """ telegram message, facebook post, scraped website post, etc """
    title: str
    date: str
    date_bucket: int
    ts: float
    category: str
    channel: str
    platform: str
    post_id: int
    view: int
    description: str
    message: str
    link: str

    def is_non_empty_message(self):
        return self.message is not None and self.message != ''
