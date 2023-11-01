import asyncio

from src.db.db import DB
from src.bot.bot import Bot
from src.config import load_config

CONFIG_PATH = "paper_mind.sample.toml"


async def main():
    c = load_config(CONFIG_PATH)
    db = DB(c.db_url)
    bot = Bot(c.token, db, c.fetch_freq_hours)

    for source in c.sources:
        db_source = db.source_get(source.name)
        if db_source is None:
            db.source_create(source.name, source.url, source.kind)

    bot.start()


if __name__ == "__main__":
    asyncio.run(main())
