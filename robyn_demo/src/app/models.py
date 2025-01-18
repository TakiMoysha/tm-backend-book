from typing import List
from pydantic import BaseModel


class Asset(BaseModel):
    # symbol: str
    instrument_id: str
    volume: int
    # price: float


class ByPower(BaseModel):
    buy_power: float
    credit: float


class Portfolio(BaseModel):
    token: str
    id: str
    assets: List[Asset]
    buy_power: ByPower


class Order(BaseModel):
    symbol: str
    instrument_id: str
    side: str
    volume: int
    # value: float

    start_time: str
    end_time: str


class PairSignal(BaseModel):
    buy: List[Order]
    sell: List[Order]


## insted Responses
class OrdersPage(BaseModel):
    number: int
    size: int
    content: List[Order]
