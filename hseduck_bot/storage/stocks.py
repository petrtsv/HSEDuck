import datetime
from abc import ABC, abstractmethod
from typing import List, Union

from hseduck_bot.storage.db.base import AbstractStorage


class StockInfo:
    def __init__(self, ticker: str, name: str, description: str = "", json_info: str = "{}"):
        self.ticker = ticker
        self.name = name
        self.description = description
        self.json_info = json_info


class StockRecord:
    def __init__(self, ticker: str, price: int, timestamp: datetime.datetime):
        self.ticker = ticker
        self.price = price
        self.timestamp = timestamp


class StockStorage(AbstractStorage, ABC):
    @abstractmethod
    def save_stock_record(self, record: StockRecord) -> None:
        """
        Save new record to storage
        :param record: A record to save
        :return:
        """
        pass

    @abstractmethod
    def get_stock_records(self, ticker: str, from_date: datetime.datetime = datetime.date(1, 1, 1)) \
            -> List[StockRecord]:
        """
        Get list of all available records for given ticker
        :param ticker: A ticker to get records for
        :param from_date: (optional) Return records after the particular timestamp
        :return: List of available records
        """
        pass

    @abstractmethod
    def get_last_stock_record(self, ticker: str) -> Union[StockRecord, None]:
        """
        Get last record for given ticker.
        :param ticker: Ticker to get record for.
        :return: Last record for given ticker, None if not found
        """
        pass

    @abstractmethod
    def get_stock_info(self, ticker: str) -> Union[StockInfo, None]:
        pass

    @abstractmethod
    def save_stock_info(self, info: StockInfo) -> None:
        pass

    @abstractmethod
    def get_stocks(self) -> List[StockInfo]:
        pass
