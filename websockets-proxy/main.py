import asyncio
import logging
import signal

import websockets

STOMP_URL = "ws://localhost:15674/ws"


async def proxy(websocket, path):
    async with websockets.connect(STOMP_URL) as ws:
        client_to_server_task = asyncio.create_task(client_to_server(ws, websocket))
        server_to_client_task = asyncio.create_task(server_to_client(ws, websocket))

        await client_to_server_task
        await server_to_client_task


async def client_to_server(ws, websocket):
    async for message in ws:
        await websocket.send(message)


async def server_to_client(ws, websocket):
    async for message in websocket:
        await ws.send(message)


logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)


class LoggerAdapter(logging.LoggerAdapter):
    """Add connection ID and client IP address to websockets logs."""

    def process(self, msg, kwargs):
        try:
            websocket = kwargs["extra"]["websocket"]
        except KeyError:
            return msg, kwargs
        xff = websocket.request_headers.get("X-Forwarded-For")
        return f"{websocket.id} {xff} {msg}", kwargs


if __name__ == "__main__":
    async def server():
        loop = asyncio.get_running_loop()
        stop = loop.create_future()
        loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

        async with websockets.serve(proxy, "localhost", 8765):
            await stop

    asyncio.run(server())

