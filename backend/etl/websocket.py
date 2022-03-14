from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from etl.workspace import WorkSpaceManager
import logging as log
import mongoengine as mongo

mongo.connect('mongotest')

router = APIRouter()
manager = WorkSpaceManager()

@router.websocket("/ws", format)
async def websocket_endpoint(websocket: WebSocket, client_id = 0):
    await manager.connectionManager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_json()
            log.info(msg)
            await manager.handleMsg(msg)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # await manager.broadcast(f"Client #{client_id} left the chat")