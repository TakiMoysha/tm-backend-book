from typing import List
from pydantic import BaseModel


class Order(BaseModel):
    symbol: str
    instrument_id: str
    side: str
    volume: int
    # value: float

    start_time: str
    end_time: str


## insted Responses
class OrdersPage(BaseModel):
    number: int
    size: int
    content: List[Order]
