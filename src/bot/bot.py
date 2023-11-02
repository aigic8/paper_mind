import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, Application, ChatMemberHandler, ContextTypes
from src.db.db import DB
from src.bot.scheduled_fetcher import ScheduledFetcher

CHAT_TYPE_GROUP = "group"
CHAT_TYPE_SUPER_GROUP = "supergroup"

CHAT_MEMBER_STATUS_MEMBER = "member"
CHAT_MEMBER_STATUS_BANNED = "kicked"
CHAT_MEMBER_STATUS_LEFT = "left"


class Bot:
    token: str
    _db: DB
    _app: Application
    fetch_freq_hours: int

    def __init__(self, token: str, db: DB, fetch_freq_hours: int):
        self.token = token
        self.fetch_freq_hours = fetch_freq_hours
        self._app = ApplicationBuilder().token(token).build()
        self._db = db

    def start(self):
        self._app.add_handler(ChatMemberHandler(self._chat_member_handler))
        sf = ScheduledFetcher(self.fetch_freq_hours, self._db, self._app.bot)
        sf.start()
        self._app.run_polling()

    async def _chat_member_handler(self, update: Update, _: ContextTypes.DEFAULT_TYPE):
        if update.my_chat_member is None or not is_chat_type_group(update.my_chat_member.chat.type):
            return
        new_status = update.my_chat_member.new_chat_member.status
        if new_status == CHAT_MEMBER_STATUS_MEMBER:
            logging.info(f"joined group {update.my_chat_member.chat.id}")
            self._db.group_create(update.my_chat_member.chat.id)
        elif new_status == CHAT_MEMBER_STATUS_LEFT or new_status == CHAT_MEMBER_STATUS_BANNED:
            logging.info(f"left group {update.my_chat_member.chat.id}")
            self._db.group_delete(update.my_chat_member.chat.id)


def is_chat_type_group(chat_type: str) -> bool:
    return chat_type == CHAT_TYPE_GROUP or chat_type == CHAT_TYPE_SUPER_GROUP
