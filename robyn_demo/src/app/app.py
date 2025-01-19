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
        deps = app.dependencies.get_global_dependencies()
        logger.info("depenencies", deps=deps)
        from_dishka = deps.get("from_dishka")
        logger.info("depenencies", from_dishka=from_dishka)

        return "ok"

    # app.inject(database=DatabaseClient)
    # not working, use di.py and dishka
    # router.inject(database=MockCache)
    # router.inject(database=MockDatabase)
    setup_robyn_dishka(app)
    return app


def run_app():
    create_app().start(port=8000)
