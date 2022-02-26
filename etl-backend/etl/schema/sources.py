from os.path import exists
import config
import pandas as pd
from pandas.io.json import build_table_schema
from .connections import *


# Source base class with general functionality
class Source:
    def __init__(self, sourceName) -> None:
        self._df_sample = None
        self.sourceName = sourceName
        self.defaultSchema = build_table_schema(self.generateSample())

    @property
    def df_sample(self) -> pd.DataFrame:
        return self._df_sample

    @df_sample.setter
    def df_sample(self, data: pd.DataFrame):
        self._df_sample = data

    def testConnection(self) -> bool:
        pass

    def generateSample(self) -> pd.DataFrame:
        pass

    def extract(self) -> pd.DataFrame:
        pass


# CSV source class
class CSV(Source):
    def __init__(self, name: str, fileName: str) -> None:
        self.fileName = fileName
        self.filePath = f'{config.FILE_STORAGE_PATH}{self.fileName}'
        super().__init__(name)

    def testConnection(self) -> bool:
        return exists(self.filePath)

    def generateSample(self) -> pd.DataFrame:
        self.df_sample = pd.read_csv(self.filePath, nrows=1)
        return self.df_sample

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.filePath)

# PostgreSQL class
class PostgreSQL(Source):
    def __init__(self, name: str, tableName: str, connection: PostgreSQLConnection) -> None:
        self.tableName = tableName
        self.connection = connection

        super().__init__(name)

    def testConnection(self) -> bool:
        return self.connection.isConnected()

    def generateSample(self) -> pd.DataFrame:
        self.df_sample = pd.read_sql(f'SELECT * FROM {self.tableName};')
        return self.df_sample
