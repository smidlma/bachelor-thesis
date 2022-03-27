from asyncio import sleep
import os
from typing import Optional
from fastapi import FastAPI, Request, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
import mongoengine as mongo
from etl.models.connections import Connection, PostgreSQLConnection
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


app = FastAPI()
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mongo.connect("mongotest")
log.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)",
    level=log.NOTSET,
)

app.include_router(ws.router)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

# @app.on_event('startup')
# def startup():
#     mongo.connect('mongotest')
@app.get("/")
async def get():
    return HTMLResponse(html)
    # return {file.filename}


########## Manage pipelines ##########
@app.get("/api/pipelines")
async def get():
    pip = Pipeline.objects()
    if pip is None:
        return []
    return [p.json() for p in pip]


@app.post("/api/pipelines")
async def createPipeline():
    return {"Not Implemented"}


########## Manage connections ##########
@app.get("/api/connections")
async def getConnections():
    await sleep(10)
    connections = Connection.objects()
    return [c.json() for c in connections]


@app.post("/api/connections")
async def createConnection():
    return {"Not Implemented"}


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


# postgresql+psycopg2://smidlma:@localhost:5432/warehouse
# postgresql+psycopg2://smidlma:@localhost:5423/warehouse
########## Manage files ##########
@app.get("/api/files")
async def getFiles():
    dir_name = config.FILE_STORAGE_PATH
    files = list()
    list_of_files = filter(
        lambda x: os.path.isfile(os.path.join(dir_name, x)), os.listdir(dir_name)
    )
    files_with_size = [
        (file_name, os.stat(os.path.join(dir_name, file_name)).st_size)
        for file_name in list_of_files
    ]
    print(files_with_size)
    for fileName, fileSize in files_with_size:
        files.append({"fileName": fileName, "fileSize": fileSize})

    return files


@app.post("/api/files/upload")
async def uploadFile(file: UploadFile):
    return {"Not Implemented"}
