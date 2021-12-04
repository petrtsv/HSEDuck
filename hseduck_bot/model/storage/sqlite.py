import sqlite3
from sqlite3 import Cursor
from typing import Dict, Any, Union

from hseduck_bot.model.contests import Contest
from hseduck_bot.model.portfolios import Portfolio
from hseduck_bot.model.storage.general_sql import AbstractSQLStorage
from hseduck_bot.model.users import User


class SQLiteStorage(AbstractSQLStorage):
    def __init__(self, db_file):
        super().__init__()
        self.db_file = db_file
        self.connection = None
        self.cursor: Union[Cursor, None] = None

    def execute_query(self, template: str, args: Dict[str, Any] = None, commit=True) -> None:
        self.cursor.execute(template, args) if args is not None else self.cursor.execute(template)
        if commit:
            self.connection.commit()

    def init(self):
        self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()

    def create_user(self, user: User) -> None:
        if user is None:
            return
        self.execute_query("INSERT INTO users (username) VALUES "
                           "(:username) ON CONFLICT (username) DO NOTHING", {
                               'username': user.username
                           })
        user.id = self.cursor.lastrowid

    def create_portfolio(self, portfolio: Portfolio) -> None:
        if portfolio is None:
            return
        self.execute_query("INSERT INTO portfolios (owner_id, name, contest_id) VALUES "
                           "(:owner_id, :name, :contest_id)", {
                               'owner_id': portfolio.owner_id,
                               'name': portfolio.name,
                               'contest_id': portfolio.contest_id
                           })
        portfolio.id = self.cursor.lastrowid

    def new_contest(self, contest: Contest) -> None:
        if contest is None:
            return
        self.execute_query("INSERT INTO contests (owner_id, name, start_timestamp, end_timestamp, status) VALUES "
                           "(:owner_id, :name, :start_timestamp, :end_timestamp, :status)", {
                               'owner_id': contest.owner_id,
                               'name': contest.name,
                               'start_timestamp': self.datetime_to_int(contest.start_date),
                               'end_timestamp': self.datetime_to_int(contest.end_date),
                               'status': contest.status
                           })
        contest.id = self.cursor.lastrowid
