from enum import Enum
from fastapi import WebSocket
from etl.models.pipeline import Pipeline

class Command(Enum):
    INIT_STATE = 'INIT_STATE'
    OPEN_PIPELINE = 'OPEN_PIPELINE'
    CLOSE_PIPELINE = 'OPEN_PIPELINE'
    RUN_PIPELINE = 'RUN_PIPELINE'
    ADD_SOURCE = 'ADD_SOURCE'
    REMOVE_SOURCE = 'REMOVE_SOURCE'
    ADD_TRANSFORMATION = 'ADD_TRANSFORMATION'
    REMOVE_TRANSFORMATION = 'REMOVE_TRANSFORMATION'


    
class ConnectionManager:
    def __init__(self):
        self.active_connections:list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, message:dict):
        for connection in self.active_connections:
            await connection.send_json(message)



class Store:
    def __init__(self) -> None:
        self.pipeline = Pipeline.objects(name='My pip').first()


class WorkSpaceManager:
    def __init__(self) -> None:
        self.connectionManager = ConnectionManager()
        self.store = Store()
    
    async def handleMsg(self, msg: dict):
       await self.connectionManager.send(self.store.pipeline.to_json())





