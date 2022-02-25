from os.path import exists

from numpy import number
import config
import pandas as pd
from pandas.io.json import build_table_schema
import psycopg2
from sqlalchemy import create_engine


class Source:
    def __init__(self, name) -> None:
        self.name = name
        self.defaultSchema = None
        
    def testConnection(self) -> bool:
        pass

    def getSample(self) -> pd.DataFrame:
        pass


class Connection:
    def __init__(self, host, port, user, password, database) -> None:
        self.con = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
    
    def connect(self):
        pass

    def close(self):
        if self.con is not None:
            self.con.close()

    def is_connected(self) -> bool:
        self.connect()
        if self.con is None:
            return False
        else:
            return True


class PostgreSQLConnection(Connection):
    def __init__(self, host:str, port:number, user:str, password:str, database:str) -> None:
        super().__init__(host, port, user, password, database)

    def connect(self):
        engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
        try:
            self.con = engine.connect()
        except:
            self.con = None
        

class CSV(Source):
    def __init__(self, name:str, fileName:str) -> None:
        self.fileName = fileName
        self.filePath = f'{config.FILE_STORAGE_PATH}{self.fileName}'
        self.defaultSchema = build_table_schema(self.getSample())
        super().__init__(name)
    
    def testConnection(self) -> bool:
        return exists(self.filePath)
    
    def getSample(self) -> pd.DataFrame:
        return pd.read_csv(self, nrows=1)


class PostgreSQL(Source):
    def __init__(self, name:str, tableName:str, connection:Connection) -> None:
        self.tableName = tableName
        self.connection = connection
        super().__init__(name)

    def testConnection(self) -> bool:
        return self.connection.is_connected()

    def getSample(self) -> pd.DataFrame:
        return super().getSample()