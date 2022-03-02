from os.path import exists

from numpy import delete
from sqlalchemy import table
import etl.config as config
import pandas as pd
from pandas.io.json import build_table_schema
from .connections import *
import mongoengine as mongo


# Source base class with general functionality
class Source(mongo.Document):
    sourceName = mongo.StringField()

    meta = {'allow_inheritance': True}

    def __init__(self, **data) -> None:
        super(Source, self).__init__(**data)

        print('Base constructor')
        self._df_sample = self.generateSample()
        self.defaultSchema = build_table_schema(self.df_sample)

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
    fileName = mongo.StringField()
    filePath = mongo.StringField()

    def __init__(self, sourceName: str, fileName: str, **data) -> None:
        if 'filePath' not in data:
            data['filePath'] = f'{config.FILE_STORAGE_PATH}{fileName}'
        super(CSV, self).__init__(
            sourceName=sourceName, fileName=fileName, **data)

    def testConnection(self) -> bool:
        return exists(self.filePath)

    def generateSample(self) -> pd.DataFrame:
        self.df_sample = pd.read_csv(self.filePath, nrows=1)
        return self.df_sample

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.filePath)


# PostgreSQL class, tableName must be lowerCase
class PostgreSQL(Source):
    tableName = mongo.StringField()
    connection = mongo.ReferenceField(Connection)

    def __init__(self, sourceName: str, tableName: str, connection: Connection, **data) -> None:
        # data['tableName'] = data['tableName'].lower()
        print('Child constructor')
        super(PostgreSQL, self).__init__(sourceName=sourceName,
                                         tableName=tableName, connection=connection, **data)

    def testConnection(self) -> bool:
        return self.connection.isConnected()

    def generateSample(self) -> pd.DataFrame:
        if not self.testConnection():
            self.connection.connect()

        self.df_sample = pd.read_sql_query(
            f'SELECT * FROM {self.tableName} LIMIT 1;', self.connection.con)
        return self.df_sample

    def extract(self) -> pd.DataFrame:
        if not self.testConnection():
            self.connection.connect()
        return pd.read_sql_query(f'SELECT * FROM {self.tableName};', self.connection.con)
