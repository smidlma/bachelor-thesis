from asyncio import sleep
import os
import time
from typing import Optional
from fastapi import FastAPI, Request, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
import mongoengine as mongo
import pandas as pd
from etl.models.connections import Connection, PostgreSQLConnection
from etl.models.destinations import Destination, PostgreSQLDest
from etl.models.pipeline import Pipeline
import logging as log
import etl.config as config
import etl.websocket as ws
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


class ConnectionModel(BaseModel):
    host: str
    port: int
    user: str
    password: Optional[str] = None
    database: str


class PipelineModel(BaseModel):
    pipelineName: str
    destinationName: str
    connectionId: str
    targetTable: str
    insertOption: str


app = FastAPI()
origins = config.ALLOW_ORIGINS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo.connect(host=config.MONGO_CON_STR)
log.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)",
    level=log.NOTSET,
)

app.include_router(ws.router)


@app.get("/")
async def get():
    return {"Hello": "World"}


########## Manage pipelines ##########
@app.get("/api/pipelines")
async def get():
    pip = Pipeline.objects()
    if pip is None:
        return []
    return [p.json() for p in pip]


@app.post("/api/pipelines")
async def createPipeline(body: PipelineModel):
    try:
        con = Connection.objects(id=body.connectionId).first()
        dest = PostgreSQLDest(
            destinationName=body.destinationName,
            targetTable=body.targetTable,
            insertOption=body.insertOption,
            connection=con,
        )
        pipeline = Pipeline(name=body.pipelineName)
        pipeline.setDestination(dest)
        pipeline.save()
        return {"created": True}
    except Exception as e:
        return {"created": False, "error": e}


# End point for automatic run
@app.get("/api/pipelines/run/{id}")
def runPipeline(id):
    time.sleep(5)
    return {"success": True, "message": f"Pipeline {id}, completed successfuly"}
    # try:
    #     p = Pipeline.objects(id=id).first()
    #     result = p.run()
    #     return result
    # except Exception as e:
    #     return {"success": False, "error": str(e)}


########## Manage connections ##########
@app.get("/api/connections")
async def getConnections():
    connections = Connection.objects()
    return [c.json() for c in connections]


@app.post("/api/connections")
async def createConnection(body: ConnectionModel):
    try:
        connection = PostgreSQLConnection(
            host=body.host,
            port=body.port,
            user=body.user,
            password=body.password,
            database=body.database,
        ).save()
        return {"created": True}

    except Exception as e:
        return {"created": False, "error": e}


@app.post("/api/connections/test")
async def testConnecion(body: ConnectionModel):
    connection = PostgreSQLConnection(
        host=body.host,
        port=body.port,
        user=body.user,
        password=body.password,
        database=body.database,
    )

    if connection.connect():
        return {"connected": True}
    else:
        return {"connected": False}


########## Manage files ##########
@app.get("/api/files")
async def getFiles():
    dir_name = config.FILE_STORAGE_PATH
    files = list()
    list_of_files = filter(
        lambda x: os.path.isfile(os.path.join(dir_name, x)), os.listdir(dir_name)
    )
    files_with_size = [
        (
            file_name,
            os.stat(os.path.join(dir_name, file_name)).st_size,
        )
        for file_name in list_of_files
    ]
    for fileName, fileSize in files_with_size:
        f = open(f"{dir_name}/{fileName}", "r")
        lines = [f.readline() for i in range(20)]
        f.close()
        files.append({"fileName": fileName, "fileSize": fileSize, "filePreview": lines})

    return files


@app.post("/api/files/upload")
async def uploadFile(file: UploadFile):
    try:
        content = await file.read()
        open(f"file-storage/{file.filename}", "wb").write(content)
        return {
            "upload": True,
        }
    except Exception as e:
        return {"upload": False, "error": e}
