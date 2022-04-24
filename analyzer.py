from model import Post
from dataclasses import dataclass, replace, asdict
from abc import ABC, abstractmethod
import re

class Rule(ABC):
    @abstractmethod
    def analyze(self, post: Post) -> Post:
        pass
 
@dataclass
class RegexpRule(Rule):
    
    def __init__(self, regexps: dict[str, list[str]], update: dict[str, str]):
       self.regexps = regexps
       self.update = update

    def analyze(self, post: Post) -> Post:
        print(f"regexps {self.regexps}")
        post_dict = asdict(post)
        for k, v in self.regexps.items():
            for r in v:
                pattern = re.compile(r) # todo compile once
                if re.search(pattern, post_dict[k]):
                    print(f"match {pattern} in {post_dict[k]}")
                    return replace(post, **self.update)
        return post
 
rules = [
    # geo
    RegexpRule({ "message": ["Київ"] }, { "geo": "київ" }),
    # infer category
    RegexpRule({ "message": ["гуманітарн"] }, { "category": "gum" }),
    # infer post type
    RegexpRule({ "message": ["Шукаю"] }, { "post_type": "need" }),
    # aux rules
    # hide ammunition
    RegexpRule({ "message": ["бронік", "бронежилет", ""] }, { "hidden": True }),
]


# simple test
from channels import telegram_channels_new

message1 = "#Київ #Україна\
\
Шукаю гуманітарні склади по Україні для виконання волонтерських запитів. \
\
Запити від:\
- багатодітних матерів\
- переселенці з дітками до 2х років! \
\
Що шукають: тільки дітки до 2х років!!! \
—Памперси \
—Пляшечки, соски\
—Суміш\
—Пюрешки фруктові \
—Продукти тривалого зберігання (Вермішельки, каші) \
—медикаменти\
—засоби гігієни\
—одяг /взуття \
\
Якщо у вас є інфо або ви безпосередньо представник складу, будь ласка, зв'яжіться зі мною🙏\
\
Мої контакти: Оксана, вайбер 0985767819 \
Для зв'язку 0934327366"

post1 = Post(
    title = message1[0:69],
    date = "2022-04-17 10:00:00",
    date_bucket = "1d",
    ts = 1111111111,
    category = None,
    channel = "vvolunteerskyiv",
    channel_id = "vvolunteerskyiv",
    channel_title = "vsdfsdf",
    platform = "tg",
    post_id = 1,
    views = 123,
    description = message1[0:200],
    message = message1,
    link = f"https://t.me/vvolunteerskyiv/123",
    author = "arthur")

posts = [post1]
for ch in telegram_channels_new:
    for post in posts:
        post.category = ch.category
        post.post_type = ch.post_type
        post.geo = ch.geo
        updated = post
        for rule in rules:
            updated = rule.analyze(updated)
        print(updated)
    
