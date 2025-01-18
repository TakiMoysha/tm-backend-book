from datetime import datetime
from typing import List

from robyn import Request, Response, SubRouter

from .models import Order, OrdersPage


router = SubRouter(__file__)


@router.get("/")
async def h(request: Request):
    return "Hello :)"


@router.get("/static/{static_path}")
async def static_files(request: Request):
    print(request.path_params.get("static_path"))
    return "done"


@router.get("/test/orders")
async def test_orders(request: Request):
    orders: List[Order] = []
    for k in range(10):
        orders.append(
            Order(
                symbol=str(k),
                instrument_id=str(k),
                side="buy",
                volume=50,
                start_time=datetime.now().isoformat(timespec="milliseconds"),
                end_time=datetime.now().isoformat(timespec="milliseconds"),
            )
        )

    data = OrdersPage(number=1, size=10, content=orders).model_dump_json()
    return Response(
        status_code=200,
        headers={"Content-Type": "application/json"},
        description=data,
    )
