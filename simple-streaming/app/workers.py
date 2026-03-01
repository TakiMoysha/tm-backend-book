import asyncio
import logging

import httpx
from httpx_ws import aconnect_ws

from app.config import SourceConfig


class BaseWorker:
    async def start(self, *args, **kwargs): ...


"""
Rate Limit:
    Requests per second per IP: 8
    Requests per second per IP in bursts: Up to 20
    Messages sent by the client every second per IP: 100
"""


class ListenerWorker(BaseWorker):
    def __init__(self, config: SourceConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient()

    async def start(self, stop_event: asyncio.Event):
        """TODO: move to services.py"""
        async with aconnect_ws(self._config.wss_url, self._client) as ws:
            subscribe_msg = {
                "type": "subscribe",
                "product_ids": self._config.subscription["product_ids"],
                "channels": self._config.subscription["channels"],
            }
            logging.info(subscribe_msg)
            await ws.send_json(subscribe_msg)

            while not stop_event.is_set():
                msg = await ws.receive_json()
                logging.info(msg)
