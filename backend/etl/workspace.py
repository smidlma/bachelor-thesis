from enum import Enum
from typing import List
from fastapi import WebSocket
from etl.models.pipeline import Pipeline


class Command(Enum):
    INIT_STATE = "INIT_STATE"
    OPEN_PIPELINE = "OPEN_PIPELINE"
    CLOSE_PIPELINE = "OPEN_PIPELINE"
    RUN_PIPELINE = "RUN_PIPELINE"
    ADD_SOURCE = "ADD_SOURCE"
    REMOVE_SOURCE = "REMOVE_SOURCE"
    ADD_TRANSFORMATION = "ADD_TRANSFORMATION"
    REMOVE_TRANSFORMATION = "REMOVE_TRANSFORMATION"
    SOURCE_SCHEMA_MAPPING = "SOURCE_SCHEMA_MAPPING"


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, data: dict):
        resp = {"from": "BE", "to": "FE", "data": data}
        for connection in self.active_connections:
            await connection.send_json(resp)


class PipelineBuilder:
    def __init__(self) -> None:
        self.pipeline = Pipeline.objects(name="My pip").first()

    def schemaMapping(self, data):
        sourceId = data["sourceId"]
        schema = data["schema"]
        s = next(filter(lambda x: str(x.id) == sourceId, self.pipeline.sources), None)
        s.setSchema(schema)
        self.pipeline.save()
        pass


class WorkSpaceManager:
    def __init__(self) -> None:
        self.connectionManager = ConnectionManager()
        self.store = PipelineBuilder()

    async def sendOpenedPipeline(self):
        await self.connectionManager.send(self.store.pipeline.json())

    async def handleMsg(self, msg: dict):
        if msg["cmd"] == Command.INIT_STATE.value:
            await self.sendOpenedPipeline()
        elif msg["cmd"] == Command.SOURCE_SCHEMA_MAPPING.value:
            self.store.schemaMapping(msg["data"])
            await self.sendOpenedPipeline()
