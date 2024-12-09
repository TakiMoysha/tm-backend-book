from functools import lru_cache

class AppConfig:
    def __init__(self):
        self.database_uri = "sqlite:///db.sqlite3"


@lru_cache()
def get_config():
    return AppConfig()
