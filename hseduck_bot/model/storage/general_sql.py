import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union, Iterable

from hseduck_bot.model import contests
from hseduck_bot.model.contests import ContestStorage, Contest
from hseduck_bot.model.portfolios import PortfolioStorage, Portfolio
from hseduck_bot.model.short_transactions import ShortTransactionStorage, ShortTransaction
from hseduck_bot.model.stocks import StockStorage, StockRecord, StockInfo
from hseduck_bot.model.storage.base import BaseStorage
from hseduck_bot.model.transactions import TransactionStorage, Transaction
from hseduck_bot.model.users import UserStorage, User


class AbstractSQLStorage(BaseStorage, StockStorage, UserStorage, PortfolioStorage, TransactionStorage, ContestStorage,
                         ShortTransactionStorage,
                         ABC):

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
                           "price BIGINT NOT NULL , "
                           "record_timestamp BIGINT  NOT NULL "
                           ")")
        self.execute_query("CREATE TABLE IF NOT EXISTS stock_info ("
                           "ticker VARCHAR(10) UNIQUE, "
                           "stock_name VARCHAR(128) NOT NULL , "
                           "description VARCHAR(16384) DEFAULT '', "
                           "json_info TEXT DEFAULT '{}'"
                           ")")

        self.execute_query("CREATE TABLE IF NOT EXISTS users ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "username VARCHAR(64) NOT NULL UNIQUE)")

        self.execute_query("CREATE TABLE IF NOT EXISTS portfolios ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "owner_id BIGINT NOT NULL, "
                           "name VARCHAR(128) NOT NULL, "
                           "contest_id BIGINT)")

        self.execute_query("CREATE TABLE IF NOT EXISTS transactions("
                           "portfolio_id BIGINT NOT NULL, "
                           "ticker VARCHAR(10) NOT NULL, "
                           "quantity BIGINT NOT NULL )")

        self.execute_query("CREATE TABLE IF NOT EXISTS contests( "
                           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "owner_id BIGINT NOT NULL, "
                           "name VARCHAR(128) NOT NULL, "
                           "start_timestamp BIGINT NOT NULL, "
                           "end_timestamp BIGINT NOT NULL, "
                           "status INTEGER NOT NULL)")

        self.execute_query("CREATE TABLE IF NOT EXISTS participations( "
                           "user_id BIGINT NOT NULL, "
                           "contest_id BIGINT NOT NULL)")

        self.execute_query("CREATE TABLE IF NOT EXISTS short_transactions( "
                           "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "portfolio_id BIGINT NOT NULL, "
                           "ticker VARCHAR(10) NOT NULL, "
                           "quantity BIGINT NOT NULL,"
                           "timestamp BIGINT NOT NULL)")

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

    def get_last_stock_record(self, ticker: str, timestamp: Optional[datetime.datetime] = None) -> \
            Union[StockRecord, None]:
        if timestamp is None:
            timestamp = datetime.datetime.now()
        int_timestamp: int = self.datetime_to_int(timestamp)
        self.execute_query("SELECT * FROM stock_records WHERE "
                           "ticker = :ticker AND record_timestamp <= :timestamp "
                           "ORDER BY record_timestamp DESC",
                           {
                               'ticker': ticker,
                               'timestamp': int_timestamp
                           })
        result = self.cursor.fetchone()
        return result if result is None else StockRecord(ticker=result[0], price=result[1],
                                                         timestamp=self.int_to_datetime(result[2]))

    def save_stock_info(self, info: StockInfo) -> None:
        if info is None:
            return
        self.execute_query("INSERT INTO stock_info (ticker, stock_name, description, json_info) VALUES "
                           "(:ticker, :stock_name, :description, :json_info) "
                           "ON CONFLICT (ticker) DO UPDATE SET ticker = EXCLUDED.ticker", {
                               "ticker": info.ticker,
                               "stock_name": info.name,
                               "description": info.description,
                               "json_info": info.json_info
                           })

    def get_stock_info(self, ticker: str) -> Union[StockInfo, None]:
        self.execute_query("SELECT * FROM stock_info WHERE "
                           "ticker = :ticker",
                           {'ticker': ticker})
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
                           "(:username) ON CONFLICT (username) DO NOTHING RETURNING id", {
                               'username': user.username
                           })
        row = self.cursor.fetchone()
        user.id = row[0]

    def find_user(self, user: User, create: bool = False) -> None:
        if user is None:
            return
        self.execute_query("SELECT * FROM users WHERE "
                           "username = :username", {
                               'username': user.username
                           })
        row = self.cursor.fetchone()
        if row is None:
            if create:
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
        self.execute_query("INSERT INTO portfolios (owner_id, name, contest_id) VALUES "
                           "(:owner_id, :name, :contest_id) RETURNING id", {
                               'owner_id': portfolio.owner_id,
                               'name': portfolio.name,
                               'contest_id': portfolio.contest_id
                           })
        row = self.cursor.fetchone()
        portfolio.id = row[0]

    def get_portfolio_by_id(self, portfolio_id: int) -> Optional[Portfolio]:
        self.execute_query("SELECT * FROM portfolios WHERE "
                           "id = :id", {
                               'id': portfolio_id
                           })
        row = self.cursor.fetchone()
        if row is None:
            return None
        return Portfolio(portfolio_id=row[0], owner_id=row[1], name=row[2], contest_id=row[3])

    def get_portfolios_for_user_id(self, user_id: int) -> List[Portfolio]:
        self.execute_query("SELECT * FROM portfolios WHERE "
                           "owner_id = :owner_id", {
                               'owner_id': user_id
                           })
        return [Portfolio(portfolio_id=row[0], owner_id=row[1], name=row[2], contest_id=row[3]) for row in
                self.cursor.fetchall()]

    def get_tickers_for_portfolio(self, portfolio_id: int) -> List[str]:
        self.execute_query(
            "SELECT ticker, SUM(quantity), portfolio_id FROM transactions WHERE portfolio_id = :portfolio_id "
            "GROUP BY ticker, portfolio_id HAVING SUM(quantity) <> 0", {
                'portfolio_id': portfolio_id
            })
        res = [row[0] for row in self.cursor.fetchall()]
        return res

    def add_transaction_batch(self, batch: Iterable[Transaction]):
        self.execute_query("BEGIN TRANSACTION", commit=False)
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
            "SELECT SUM(quantity), portfolio_id, ticker FROM transactions "
            "WHERE portfolio_id = :portfolio_id AND ticker = :ticker GROUP BY portfolio_id, ticker",
            {
                'portfolio_id': portfolio_id,
                'ticker': ticker
            })
        row = self.cursor.fetchone()
        if row is None:
            return 0

        return row[0] if row[0] is not None else 0

    def new_contest(self, contest: Contest) -> None:
        if contest is None:
            return
        self.execute_query("INSERT INTO contests (owner_id, name, start_timestamp, end_timestamp, status) VALUES "
                           "(:owner_id, :name, :start_timestamp, :end_timestamp, :status) RETURNING id", {
                               'owner_id': contest.owner_id,
                               'name': contest.name,
                               'start_timestamp': self.datetime_to_int(contest.start_date),
                               'end_timestamp': self.datetime_to_int(contest.end_date),
                               'status': contest.status
                           })
        row = self.cursor.fetchone()
        contest.id = row[0]

    def get_participants_by_contest_id(self, contest_id: int) -> List[User]:
        self.execute_query("SELECT * FROM participations WHERE "
                           "contest_id = :contest_id",
                           {'contest_id': contest_id})
        return [self.get_user_by_id(row[0]) for row in
                self.cursor.fetchall()]

    def get_contests_for_user_id(self, user_id: int) -> List[Contest]:
        self.execute_query("SELECT * FROM participations WHERE "
                           "user_id = :user_id",
                           {'user_id': user_id})
        return [self.get_contest_by_id(row[1]) for row in
                self.cursor.fetchall()]

    def get_owned_contests_for_user_id(self, user_id: int) -> List[Contest]:
        self.execute_query("SELECT * FROM contests WHERE "
                           "owner_id = :owner_id", {
                               'owner_id': user_id
                           })
        rows = self.cursor.fetchall()

        return [Contest(contest_id=row[0], owner_id=row[1], name=row[2], start_date=self.int_to_datetime(row[3]),
                        end_date=self.int_to_datetime(row[4]), status=row[5]) for row in rows]

    def join_contest(self, user_id: int, contest_id: int) -> None:
        self.execute_query("INSERT INTO participations (user_id, contest_id) VALUES"
                           "(:user_id, :contest_id)", {
                               'user_id': user_id,
                               'contest_id': contest_id
                           })

    def is_participant(self, user_id: int, contest_id: int) -> bool:
        self.execute_query("SELECT * FROM participations WHERE "
                           "user_id = :user_id "
                           "AND contest_id = :contest_id",
                           {
                               'user_id': user_id,
                               'contest_id': contest_id
                           })
        return self.cursor.fetchone() is not None

    def update_all_contests(self, timestamp: datetime.datetime) -> None:
        int_timestamp = self.datetime_to_int(timestamp)
        self.execute_query("UPDATE contests SET status = :new_status "
                           "WHERE start_timestamp > :current_timestamp",
                           {
                               "new_status": contests.STATUS_BEFORE,
                               'current_timestamp': int_timestamp
                           })

        self.execute_query("UPDATE contests SET status = :new_status "
                           "WHERE start_timestamp <= :current_timestamp AND "
                           "end_timestamp >= :current_timestamp",
                           {
                               "new_status": contests.STATUS_RUNNING,
                               'current_timestamp': int_timestamp
                           })

        self.execute_query("UPDATE contests SET status = :new_status "
                           "WHERE end_timestamp < :current_timestamp ",
                           {
                               "new_status": contests.STATUS_FINISHED,
                               'current_timestamp': int_timestamp
                           })

    def get_contest_by_id(self, contest_id) -> Optional[Contest]:
        self.execute_query("SELECT * FROM contests WHERE "
                           "id = :id", {
                               'id': contest_id
                           })
        row = self.cursor.fetchone()
        if row is None:
            return None
        return Contest(contest_id=row[0], owner_id=row[1], name=row[2], start_date=self.int_to_datetime(row[3]),
                       end_date=self.int_to_datetime(row[4]), status=row[5])

    def get_contest_portfolio_for_user_id(self, user_id: int, contest_id: int) -> Optional[Portfolio]:
        self.execute_query("SELECT * FROM portfolios WHERE "
                           "owner_id = :owner_id AND contest_id = :contest_id", {
                               'owner_id': user_id,
                               'contest_id': contest_id
                           })
        row = self.cursor.fetchone()
        return row if row is None else Portfolio(portfolio_id=row[0], owner_id=row[1], name=row[2], contest_id=row[3])

    def add_short_transaction_batch(self, batch: Iterable[ShortTransaction]) -> None:
        self.execute_query("BEGIN TRANSACTION", commit=False)
        for transaction in batch:
            self.execute_query(
                "INSERT INTO short_transactions (portfolio_id, ticker, quantity, timestamp) VALUES "
                "(:portfolio_id, :ticker, :quantity, :timestamp)", {
                    'portfolio_id': transaction.portfolio_id,
                    'ticker': transaction.ticker,
                    'quantity': transaction.quantity,
                    'timestamp': self.datetime_to_int(transaction.timestamp),
                }, commit=False)
        self.execute_query("COMMIT TRANSACTION")
        self.connection.commit()

    def get_ready_short_transactions(self, timestamp: Optional[datetime.datetime] = None) -> List[ShortTransaction]:
        if timestamp is None:
            timestamp = datetime.datetime.now()
        self.execute_query("SELECT * FROM short_transactions WHERE "
                           "timestamp <= :timestamp",
                           {'timestamp': self.datetime_to_int(timestamp)})
        return [
            ShortTransaction(
                transaction_id=int(row[0]),
                portfolio_id=int(row[1]),
                ticker=str(row[2]),
                quantity=int(row[3]),
                timestamp=self.int_to_datetime(int(row[4]))
            )
            for row in self.cursor.fetchall()]

    def remove_short_transaction(self, transaction_id: int) -> None:
        self.execute_query("DELETE FROM short_transactions WHERE id = :id", {'id': transaction_id})

    def get_current_shorts(self, portfolio_id: int) -> List[ShortTransaction]:
        self.execute_query(
            "SELECT * FROM short_transactions "
            "WHERE portfolio_id = :portfolio_id",
            {
                'portfolio_id': portfolio_id
            })

        return [
            ShortTransaction(
                transaction_id=int(row[0]),
                portfolio_id=int(row[1]),
                ticker=str(row[2]),
                quantity=int(row[3]),
                timestamp=self.int_to_datetime(int(row[4]))
            )
            for row in self.cursor.fetchall()]
