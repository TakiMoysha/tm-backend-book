from datetime import datetime

import aiomcache
import orjson
import structlog
from dishka.container import ContextWrapper

# from dishka.integrations.fastapi import FromDishka
from robyn import Request, Response, SubRouter

from app.cache import CacheClient
from app.consts import HeadersContentType
from app.database import DatabaseClient
from app.models import Order, OrdersPage

logger = structlog.get_logger()
router = SubRouter(__file__, prefix="/api")
router.inject(conn=DatabaseClient)
router.inject(cache=CacheClient)


@router.get("/health")
async def h(request: Request, global_dependencies) -> Response:
    # , database: MockDatabase, cache: MockCache
    deps_map = router.dependencies.get_global_dependencies()
    from_dishka = deps_map.get("from_dishka")
    conn = router.dependencies.get_router_dependencies(router).get("conn")
    logger.info("depenencies", conn=global_dependencies)

    if from_dishka is None:
        return Response(
            status_code=200,
            headers={"Content-Type": HeadersContentType.PLAIN},
            description="error",
        )

    container: ContextWrapper = from_dishka()
    database = container.container.get(DatabaseClient)
    cache = container.container.get(CacheClient)

    data = {
        "request": "ok" if request else "error",
        "database": "ok" if database else "error",
        "cache": "ok" if cache else "error",
    }
    return Response(
        status_code=200,
        headers={"Content-Type": HeadersContentType.JSON},
        description=orjson.dumps(data),
    )


@router.get("/static/{static_path}")
async def static_files(request: Request):
    print(request.path_params.get("static_path"))
    return "done"


@router.get("/orders")
async def orders_page(request: Request):
    page_size = 10
    orders = [
        Order(
            symbol=str(k),
            instrument_id=str(k),
            side="buy",
            volume=50,
            start_time=datetime.now().isoformat(timespec="milliseconds"),
            end_time=datetime.now().isoformat(timespec="milliseconds"),
        )
        for k in range(10)
    ]

    data = OrdersPage(number=1, size=page_size, content=orders).model_dump_json()
    return Response(
        status_code=200,
        headers={"Content-Type": HeadersContentType.JSON},
        description=data,
    )


@router.get("/orders/stats")
async def get_device_stats(request: Request, global_dependencies):
    try:
        # start_time = time.perf_counter()
        stats = await cache.stats()
        # H.labels(op="stats", db="memcache").observe(time.perf_counter() - start_time)

        return {
            "curr_items": stats.get(b"curr_items", 0),
            "total_items": stats.get(b"total_items", 0),
            "bytes": stats.get(b"bytes", 0),
            "curr_connections": stats.get(b"curr_connections", 0),
            "get_hits": stats.get(b"get_hits", 0),
            "get_misses": stats.get(b"get_misses", 0),
        }
    except aiomcache.exceptions.ClientException:
        logger.exception("Memcached error")
        raise Response(
            status_code=500,
            headers={"Content-Type": HeadersContentType.PLAIN},
            description="Memcached error occurred while retrieving stats",
        )
    except Exception:
        logger.exception("Unknown error")
        raise Response(
            status_code=500,
            headers={"Content-Type": HeadersContentType.PLAIN},
            description="An unexpected error occurred while retrieving stats",
        )
