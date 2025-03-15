import json
import asyncio
import random
import structlog

from websockets import ConnectionClosedError
from websockets.asyncio.connection import Connection
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK
from websockets.server import Extension


logger = structlog.get_logger("server")

CONNECTIONS = {}


async def long_streaming_data(ws: Connection):
    for n in range(100):
        frame = {
            "id": n,
            "message": "test message",
        }
        await ws.send(json.dumps(frame))
        await asyncio.sleep(random.uniform(0.1, 0.3))


async def message_handler(ws: Connection):
    msg = await ws.recv()

    try:
        json_msg: dict = json.loads(msg)
    except json.JSONDecodeError:
        await ws.send(json.dumps({"error": "Invalid JSON"}))
        return

    if json_msg.get("subscribe"):
        asyncio.create_task(long_streaming_data(ws))

    response = {
        **json_msg,
        "peername": ws.transport.get_extra_info("peername"),
    }
    await ws.send(json.dumps(response))
    logger.info("Message: %s", json_msg)


async def connection_processing(ws: Connection):
    logger.info("Connection: %s", ws.transport.get_extra_info("peername"))
    conn_peername = ws.transport.get_extra_info("peername")
    CONNECTIONS[str(ws.id)] = ws
    while True:
        try:
            await message_handler(ws)
        except ConnectionClosedOK or ConnectionClosedError:
            pass
        finally:
            conn = CONNECTIONS.pop(str(ws.id))
            logger.info("Closed: %s (%s)", conn.id, conn_peername)
            break


async def server(host: str, port: int):
    async with serve(connection_processing, host, port) as server:
        await server.serve_forever()


def _server_runner():
    try:
        host, port = "0.0.0.0", 8001
        logger.info("Starting server: %s:%s", host, port)
        asyncio.run(server(host, port))
    except KeyboardInterrupt:
        logger.info("Server is stopping")
        pass
