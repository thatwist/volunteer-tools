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
  post_type: str # потреба чи пропозиція чи новина чи булшіт
  platform: str
  channel: str # channel.ref
  hidden: bool # e.g. amunition might be hidden
  post_id: int # platform+channel+post_id = unique
  views: Optional[int]
  text: str
  link: str
  geo: Optional[str] # can be list, e.g. ride from->to or multiple locations
  tags: list[str] = []

@dataclass
class Channel
  platform: str
  ref: str # e.g. for telegram - id of the group, platform+ref = unique
  title: str
  link: str # todo - this can be derived, method to override?
  size: int # audience size, how many people, todo - this one is dynamic, so should be periodically updated
  # meta
  category: Optional[str] = None
  tags: list[str] = []
  geo: Optional[str] = None
