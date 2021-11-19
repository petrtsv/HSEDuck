import datetime
import sqlite3
from sqlite3 import Cursor
from typing import Dict, Any, Union, List

from hseduck_bot.storage.stocks import StockStorage, StockInfo, StockRecord


class SQLiteStorage(StockStorage):
    @staticmethod
    def datetime_to_int(timestamp: datetime.datetime):
        return int(timestamp.timestamp() * 1000)

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None
        self.cursor: Union[Cursor, None] = None

    def execute_query(self, template: str, args: Dict[str, Any] = None) -> None:
        self.cursor.execute(template, args) if args is not None else self.cursor.execute(template)

    def init(self):
        self.connection = sqlite3.connect(self.db_file)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()

    def build_scheme(self):
        self.execute_query("CREATE TABLE IF NOT EXISTS stock_records ( "
                           "ticker VARCHAR(10), "
                           "price INTEGER, "
                           "record_timestamp INTEGER "
                           ")")
        self.execute_query("CREATE TABLE IF NOT EXISTS stock_info ("
                           "ticker VARCHAR(10) UNIQUE ON CONFLICT REPLACE, "
                           "stock_name VARCHAR(128), "
                           'description VARCHAR(16384) DEFAULT "", '
                           'json_info TEXT DEFAULT "{}"'
                           ")")

    def save_stock_record(self, record: StockRecord) -> None:
        if record is None:
            return
        self.execute_query("INSERT INTO stock_records (ticker, price, record_timestamp) VALUES "
                           "(:ticker, :price, :timestamp)", {
                               "ticker": record.ticker,
                               "price": record.price,
                               "record_timestamp": self.datetime_to_int(record.timestamp),
                           })

    def get_stock_records(self, ticker: str, from_date: datetime.datetime = None) \
            -> List[StockRecord]:
        self.execute_query("SELECT * FROM stock_records WHERE "
                           "ticker = :ticker " +
                           ("" if from_date is None else "record_timestamp >= :from_timestamp ") +
                           "ORDER BY record_timestamp DESC")
        return [StockRecord(ticker=row[0], price=row[1], timestamp=datetime.datetime.fromtimestamp(row[2])) for row in
                self.cursor.fetchall()]

    def get_last_stock_record(self, ticker: str) -> Union[StockRecord, None]:
        self.execute_query("SELECT * FROM stock_records WHERE "
                           "ticker = :ticker "
                           "ORDER BY record_timestamp DESC")
        result = self.cursor.fetchone()
        return result if result is None else StockRecord(ticker=result[0], price=result[1],
                                                         timestamp=datetime.datetime.fromtimestamp(result[2]))

    def save_stock_info(self, info: StockInfo) -> None:
        if info is None:
            return
        self.execute_query("INSERT INTO stock_info (ticker, stock_name, description, json_info) VALUES "
                           "(:ticker, :stock_name, :description, :json_info)", {
                               "ticker": info.ticker,
                               "stock_name": info.name,
                               "description": info.description,
                               "json_info": info.json_info
                           })

    def get_stock_info(self, ticker: str) -> Union[StockInfo, None]:
        self.execute_query("SELECT * FROM stock_info WHERE "
                           "ticker = :ticker")
        result = self.cursor.fetchone()
        return result if result is None else StockInfo(ticker=result[0], name=result[1], description=result[2],
                                                       json_info=result[3])

    def get_stocks(self) -> List[StockInfo]:
        self.execute_query("SELECT * FROM stock_info")
        return [StockInfo(ticker=row[0], name=row[1], description=row[2], json_info=row[3]) for row in
                self.cursor.fetchall()]
