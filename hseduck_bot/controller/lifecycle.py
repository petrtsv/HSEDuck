import asyncio
import traceback
from typing import Optional

from hseduck_bot import config
from hseduck_bot.controller import users, stocks, portfolios, transactions, fetch, contests, short_transactions
from hseduck_bot.model.storage.base import BaseStorage
from hseduck_bot.model.storage.postgres import PostgresStorage
from hseduck_bot.model.storage.sqlite import SQLiteStorage
from hseduck_bot.util import Periodic

storage: Optional[BaseStorage] = None
updater_stocks: Optional[Periodic] = None
updater_db: Optional[Periodic] = None


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
    contests.initialize(storage)
    short_transactions.initialize(storage)
    print("Storage loaded")

    contests.create_global_competition()

    print("Load stocks from list...")
    fetch.fetch_stocks_info()
    print("Loaded")
    await start_update()
    print("Bot loaded")


def update_stocks():
    try:
        for stock in stocks.all_stocks():
            last_record = stocks.last_record(stock.ticker)
            last_timestamp = None if last_record is None else last_record.timestamp
            fetch.fetch_stock_prices(stock.ticker, start=last_timestamp)
    except Exception:
        print("Exception while updating stocks!")
        print(traceback.format_exc())


def update_db():
    try:
        contests.update()
        short_transactions.update()
    except Exception:
        print("Exception while updating db!")
        print(traceback.format_exc())


async def start_update():
    print("Update prices every %.2f second(s)" % config.UPDATE_STOCKS_INTERVAL)
    global updater_stocks
    updater_stocks = Periodic(update_stocks, config.UPDATE_STOCKS_INTERVAL)

    print("Update db every %.2f second(s)" % config.UPDATE_DB_INTERVAL)
    global updater_db
    updater_db = Periodic(update_db, config.UPDATE_DB_INTERVAL)

    await asyncio.gather(updater_stocks.start(), updater_db.start())


async def unload():
    if updater_stocks is not None:
        await updater_stocks.stop()
    if updater_db is not None:
        await updater_db.stop()
    print("Closing storage...")
    global storage
    storage.close()
    print("Storage closed")
