import asyncio
import tomllib

from src.db.db import DB, Source
from typing import List
from src.bot.bot import Bot


async def main():
    config_file = open("paper_mind.toml", 'rb')
    config = tomllib.load(config_file)
    config_file.close()
    sources_raw = config["sources"]
    sources: List[Source] = []
    for source in sources_raw:
        sources.append(Source(name=source["name"], kind=source["kind"], url=source["url"], last_id=""))
    db_url = config["db_url"]
    token = config["token"]
    fetch_freq_hours = config["fetch_freq_hours"]

    db = DB(db_url)
    bot = Bot(token, db, fetch_freq_hours)

    for source in sources:
        db_source = db.source_get(source.name)
        if db_source is None:
            db.source_create(source.name, source.url, source.kind)

    bot.start()


if __name__ == "__main__":
    asyncio.run(main())
