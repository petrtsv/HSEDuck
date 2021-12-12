import datetime
from abc import ABC, abstractmethod
from typing import List, Union, Optional

from hseduck_bot import config


class StockInfo:
    def __init__(self, ticker: str, name: str, description: str = "", json_info: str = "{}"):
        self.ticker = ticker
        self.name = name
        self.description = description
        self.json_info = json_info


class StockRecord:
    def __init__(self, ticker: str, price: int, timestamp: datetime.datetime):
        self.ticker = ticker
        self.price = int(price)
        self.timestamp = timestamp

    @property
    def price_repr(self):
        return config.PRICE_REPR % self.price_float

    @property
    def price_float(self):
        return self.price / config.PRICE_PRECISION


class StockStorage(ABC):
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
    def get_last_stock_record(self, ticker: str, timestamp: Optional[datetime.datetime] = None) -> \
            Union[StockRecord, None]:
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
