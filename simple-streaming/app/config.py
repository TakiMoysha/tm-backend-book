import os
from dataclasses import dataclass
from dataclasses import field
from functools import lru_cache
import sqlite3


@dataclass
class SinkConfig:
    type: str = "clickhouse_connect"
    host: str = field(default_factory=lambda: os.getenv("APP__CLICKHOUSE_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("APP__CLICKHOUSE_PORT", 8123)))
    database: str = "coinbase"
    table: str = "coinbase_ticker"
    user: str = "coinbase"
    password: str = "demo_coinbase"


@dataclass
class SourceConfig:
    wss_url: str = "wss://ws-feed-public.sandbox.exchange.coinbase.com"
    type: str = "coinbase"

    @property
    def subscription(self):
        """customizable parameter, can be loaded from remote storage, file, etc."""
        return {
            "product_ids": ["BTC-USD", "ETH-USD"],
            "channels": ["ticker_batch"],
        }


@dataclass
class DatabaseConfig:
    path: str = field(default_factory=lambda: os.getenv("APP__DATABASE_PATH", "tmp/database.db"))

    def __post_init__(self):
        if not os.path.exists(self.path):
            self.create_database()

    def create_database(self):
        _test_db = ":memory:"
        con = sqlite3.connect(_test_db)
        con.execute("""
            CREATE TABLE IF NOT EXISTS coinbase_ticker (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                price REAL NOT NULL,
                volume REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP 
            )
        """)


@dataclass
class AppConfig:
    source = SourceConfig()
    sink = SinkConfig()
    database = DatabaseConfig()


@lru_cache(maxsize=1)
def get_config():
    return AppConfig()
