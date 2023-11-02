from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import String, create_engine, Column, DateTime, BigInteger
from sqlalchemy.sql import func

Base = declarative_base()

SOURCE_KIND_SCIENCE_DIRECT = "scienceDirect"


class Source(Base):
    __tablename__ = "sources"

    name = Column(String, primary_key=True)
    url = Column(String)
    kind = Column(String)
    last_id = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, name: str, kind: str, url: str, last_id: str):
        self.name = name
        self.kind = kind
        self.url = url
        self.last_id = last_id

    def __repr__(self):
        return f"Source(name={self.name}, last_id={self.last_id}, created_at={self.created_at})"


class Group(Base):
    __tablename__ = "groups"

    chat_id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, chat_id: int):
        self.chat_id = chat_id

    def __repr__(self):
        return f"Group(chat_id={self.chat_id}, created_at={self.created_at})"


class DB:
    _s: Session

    def __init__(self, url: str):
        engine = create_engine(url)
        Base.metadata.create_all(engine)
        s_maker = sessionmaker(bind=engine)
        self._s = s_maker()

    def source_create(self, name: str, url: str, kind: str):
        self._s.add(Source(name, kind, url, ""))
        self._s.commit()

    def source_get(self, name: str) -> Source | None:
        return self._s.query(Source).filter(Source.name == name).first()

    def source_get_all(self):
        return self._s.query(Source).all()

    def source_set_last_id(self, name: str, last_id: str):
        self._s.query(Source).filter(Source.name == name).update({"last_id": last_id})
        self._s.commit()

    def group_get_all(self):
        return self._s.query(Group).all()

    def group_create(self, chat_id: int):
        self._s.add(Group(chat_id))
        self._s.commit()

    def group_delete(self, chat_id: int):
        self._s.query(Group).filter(Group.chat_id == chat_id).delete()
        self._s.commit()
