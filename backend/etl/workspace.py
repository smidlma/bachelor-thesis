from enum import Enum
from typing import List
from fastapi import WebSocket
from etl.models.connections import Connection
from etl.models.pipeline import Pipeline
from etl.models.sources import CSV, Join, PostgreSQL
from etl.models.transformations import DateFilter, MaskColumn, Sort, ValueFilter


class TranformationFactory:
    @staticmethod
    def createTransformation(data):
        if data["type"] == "Sort":
            return Sort(
                column=data["column"],
                position=data["position"],
                ascending=data["ascending"],
            )
        elif data["type"] == "Mask":
            return MaskColumn(column=data["column"], position=data["position"])
        elif data["type"] == "DateFilter":
            return DateFilter(
                column=data["column"],
                position=data["position"],
                op=data["op"],
                datetimes=data["datetimes"],
            )
        elif data["type"] == "ValueFilter":
            return ValueFilter(
                column=data["column"],
                position=data["position"],
                op=data["op"],
                vals=data["vals"],
            )


class Command(Enum):
    INIT_STATE = "INIT_STATE"
    OPEN_PIPELINE = "OPEN_PIPELINE"
    CLOSE_PIPELINE = "CLOSE_PIPELINE"
    RUN_PIPELINE = "RUN_PIPELINE"
    ADD_SOURCE = "ADD_SOURCE"
    REMOVE_SOURCE = "REMOVE_SOURCE"
    ADD_TRANSFORMATION = "ADD_TRANSFORMATION"
    REMOVE_TRANSFORMATION = "REMOVE_TRANSFORMATION"
    SOURCE_SCHEMA_MAPPING = "SOURCE_SCHEMA_MAPPING"
    SHOW_SOURCE_PREVIEW = "SHOW_SOURCE_PREVIEW"
    ADD_JOIN = "ADD_JOIN"
    ADD_DESTINATION = "ADD_DESTINATION"


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, cmd, data: dict):
        resp = {"from": "BE", "to": "FE", "cmd": cmd, "data": data}
        for connection in self.active_connections:
            await connection.send_json(resp)


class PipelineBuilder:
    def __init__(self) -> None:
        self.pipeline = None

    def openPipeline(self, data):
        self.pipeline = Pipeline.objects(id=data["id"]).first()

    def closePipeline(self, data):
        self.pipeline = None

    def getPipelineJson(self):
        if self.pipeline is None:
            return None
        return self.pipeline.json()

    def schemaMapping(self, data):
        sourceId = data["sourceId"]
        s = next(filter(lambda x: str(x.id) == sourceId, self.pipeline.sources), None)
        schema = data["schema"]
        s.setSchema(schema)
        self.pipeline.save()

    def addSource(self, data):
        if data["sourceType"] == "csv":
            s = CSV(name=data["name"], fileName=data["fileName"])
            self.pipeline.addSource(s)
            self.pipeline.save()
        elif data["sourceType"] == "postgresql":
            c = Connection.objects(id=data["connection"]).first()
            s = PostgreSQL(name=data["name"], tableName=data["tableName"], connection=c)
            self.pipeline.addSource(s)
            self.pipeline.save()

    def addJoin(self, data):
        s1ID = data["s1"]
        s2ID = data["s2"]
        how = data["how"]
        s1 = next(filter(lambda x: str(x.id) == s1ID, self.pipeline.sources), None)
        s2 = next(filter(lambda x: str(x.id) == s2ID, self.pipeline.sources), None)

        if s1 is None:
            s1 = next(filter(lambda x: str(x.id) == s1ID, self.pipeline.joins), None)
        if s2 is None:
            s2 = next(filter(lambda x: str(x.id) == s2ID, self.pipeline.joins), None)

        if data["id"] is None:
            name = f"Join({s1.name} {how} {s2.name})"
            join = Join(name=name, s1=s1, s2=s2, how=how)
            self.pipeline.addJoin(join)
            self.pipeline.save()
        else:
            j = next(
                filter(lambda x: str(x.id) == data["id"], self.pipeline.joins),
                None,
            )

            j.update(s1, s2, how)
            self.pipeline.save()

    def addTransformation(self, data):
        s = next(
            filter(lambda x: str(x.id) == data["sourceId"], self.pipeline.sources), None
        )
        if data["id"] is None:
            pos = len(s.transformations) - 1
            data["position"] = pos
            tr = TranformationFactory.createTransformation(data)
            s.addTransformation(tr)
            self.pipeline.save()
        else:
            tr = next(
                filter(lambda x: str(x.id) == data["id"], s.transformations),
                None,
            )
            tr.update(data)
            self.pipeline.save()

    def addDestination(self, data):
        # update
        print(data)
        self.pipeline.destination.update(data)
        self.pipeline.save()


class WorkSpaceManager:
    def __init__(self) -> None:
        self.connectionManager = ConnectionManager()
        self.builder = PipelineBuilder()
        self.running = []

    async def sendInitState(self):
        await self.sendOpenedPipeline()
        await self.sendRunning()

    async def sendRunning(self):
        await self.connectionManager.send("RUNNING_PIPELINE", self.running)

    async def sendOpenedPipeline(self):
        await self.connectionManager.send("PIPELINE", self.builder.getPipelineJson())

    async def runPipeline(self, pipeline: Pipeline):
        if pipeline is None:
            return False
        print("task start")
        self.running.append(str(pipeline.id))
        await self.sendRunning()
        result = pipeline.run()
        await self.connectionManager.send("INFO", result)
        self.running.remove(str(pipeline.id))
        # await asyncio.sleep(10)
        await self.sendRunning()
        print("task end")
        return result

    async def handleMsg(self, msg: dict):
        if msg["cmd"] == Command.INIT_STATE.value:
            await self.sendInitState()
        elif msg["cmd"] == Command.OPEN_PIPELINE.value:
            self.builder.openPipeline(msg["data"])
            await self.sendOpenedPipeline()
        elif msg["cmd"] == Command.CLOSE_PIPELINE.value:
            self.builder.closePipeline(msg["data"])
            await self.sendOpenedPipeline()
        elif msg["cmd"] == Command.RUN_PIPELINE.value:
            res = await self.runPipeline(self.builder.pipeline)
            print(res)
        elif msg["cmd"] == Command.SOURCE_SCHEMA_MAPPING.value:
            self.builder.schemaMapping(msg["data"])
            await self.sendOpenedPipeline()
        elif msg["cmd"] == Command.ADD_SOURCE.value:
            self.builder.addSource(msg["data"])
            await self.sendOpenedPipeline()
        elif msg["cmd"] == Command.ADD_JOIN.value:
            self.builder.addJoin(msg["data"])
            await self.sendOpenedPipeline()
        elif msg["cmd"] == Command.ADD_TRANSFORMATION.value:
            self.builder.addTransformation(msg["data"])
            await self.sendOpenedPipeline()
        elif msg["cmd"] == Command.ADD_DESTINATION.value:
            self.builder.addDestination(msg["data"])
            await self.sendOpenedPipeline()
