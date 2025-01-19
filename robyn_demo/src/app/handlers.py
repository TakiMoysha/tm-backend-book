from datetime import datetime

import aiomcache
import orjson
import structlog
from robyn import Request, Response, SubRouter
from robyn.dependency_injection import DependencyMap

from app.cache import CacheClient
from app.consts import HeadersContentType
from app.database import DatabaseClient

from .models import Order, OrdersPage

logger = structlog.get_logger()
router = SubRouter(__file__, prefix="/api")


@router.get("/health")
async def h(request: Request):
    # , database: MockDatabase, cache: MockCache
    deps_map = DependencyMap().get_dependency_map(router)
    logger.info("depenencies", global_depenencies=deps_map)
    _request = "ok" if request else "error"
    _database = "ok" if "database" else "error"
    _cache = "ok" if "cache" else "error"

    data = {"request": _request, "database": _database, "cache": _cache}
    return Response(
        status_code=200,
        headers={"Content-Type": HeadersContentType.JSON},
        description=orjson.dumps(data),
    )


@router.get("/static/{static_path}")
async def static_files(request: Request, database: DatabaseClient, cache: CacheClient):
    print(request.path_params.get("static_path"))
    return "done"


@router.get("/orders")
async def test_orders(request: Request, database: DatabaseClient, cache: CacheClient):
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
async def get_device_stats(request: Request, database: DatabaseClient, cache: CacheClient):
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
