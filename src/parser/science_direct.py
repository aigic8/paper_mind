from typing import List
from src.parser.types import Article
import feedparser
import datetime
import re


def new_science_direct_articles(url: str, after_id: str) -> tuple[List[Article], str]:
    articles: List[Article] = []
    res = feedparser.parse(url)
    last_id = ''
    for entry in res.entries:
        if entry.id == after_id:
            break
        authors = extract_authors(entry.summary)
        if authors is None:
            authors = []
        pub_date = extract_pub_date(entry.summary)
        if pub_date is None:
            continue
        if last_id == '':
            last_id = entry.id
        articles.append(Article(title=entry.title, url=entry.link, authors=authors, publish_date=pub_date))
    return articles, last_id


def extract_pub_date(summary: str) -> datetime.datetime | None:
    date_str_raw = re.search('Publication date:\s+(\d+\s+[A-Za-z]+\s+\d{4})', summary)
    if date_str_raw is None:
        return None
    date_str = remove_prefix("Publication date:", date_str_raw.group()).strip()
    return datetime.datetime.strptime(date_str, "%d %B %Y")


def extract_authors(summary: str) -> List[str] | None:
    authors_str_raw = re.search('Author\(s\): ([A-Za-z\s,]+)', summary)
    if authors_str_raw is None:
        return None
    authors_str = remove_prefix("Author(s):", authors_str_raw.group()).strip()
    authors = authors_str.split(",")
    return [author.strip() for author in authors]


def remove_prefix(prefix: str, text: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
