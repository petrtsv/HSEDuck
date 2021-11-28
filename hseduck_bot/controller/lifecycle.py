import asyncio
from asyncio import Task
from typing import Optional

from hseduck_bot import config
from hseduck_bot.controller import users, stocks, portfolios, transactions, fetch
from hseduck_bot.model.storage.base import BaseStorage
from hseduck_bot.model.storage.postgres import PostgresStorage
from hseduck_bot.model.storage.sqlite import SQLiteStorage
from hseduck_bot.util import Periodic

storage: Optional[BaseStorage] = None
updater: Optional[Periodic] = None


async def load():
    print("Loading storage...")
    print("Using DB: %s" % config.DB_TYPE)
    global storage
    if config.DB_TYPE == 'sqlite':
        storage = SQLiteStorage(config.CONNECTION_STRING)
    else:
        storage = PostgresStorage(config.CONNECTION_STRING)

    storage.init()
    storage.build_scheme()

    users.initialize(storage)
    stocks.initialize(storage)
    portfolios.initialize(storage)
    transactions.initialize(storage)
    print("Storage loaded")

    print("Load stocks from list...")
    fetch.fetch_stocks_info()
    print("Loaded")
    await start_update()
    print("Bot loaded")


def update():
    try:
        for stock in stocks.all_stocks():
            last_record = stocks.last_record(stock.ticker)
            last_timestamp = None if last_record is None else last_record.timestamp
            fetch.fetch_stock_prices(stock.ticker, start=last_timestamp)
    except Exception as e:
        print("Exception while updating!")
        print(e)


async def start_update():
    print("Update prices every %.2f second(s)" % config.UPDATE_INTERVAL)
    global updater
    updater = Periodic(update, config.UPDATE_INTERVAL)
    await updater.start()


async def unload():
    if updater is not None:
        await updater.stop()
    print("Closing storage...")
    global storage
    storage.close()
    print("Storage closed")
