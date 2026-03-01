import logging
import httpx
from httpx_ws import aconnect_ws
from app.config import SourceConfig


class BaseWorker: ...


"""
Rate Limit:
    Requests per second per IP: 8
    Requests per second per IP in bursts: Up to 20
    Messages sent by the client every second per IP: 100
"""


class ListenerWorker(BaseWorker):
    def __init__(self, config: SourceConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(headers={"Sec-WebSocket-Extensions": "permessage-deflate"})

    async def start(self):
        """TODO: move to services.py"""
        async with aconnect_ws(self._config.wss_url, self._client) as ws:
            self._ws = ws
            subscribe_msg = {
                "type": "subscribe",
                "product_ids": self._config.subscription["product_ids"],
                "channels": self._config.subscription["channels"],
            }
            await ws.send_json(subscribe_msg)

            msg = await ws.receive_json()
            logging.info(msg)
