from enum import Enum
from pandas import DataFrame
from .connections import Connection, PostgreSQLConnection
import pandas as pd

class TableOptions(Enum):
    APPEND = 'append'
    REPLACE = 'replace'
    FAIL = 'fail'
    
# Destination base class for general functionality
class Destination:
    def __init__(self, destinationName:str, targetTable:str, connection:Connection) -> None:
        self.destinationName = destinationName
        self.targetTable = targetTable
        self.connection = connection
    
    def load(self, df: DataFrame, tableOption:TableOptions):
        rowsAffected = df.to_sql(self.targetTable, self.connection.con, if_exists=tableOption.value)
        return rowsAffected

# PostgreSQL destination class
class PostgreSQLDest(Destination):
    def __init__(self, destinationName: str, targetTable: str, connection: PostgreSQLConnection) -> None:
        super().__init__(destinationName, targetTable, connection)

    