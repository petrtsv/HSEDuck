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


def last_record(ticker: str):
    return stock_storage.get_last_stock_record(ticker)


def price_int(ticker: str):
    return int(last_record(ticker).price)


def price_str(ticker: str):
    record = last_record(ticker)
    return record.price_repr if record is not None else "NONE"


def price_float(ticker: str):
    record = last_record(ticker)
    return float(record.price_float if record is not None else math.nan)


def save_record(record: StockRecord):
    stock_storage.save_stock_record(record)
