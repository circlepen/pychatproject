from fastapi import WebSocket
from typing import List
import asyncio
from typing import Optional

# manager
class SocketManager:
    """a manager to control websocket actions"""
    def __init__(self):
        self.active_connections: List[(WebSocket, str)] = []

    async def connect(self, websocket: WebSocket, user: str, target: Optional[str]=None):
        await websocket.accept()
        if target:
            roomid = "".join(sorted([user, target]))
        else:
            roomid = ""
        self.active_connections.append({"ws": websocket, "user": user, "id": roomid})

    def disconnect(self, websocket: WebSocket, user: str, target: Optional[str]=None):
        if target:
            roomid = "".join(sorted([user, target]))
        else:
            roomid = ""
        self.active_connections.remove({"user": user, "ws": websocket, "id": roomid})

    async def send_personal_message(self, message: dict, user: str, target: str):
        # 發送個人訊息
        roomid = "".join(sorted([user, target]))
        for connection in self.active_connections:
            if connection["id"] == roomid:
                await connection['ws'].send_json(message)

    async def broadcast(self, data: dict):
        for connection in self.active_connections:
                await connection["ws"].send_json(data)

ws_manager = SocketManager()
