import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import logging as log


# Connection base class for general connection functionality
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

    def isConnected(self) -> bool:
        if self.con is None:
            return False
        else:
            return True


class PostgreSQLConnection(Connection):
    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        super().__init__(host, port, user, password, database)
        self.connect()

    def connect(self) -> bool:
        connection_string = f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
        log.debug(connection_string)
        engine = create_engine(connection_string)
        try:
            self.con = engine.connect()
            return True
        except Exception as e:
            self.con = None
            log.error(e)
            return False