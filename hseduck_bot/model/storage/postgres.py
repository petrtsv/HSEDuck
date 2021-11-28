import re
from typing import Dict, Any, Optional

import psycopg2
from psycopg2._psycopg import cursor

from hseduck_bot.model.storage.general_sql import AbstractSQLStorage


class PostgresStorage(AbstractSQLStorage):
    def __init__(self, conn_string):
        super().__init__()
        self.conn_string = conn_string
        self.connection = None
        self.cursor: Optional[cursor] = None

    SQLITE_TO_POSTGRES_REGEX = re.compile(r':(\w+)\b')

    def execute_query(self, template: str, args: Dict[str, Any] = None, commit=True) -> None:
        template = re.sub(self.SQLITE_TO_POSTGRES_REGEX, r'%(\1)s', template)
        self.cursor.execute(template, args) if args is not None else self.cursor.execute(template)
        if commit:
            self.connection.commit()

    def init(self):
        self.connection = psycopg2.connect(self.conn_string)
        self.cursor = self.connection.cursor()

    def close(self) -> None:
        self.connection.close()
