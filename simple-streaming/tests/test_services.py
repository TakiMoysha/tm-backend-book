import asyncio
import logging

import httpx
import httpx_ws
import pytest

from app.config import get_config
from app.workers import ListenerWorker

pytestmark = pytest.mark.asyncio

async def test_httpx_ws_connection():
    httpx_client = httpx.AsyncClient()
    async with httpx_ws.aconnect_ws("wss://ws-feed-public.sandbox.exchange.coinbase.com", httpx_client) as ws:
        await ws.send_json({"type": "subscribe", "product_ids": ["BTC-USD"], "channels": ["ticker_batch"]})
        logging.info(await ws.receive_text())


async def test_listener_worker():
    worker = ListenerWorker(get_config().source)
    STOP_EVENT = asyncio.Event()
    await worker.start(STOP_EVENT)
