import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import get_config
from app.workers import BaseWorker, ListenerWorker

logging.basicConfig(format="%(levelname)s [%(asctime)s]: %(message)s", level=logging.INFO)


def spawn_worker(worker: BaseWorker, STOP_EVENT: asyncio.Event):
    async def _async_task_processor():
        identity = asyncio.current_task().get_name()
        try:
            await worker.start(STOP_EVENT)
        except asyncio.CancelledError:
            pass
        logging.info(f"Worker {identity} stopped")

    return asyncio.create_task(_async_task_processor())


@asynccontextmanager
async def lifespan(app: FastAPI):
    WORKERS_STOP_EVENT = asyncio.Event()
    workers_pool = [ListenerWorker(get_config().source)]
    workers_tasks = tuple(spawn_worker(w, WORKERS_STOP_EVENT) for w in workers_pool)
    yield
    WORKERS_STOP_EVENT.set()
    await asyncio.gather(*workers_tasks, return_exceptions=True)


def bootstrap():
    app = FastAPI(lifespan=lifespan)
    app.state._config = get_config()

    return app


app = bootstrap()
