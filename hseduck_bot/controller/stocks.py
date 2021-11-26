from typing import Optional

from hseduck_bot.model.stocks import StockStorage, StockInfo, StockRecord

stock_storage: Optional[StockStorage] = None


def initialize(storage: StockStorage):
    global stock_storage
    stock_storage = storage


def save_info(info: StockInfo):
    stock_storage.save_stock_info(info)


def all_stocks():
    return stock_storage.get_stocks()


def last_record(ticker: str):
    return stock_storage.get_last_stock_record(ticker)


def price(ticker: str):
    return last_record(ticker).price


def save_record(record: StockRecord):
    stock_storage.save_stock_record(record)
