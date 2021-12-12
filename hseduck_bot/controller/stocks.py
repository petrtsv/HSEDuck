import datetime
import math
from typing import Optional

from hseduck_bot.model.stocks import StockStorage, StockInfo, StockRecord

stock_storage: Optional[StockStorage] = None


def initialize(storage: StockStorage):
    global stock_storage
    stock_storage = storage


def save_info(info: StockInfo):
    stock_storage.save_stock_info(info)


def get_info(ticker: str):
    return stock_storage.get_stock_info(ticker)


def all_stocks():
    return stock_storage.get_stocks()


def last_record(ticker: str, timestamp: Optional[datetime.datetime] = None):
    return stock_storage.get_last_stock_record(ticker, timestamp=timestamp)


def price_int(ticker: str, timestamp: Optional[datetime.datetime] = None):
    return int(last_record(ticker, timestamp=timestamp).price)


def price_str(ticker: str, timestamp: Optional[datetime.datetime] = None):
    record = last_record(ticker, timestamp=timestamp)
    return record.price_repr if record is not None else "NONE"


def price_float(ticker: str, timestamp: Optional[datetime.datetime] = None):
    record = last_record(ticker, timestamp=timestamp)
    return float(record.price_float if record is not None else math.nan)


def save_record(record: StockRecord):
    stock_storage.save_stock_record(record)
