from audioop import getsample
from os.path import exists
import config
import pandas as pd
from pandas.io.json import build_table_schema

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

    def is_connected(self) -> bool:
        if self.con is None:
            return False
        else:
            return True

class PostgreSQLConnection(Connection):
    def __init__(self, host, port, user, password, database) -> None:
        super().__init__(host, port, user, password, database)

    def connect(self):
        engine = create_engine(f'postgresql+psycopg2://test:@127.0.0.1', pool_recycle=3600)
        try:
            self.con = engine.connect()
        except:
            self.con = None
        


    

class CSV(Source):
    def __init__(self, name, fileName) -> None:
        self.fileName = fileName
        self.filePath = f'{config.FILE_STORAGE_PATH}{self.fileName}'
        self.defaultSchema = build_table_schema(self.getSample())
        super().__init__(name)
    
    def testConnection(self) -> bool:
        return exists(self.filePath)
    
    def getSample(self) -> pd.DataFrame:
        return pd.read_csv(self, nrows=1)

class PostgreSQL(Source):
    def __init__(self, name, table) -> None:
        self.table = table
        self.connection = Connection()
        super().__init__(name)

    def testConnection(self):
        return self.connection.is_connected()

    