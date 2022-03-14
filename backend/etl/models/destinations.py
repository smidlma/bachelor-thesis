from enum import Enum
from pandas import DataFrame
import etl.models.connections as con
import pandas as pd
import mongoengine as mongo
from bson import ObjectId

##


class InsertOption(Enum):
    APPEND = 'append'
    REPLACE = 'replace'
    FAIL = 'fail'


# Destination base class for general functionality
class Destination(mongo.EmbeddedDocument):
    id = mongo.ObjectIdField(default=ObjectId)
    destinationName = mongo.StringField()
    targetTable = mongo.StringField()
    connection = mongo.ReferenceField(con.Connection)

    meta = {'allow_inheritance': True}

    def __init__(self, destinationName: str, targetTable: str, connection: con.Connection, **data) -> None:
        super(Destination, self).__init__(destinationName=destinationName,
                                          targetTable=targetTable.lower(), connection=connection, **data)

    def load(self, df: DataFrame, tableOption: InsertOption):
        if not self.connection.isConnected():
            self.connection.connect()

        rowsAffected = df.to_sql(
            self.targetTable, self.connection.con, if_exists=tableOption.value)
        return rowsAffected


# PostgreSQL destination class
class PostgreSQLDest(Destination):
    def __init__(self, destinationName: str, targetTable: str, connection: con.Connection, **data) -> None:
        super(PostgreSQLDest, self).__init__(destinationName=destinationName,
                                             targetTable=targetTable.lower(), connection=connection, **data)
