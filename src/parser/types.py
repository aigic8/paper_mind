from typing import List
from datetime import datetime

SCIENCE_DIRECT_SOURCE = "scienceDirect"


class Source:
    name: str
    kind: str
    url: str

    def __init__(self, name: str, kind: str, url: str) -> None:
        self.name = name
        self.kind = kind
        self.url = url


class Article:
    title: str
    url: str
    authors: List[str]
    publish_date: datetime

    def __init__(self, title: str, url: str, authors: List[str], publish_date: datetime) -> None:
        self.title = title
        self.url = url
        self.authors = authors
        self.publish_date = publish_date
