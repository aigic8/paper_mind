import logging
import asyncio

from src.db.db import DB
from src.bot.bot import Bot
from src.config import load_config

CONFIG_PATH = "runtime/paper_mind.toml"


async def main():
    c = load_config(CONFIG_PATH)
    db = DB(c.db_url)
    bot = Bot(c.token, db, c.fetch_freq_hours)
    logging.basicConfig(
        filename=c.log_path,
        format="%(asctime)s %(levelname)s %(message)",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG
    )

    for source in c.sources:
        db_source = db.source_get(source.name)
        if db_source is None:
            db.source_create(source.name, source.url, source.kind)

    await bot.start()


if __name__ == "__main__":
    main()
