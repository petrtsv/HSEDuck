import sqlite3
from sqlite3 import Cursor
from typing import Dict, Any, Union

from hseduck_bot.model.storage.general_sql import AbstractSQLStorage


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

