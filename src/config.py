import tomllib
from typing import List
from src.db.db import Source


class Config:
    db_url: str
    token: str
    fetch_freq_hours: int
    sources: List[Source]
    log_path: str

    def __init__(self, *, db_url: str, token: str, fetch_freq_hours: int, sources: List[Source], log_path: str):
        self.db_url = db_url
        self.token = token
        self.fetch_freq_hours = fetch_freq_hours
        self.sources = sources
        self.log_path = log_path


def load_config(config_path: str) -> Config:
    with open(config_path, 'rb') as config_file:
        config = tomllib.load(config_file)
    sources_raw = config["sources"]
    sources: List[Source] = []
    for source in sources_raw:
        sources.append(Source(name=source["name"], kind=source["kind"], url=source["url"], last_id=""))
    db_url = config["db_url"]
    token = config["token"]
    fetch_freq_hours = config["fetch_freq_hours"]
    log_path = config["log_path"]
    return Config(db_url=db_url, token=token, fetch_freq_hours=fetch_freq_hours, sources=sources, log_path=log_path)
