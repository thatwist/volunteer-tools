from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class Post:
  """ telegram message, facebook post, scraped website post, etc """
  title: str
  date: str
  date_bucket: int # to filter out only latest
  ts: float
  category: str
  channel: str # channel.ref
  platform: str
  post_id: int # platform+channel+post_id = unique
  views: Optional[int]
  description: str
  message: str # todo - rename to text
  # text: str
  link: str
  hidden: bool = False # e.g. amunition might be hidden
  post_type: str = "todo" # потреба чи пропозиція чи новина чи булшіт
  geo: Optional[str] = None # can be list, e.g. ride from->to or multiple locations
  #tags: list[str] = []

  def is_non_empty_message(self):
    return self.message is not None and self.message != ''

@dataclass
class Channel:
  platform: str
  ref: str # e.g. for telegram - id of the group, platform+ref = unique
  title: str
  link: str # todo - this can be derived, method to override?
  size: int # audience size, how many people, todo - this one is dynamic, so should be periodically updated
  # meta
  category: Optional[str] = None
  #tags: list[str] = []
  geo: Optional[str] = None
