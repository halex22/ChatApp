from typing import List

from fastapi import WebSocket


class ConnectionWebSocketManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

    async def disconnect(self, websocket: WebSocket) -> None:
        # TODO - must handle exception properly here
        try:
            self.active_connections.remove(websocket)
        except Exception:
            return

    async def broadcast(self, message: str) -> None:
        # TODO - broadcast just to one user
        ...
