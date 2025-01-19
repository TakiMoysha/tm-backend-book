from datetime import datetime

import aiomcache
import orjson
import structlog

from litestar import Router, get, Response

# from app.cache import CacheClient
# from app.database import DatabaseClient
from app.models import Order, OrdersPage

logger = structlog.get_logger()


@get("/health")
async def h() -> Response[bytes]:
    data = {
        "request": "ok" if "request" else "error",
        "database": "ok" if "database" else "error",
        "cache": "ok" if "cache" else "error",
    }
    return Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        content=orjson.dumps(data),
    )


@get("/orders")
async def orders_page() -> Response[bytes]:
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

    data = OrdersPage(number=1, size=page_size, content=orders)
    return Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        content=orjson.dumps(data),
    )


router = Router(path="/api", route_handlers=[h, orders_page])
