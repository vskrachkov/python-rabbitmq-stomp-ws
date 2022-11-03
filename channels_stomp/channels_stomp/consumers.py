import asyncio
import logging
from typing import Any, Optional

import websockets
from websockets.legacy.client import WebSocketClientProtocol

from channels.generic.websocket import AsyncWebsocketConsumer

log = logging.getLogger(__name__)

STOMP_URL = "ws://localhost:15674/ws"


class StompWebSocketConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._websocket_client: Optional[WebSocketClientProtocol] = None
        self._consumer_task: Optional[asyncio.Task] = None

    @property
    def websocket_client(self) -> WebSocketClientProtocol:
        if self._websocket_client is None:
            raise Exception("No connection to STOMP broker")
        return self._websocket_client

    async def connect(self):
        await self.accept()
        self._websocket_client = await websockets.connect(STOMP_URL)

        async def consumer_handler(websocket: WebSocketClientProtocol):
            async for message in websocket:
                await self.send(text_data=message)

        self._consumer_task = asyncio.create_task(consumer_handler(self.websocket_client))

    async def receive(self, text_data=None, bytes_data=None):
        await self.websocket_client.send(message=text_data or bytes_data)

    async def disconnect(self, close_code):
        if self._consumer_task:
            self._consumer_task.cancel()
        await self.websocket_client.close()
        await super().disconnect(close_code)
