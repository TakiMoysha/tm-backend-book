from sqlalchemy import create_engine
from config import AppConfig, get_config


class App:
    def __init__(self, config, engine) -> None:
        self.config = config


def create_app():
    import database

    app_config = get_config()
    engine = create_engine(app_config.database_uri)

    # database.Base.metadata.create_all(engine)
    app = App(app_config, engine)
    return app


app = create_app()
