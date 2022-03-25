from model import Post
from dataclasses import dataclass, replace, asdict
from abc import ABC, abstractmethod
import re

class Rule(ABC):
    @abstractmethod
    def analyze(self, post: Post):
        pass
 
@dataclass
class RegexpRule(Rule):
    
    def __init__(self, regexps: dict[str, list[str]], update: dict[str, str]):
       self.regexps = regexps
       self.update = update

    def analyze(self, post: Post) -> Post:
        print(f"regexps {regexps}")
        post_dict = asdict(post)
        for k, v in regexps.items():
            for r in v:
                pattern = re.compile(r) # todo compile once
                if re.search(pattern, post_dict[k]):
                    print(f"match {pattern} in {post_dict[k]}")
                    return replace(post, **update)
        return post
 
rules = [
    RegexpRule({ "text": ["київ"] }, { "geo": "київ" }),
    # hide ammunition
    RegexpRule({ "text": ["бронік", "бронежилет", ""] }, { "hidden": True }),
]

def analyze(p: Post) -> Post:
    updated = p
    for rule in rules:
        updated = rule.analyze(updated)
