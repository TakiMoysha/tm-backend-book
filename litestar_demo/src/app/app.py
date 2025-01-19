from litestar import Litestar
from litestar.plugins.structlog import StructlogPlugin
from litestar_granian import GranianPlugin

from app.handlers import router


def create_app() -> Litestar:
    app = Litestar(
        plugins=[
            StructlogPlugin(),
            GranianPlugin(),
        ],
        route_handlers=[router],
    )

    return app

