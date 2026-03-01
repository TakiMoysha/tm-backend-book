import sqlite3

from app.config import DatabaseConfig


class Database:
    def __init__(self, config: DatabaseConfig) -> None:
        self._config = config
        pass

    def __enter__(self):
        self.conn = sqlite3.connect(self._config.path)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    def execute(self, sql: str, *args):
        return self.conn.execute(sql, *args)
