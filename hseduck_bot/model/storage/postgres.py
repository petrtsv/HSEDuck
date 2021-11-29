import re
from typing import Dict, Any, Optional, List

import psycopg2
from psycopg2._psycopg import cursor, connection
from psycopg2.extensions import TRANSACTION_STATUS_INERROR

from hseduck_bot.model.storage.general_sql import AbstractSQLStorage


class PostgresStorage(AbstractSQLStorage):
    def __init__(self, conn_string):
        super().__init__()
        self.conn_string = conn_string
        self.connection: Optional[connection] = None
        self.cursor: Optional[cursor] = None

    SQLITE_TO_POSTGRES_REGEX = re.compile(r':(\w+)\b')

    def execute_query(self, template: str, args: Dict[str, Any] = None, commit=True) -> None:
        if self.connection.get_transaction_status() == TRANSACTION_STATUS_INERROR:
            self.connection.rollback()

        template = re.sub(self.SQLITE_TO_POSTGRES_REGEX, r'%(\1)s', template)
        self.cursor.execute(template, args) if args is not None else self.cursor.execute(template)
        if commit:
            self.connection.commit()

    def init(self):
        self.connection = psycopg2.connect(self.conn_string)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()

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
                           "id SERIAL PRIMARY KEY, "
                           "username VARCHAR(64) NOT NULL UNIQUE)")

        self.execute_query("CREATE TABLE IF NOT EXISTS portfolios ("
                           "id SERIAL PRIMARY KEY, "
                           "owner_id BIGINT NOT NULL, "
                           "name VARCHAR(128) NOT NULL )")

        self.execute_query("CREATE TABLE IF NOT EXISTS transactions("
                           "portfolio_id BIGINT NOT NULL, "
                           "ticker VARCHAR(10) NOT NULL, "
                           "quantity BIGINT NOT NULL )")


