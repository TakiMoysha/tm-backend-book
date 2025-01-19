import structlog
from dishka import Container, Provider, Scope, make_container
from robyn import Robyn

from app.cache import CacheClient
from app.database import DatabaseClient

logger = structlog.get_logger()

import sqlite3
from typing import Iterable
from dishka import Provider, Scope, provide


class SQLiteMemoryProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def conn(self) -> Iterable[sqlite3.Connection]:
        conn = sqlite3.connect(":memory:")
        yield conn
        conn.close()


def get_container(app: Robyn) -> Container:
    provider = Provider(scope=Scope.REQUEST)
    provider.provide(CacheClient)
    provider.provide(DatabaseClient)

    container = make_container(provider, SQLiteMemoryProvider())

    logger.info("new container", container.get(CacheClient))
    return container


def setup_robyn_dishka(app: Robyn):
    container = get_container(app)
    app.dependencies.add_global_dependency(from_diska=container)
    # app.asgi_handler = make_add_request_container_middleware(app.asgi_handler)
    # app.state.dishka_container = container
