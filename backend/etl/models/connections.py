import psycopg2
from sqlalchemy import create_engine
import logging as log
import mongoengine as mongo


# Connection base class for general connection functionality
class Connection(mongo.Document):
    host = mongo.StringField()
    port = mongo.IntField()
    user = mongo.StringField()
    password = mongo.StringField()
    database = mongo.StringField()

    meta = {"allow_inheritance": True}

    def __init__(
        self, host: str, port: int, user: str, password: str, database: str, **data
    ) -> None:
        super(Connection, self).__init__(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            **data,
        )
        self.con = None

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

    def json(self):
        return {
            "id": str(self.id),
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
        }


class PostgreSQLConnection(Connection):
    def __init__(
        self, host: str, port: int, user: str, password: str, database: str, **data
    ) -> None:
        super().__init__(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            **data,
        )

    def connect(self) -> bool:
        connection_string = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        print(connection_string)
        log.debug(connection_string)
        engine = create_engine(connection_string)
        try:
            self.con = engine.connect()
            return True
        except Exception as e:
            self.con = None
            log.error(e)
            print(e)
            return False

    def json(self):
        return super().json()
