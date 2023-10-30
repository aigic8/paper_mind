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
        schedule.every(self.freq_hours).hours.do(self.task)

    def task(self):
        sources = self._db.source_get_all()
        if len(sources) == 0:
            return

        groups = self._db.group_get_all()
        for source in sources:
            should_notify_user = source.last_id != ''
            if source.kind == SOURCE_KIND_SCIENCE_DIRECT:
                new_articles, last_id = new_science_direct_articles(source.url, source.last_id)
                if last_id == "":
                    continue
                self._db.source_set_last_id(source.name, last_id)
                if should_notify_user:
                    for article in new_articles:
                        for group in groups:
                            self._bot.send_message(group.chat_id, new_article_text(source.name, article))
                else:
                    print(f"UNKNOWN SOURCE KIND: {source.kind}")


def new_article_text(source_name: str, article: Article) -> str:
    return f"""New Article {source_name}:
{article.title}
{', '.join(article.authors)}
{article.publish_date}
{article.url}"""
