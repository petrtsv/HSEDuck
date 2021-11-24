from typing import Optional

from hseduck_bot import config
from hseduck_bot.controller import users, stocks
from hseduck_bot.model.storage.base import BaseStorage
from hseduck_bot.model.storage.sqlite import SQLiteStorage

storage: Optional[BaseStorage] = None


def load():
    global storage
    storage = SQLiteStorage(config.SQLITE_FILE)
    storage.init()
    storage.build_scheme()

    users.initialize(storage)
    stocks.initialize(storage)


def unload():
    global storage
    storage.close()
