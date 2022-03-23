from dataclasses import dataclass


@dataclass
class Post:
    """ telegram message, facebook post, scraped website post, etc """
    id: str
    platform: str
    platform_channel: str  # telegram channel, fb group, etc
    message: str
    link: str
    ts: float

    def is_non_empty_message(self):
        return self.message is not None and self.message != ''
