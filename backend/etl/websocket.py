import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from etl.config import MONGO_CON_STR
from etl.workspace import WorkSpaceManager
import logging as log
import mongoengine as mongo

mongo.connect(host=MONGO_CON_STR)

router = APIRouter()
manager = WorkSpaceManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connectionManager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_json()
            log.info(msg)
            # await manager.handleMsg(msg)
            asyncio.create_task(manager.handleMsg(msg))

    except WebSocketDisconnect:
        manager.connectionManager.disconnect(websocket)
