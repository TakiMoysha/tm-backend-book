from robyn.dependency_injection import DependencyMap
import structlog

from robyn import Config, Robyn

from app.handlers import router
from app.di import setup_robyn_dishka

logger = structlog.get_logger()


def create_app() -> Robyn:
    config = Config()

    app = Robyn(__file__, config=config)
    app.include_router(router)

    @app.get("/")
    async def index(request):
        deps_map = DependencyMap().get_dependency_map(app)
        logger.info("depenencies", global_depenencies=deps_map)

        return "ok"

    # not working, use di.py and dishka
    # router.inject(database=MockCache)
    # router.inject(database=MockDatabase)
    setup_robyn_dishka(app)

    return app


def run_app():
    create_app().start(port=8000)
