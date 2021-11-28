import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Iterable

from hseduck_bot.model.portfolios import PortfolioStorage, Portfolio
from hseduck_bot.model.stocks import StockStorage, StockRecord, StockInfo
from hseduck_bot.model.storage.base import BaseStorage
from hseduck_bot.model.transactions import TransactionStorage, Transaction
from hseduck_bot.model.users import UserStorage, User


class AbstractSQLStorage(BaseStorage, StockStorage, UserStorage, PortfolioStorage, TransactionStorage, ABC):
    @staticmethod
    def datetime_to_int(timestamp: datetime.datetime):
        return int(timestamp.timestamp() * 1000)

    @staticmethod
    def int_to_datetime(x: int):
        return datetime.datetime.fromtimestamp(x / 1000.)

    def __init__(self):
        self.connection = None
        self.cursor = None

    @abstractmethod
    def execute_query(self, template: str, args: Dict[str, Any] = None, commit=True) -> None:
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    def build_scheme(self):
        self.execute_query("CREATE TABLE IF NOT EXISTS stock_records ( "
                           "ticker VARCHAR(10) NOT NULL , "
                           "price INTEGER NOT NULL , "
                           "record_timestamp INTEGER  NOT NULL "
                           ")")
        self.execute_query("CREATE TABLE IF NOT EXISTS stock_info ("
                           "ticker VARCHAR(10) UNIQUE, "
                           "stock_name VARCHAR(128) NOT NULL , "
                           'description VARCHAR(16384) DEFAULT "", '
                           'json_info TEXT DEFAULT "{}"'
                           ")")

        self.execute_query("CREATE TABLE IF NOT EXISTS users ("
                           "id INTEGER NOT NULL PRIMARY KEY, "
                           "username VARCHAR(64) NOT NULL UNIQUE)")

        self.execute_query("CREATE TABLE IF NOT EXISTS portfolios ("
                           "id INTEGER NOT NULL PRIMARY KEY, "
                           "owner_id INTEGER NOT NULL, "
                           "name VARCHAR(128) NOT NULL )")

        self.execute_query("CREATE TABLE IF NOT EXISTS transactions("
                           "portfolio_id INTEGER NOT NULL, "
                           "ticker VARCHAR(10) NOT NULL, "
                           "quantity INTEGER NOT NULL )")

    def save_stock_record(self, record: StockRecord) -> None:
        if record is None:
            return
        self.execute_query("INSERT INTO stock_records (ticker, price, record_timestamp) VALUES "
                           "(:ticker, :price, :record_timestamp)", {
                               "ticker": record.ticker,
                               "price": record.price,
                               "record_timestamp": self.datetime_to_int(record.timestamp),
                           })

    def get_stock_records(self, ticker: str, from_date: datetime.datetime = None) \
            -> List[StockRecord]:
        self.execute_query("SELECT * FROM stock_records WHERE "
                           "ticker = :ticker " +
                           ("" if from_date is None else "record_timestamp > :from_timestamp ") +
                           "ORDER BY record_timestamp DESC",
                           {'ticker': ticker})
        return [StockRecord(ticker=row[0], price=row[1], timestamp=self.int_to_datetime(row[2])) for row in
                self.cursor.fetchall()]

    def get_last_stock_record(self, ticker: str) -> Union[StockRecord, None]:
        self.execute_query("SELECT * FROM stock_records WHERE "
                           "ticker = :ticker "
                           "ORDER BY record_timestamp DESC",
                           {'ticker': ticker})
        result = self.cursor.fetchone()
        return result if result is None else StockRecord(ticker=result[0], price=result[1],
                                                         timestamp=self.int_to_datetime(result[2]))

    def save_stock_info(self, info: StockInfo) -> None:
        if info is None:
            return
        self.execute_query("INSERT INTO stock_info (ticker, stock_name, description, json_info) VALUES "
                           "(:ticker, :stock_name, :description, :json_info) "
                           "ON CONFLICT (ticker) DO UPDATE SET ticker = EXCLUDED.dname", {
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

    def create_user(self, user: User) -> None:
        if user is None:
            return
        self.execute_query("INSERT INTO users (username) VALUES "
                           "(:username) ON CONFLICT (username) DO NOTHING", {
                               'username': user.username
                           })
        user.id = self.cursor.lastrowid

    def find_user(self, user: User, create: bool = False) -> None:
        if user is None:
            return
        self.execute_query("SELECT * FROM users WHERE "
                           "username = :username", {
                               'username': user.username
                           })
        row = self.cursor.fetchone()
        if row is None and create:
            self.create_user(user)
        else:
            user.id = row[0]

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        self.execute_query("SELECT * FROM users WHERE "
                           "id = :id", {
                               'id': user_id
                           })
        row = self.cursor.fetchone()
        if row is None:
            return None
        return User(user_id=row[0], username=row[1])

    def create_portfolio(self, portfolio: Portfolio) -> None:
        if portfolio is None:
            return
        self.execute_query("INSERT INTO portfolios (owner_id, name) VALUES "
                           "(:owner_id, :name)", {
                               'owner_id': portfolio.owner_id,
                               'name': portfolio.name
                           })
        portfolio.id = self.cursor.lastrowid

    def get_portfolio_by_id(self, portfolio_id: int) -> Optional[Portfolio]:
        self.execute_query("SELECT * FROM portfolios WHERE "
                           "id = :id", {
                               'id': portfolio_id
                           })
        row = self.cursor.fetchone()
        if row is None:
            return None
        return Portfolio(portfolio_id=row[0], owner_id=row[1], name=row[2])

    def get_portfolios_for_user_id(self, user_id: int) -> List[Portfolio]:
        self.execute_query("SELECT * FROM portfolios WHERE "
                           "owner_id = :owner_id", {
                               'owner_id': user_id
                           })
        return [Portfolio(portfolio_id=row[0], owner_id=row[1], name=row[2]) for row in self.cursor.fetchall()]

    def get_tickers_for_portfolio(self, portfolio_id: int) -> List[str]:
        self.execute_query("SELECT ticker, SUM(quantity) as total FROM transactions WHERE portfolio_id = :portfolio_id "
                           "GROUP BY ticker HAVING total > 0", {
                               'portfolio_id': portfolio_id
                           })
        return [row[0] for row in self.cursor.fetchall()]

    def add_transaction_batch(self, batch: Iterable[Transaction]):
        self.execute_query("BEGIN TRANSACTION")
        for transaction in batch:
            self.execute_query("INSERT INTO transactions (portfolio_id, ticker, quantity) VALUES "
                               "(:portfolio_id, :ticker, :quantity)", {
                                   'portfolio_id': transaction.portfolio_id,
                                   'ticker': transaction.ticker,
                                   'quantity': transaction.quantity,
                               }, commit=False)
        self.execute_query("COMMIT TRANSACTION")
        self.connection.commit()

    def get_quantity(self, portfolio_id: int, ticker: str) -> int:
        self.execute_query(
            "SELECT SUM(quantity) as total FROM transactions "
            "WHERE portfolio_id = :portfolio_id AND ticker = :ticker",
            {
                'portfolio_id': portfolio_id,
                'ticker': ticker
            })
        row = self.cursor.fetchone()
        return row[0] if row is not None else 0
