from typing import List

from dataclasses import dataclass


@dataclass
class Order:
    symbol: str
    instrument_id: str
    side: str
    volume: int
    # value: float

    start_time: str
    end_time: str


@dataclass
class OrdersPage:
    number: int
    size: int
    content: List[Order]
