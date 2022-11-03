import asyncio

import uvicorn
import websockets
from fastapi import WebSocket, FastAPI
from websockets.typing import Subprotocol

app = FastAPI()


STOMP_URL = "ws://localhost:15674/ws"


async def forward(ws: WebSocket, stomp_ws: websockets.WebSocketClientProtocol):
    while True:
        data = await ws.receive_bytes()
        print("websocket A received:", data)
        await stomp_ws.send(data)


async def reverse(ws: WebSocket, stomp_ws: websockets.WebSocketClientProtocol):
    while True:
        data = await stomp_ws.recv()
        await ws.send_text(data)
        print("websocket A sent:", data)


@app.websocket("/stomp")
async def websocket(ws: WebSocket):
    await ws.accept()
    print(ws.headers)
    stomp_ws: websockets.WebSocketClientProtocol
    async with websockets.connect(
        STOMP_URL, subprotocols=[Subprotocol("v10.stomp"), Subprotocol("v11.stomp")],
    ) as stomp_ws:
        fwd_task = asyncio.create_task(forward(ws, stomp_ws))
        rev_task = asyncio.create_task(reverse(ws, stomp_ws))
        await asyncio.gather(fwd_task, rev_task)


if __name__ == "__main__":
    uvicorn.run(app)
