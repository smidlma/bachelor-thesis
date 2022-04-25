from email.policy import default
from enum import Enum
from pandas import DataFrame
import etl.models.connections as con
import pandas as pd
import mongoengine as mongo
from bson import ObjectId
import logging as log


class InsertOption(Enum):
    """
    Insert Type options when moving data to destination
    """

    APPEND = "append"
    REPLACE = "replace"
    FAIL = "fail"


class Destination(mongo.EmbeddedDocument):
    """
    Destination base class for general functionality
    """

    id = mongo.ObjectIdField(default=ObjectId)
    destinationName = mongo.StringField()
    targetTable = mongo.StringField()
    connection = mongo.ReferenceField(con.Connection)
    insertOption = mongo.StringField(default=InsertOption.REPLACE.value)

    meta = {"allow_inheritance": True}

    def __init__(
        self,
        destinationName: str,
        targetTable: str,
        connection: con.Connection,
        insertOption: str,
        **data
    ) -> None:
        super(Destination, self).__init__(
            destinationName=destinationName,
            targetTable=targetTable.lower(),
            connection=connection,
            insertOption=insertOption,
            **data
        )

    def load(self, df: DataFrame):
        if not self.connection.isConnected():
            self.connection.connect()
        log.info("Before load")
        rowsAffected = df.to_sql(
            self.targetTable, self.connection.con, if_exists=self.insertOption
        )
        log.info("After log")
        self.connection.close()
        return rowsAffected

    def update(self, data):
        self.destinationName = data["name"]
        self.targetTable = data["targetTable"]
        newCon = con.Connection.objects(id=data["connection"]).first()
        self.connection = newCon
        self.insertOption = data["insertOption"]

    def json(self):
        return {
            "id": str(self.id),
            "destinationName": self.destinationName,
            "targetTable": self.targetTable,
            "connection": self.connection.json(),
            "insertOption": self.insertOption,
        }


class PostgreSQLDest(Destination):
    """
    PostgreSQLDest class sepcific for postgres
    """

    def __init__(
        self,
        destinationName: str,
        targetTable: str,
        connection: con.Connection,
        insertOption: str,
        **data
    ) -> None:
        super(PostgreSQLDest, self).__init__(
            destinationName=destinationName,
            targetTable=targetTable.lower(),
            connection=connection,
            insertOption=insertOption,
            **data
        )

    def update(self, data):
        return super().update(data)

    def json(self):
        return super().json()
