import logging

import schedule
import telegram

from src.db.db import DB, SOURCE_KIND_SCIENCE_DIRECT

from src.parser.science_direct import new_science_direct_articles
from src.parser.types import Article


class ScheduledFetcher:
    freq_hours: int
    _db: DB
    _bot: telegram.Bot

    def __init__(self, frequency_hours: int, db: DB, bot: telegram.Bot):
        self._db = db
        self.freq_hours = frequency_hours
        self._bot = bot

    def start(self):
        self.check_for_new_articles()
        logging.info(f"scheduled task runner for every {self.freq_hours} hours")
        schedule.every(self.freq_hours).hours.do(self.check_for_new_articles)

    def check_for_new_articles(self):
        logging.info("checking for new articles")
        sources = self._db.source_get_all()
        logging.debug(f"found {len(sources)} sources")
        if len(sources) == 0:
            return

        groups = self._db.group_get_all()
        logging.debug(f"number of groups: {len(groups)}")
        for source in sources:
            should_notify_user = source.last_id != ''
            if source.kind == SOURCE_KIND_SCIENCE_DIRECT:
                new_articles, last_id = new_science_direct_articles(source.url, source.last_id)
                logging.debug(
                    f"checked source: {source.name}, should_notify_user: {should_notify_user}, new_articles: {len(new_articles)}, last_id: {last_id}")
                if last_id == "":
                    continue
                self._db.source_set_last_id(source.name, last_id)
                if should_notify_user:
                    for article in new_articles:
                        for group in groups:
                            self._bot.send_message(group.chat_id, new_article_text(source.name, article))
                else:
                    logging.warning(f"unknown source kind: {source.kind}")


def new_article_text(source_name: str, article: Article) -> str:
    return f"""New Article {source_name}:
{article.title}
{', '.join(article.authors)}
{article.publish_date}
{article.url}"""
