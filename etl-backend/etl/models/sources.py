from email.policy import default
from os.path import exists
import etl.config as config
import pandas as pd
from pandas.io.json import build_table_schema
import etl.models.transformations as tr
import etl.models.connections as con
import mongoengine as mongo
import logging as log


# Source base class with general functionality
class Source(mongo.Document):
    name = mongo.StringField()
    transformations = mongo.ListField(mongo.ReferenceField(tr.Transformation))
    mappedSchema = mongo.DictField()

    meta = {'allow_inheritance': True}

    def __init__(self, **data) -> None:
        super(Source, self).__init__(**data)

        print('Base constructor')
        self.transformedData = None
        self._dfSample = self.generateSample()
        self.defaultSchema = build_table_schema(self.dfSample)

    @property
    def dfSample(self) -> pd.DataFrame:
        return self._dfSample

    @dfSample.setter
    def dfSample(self, data: pd.DataFrame):
        self._dfSample = data

    def testConnection(self) -> bool:
        pass

    def generateSample(self) -> pd.DataFrame:
        pass

    def extract(self) -> pd.DataFrame:
        pass

    def addTransformation(self, transformation: tr.Transformation):
        self.transformations.append(transformation)

    def runTransformations(self):
        dfTemp = self.extract()
        for tr in self.transformations:
            dfTemp = tr.transform(dfTemp)
            log.info(dfTemp)
        self.transformedData = dfTemp
        return dfTemp

    def setSchema(self, mappedSchema):
        self.mappedSchema = mappedSchema


# CSV source class
class CSV(Source):
    fileName = mongo.StringField()
    filePath = mongo.StringField()

    def __init__(self, name: str, fileName: str, **data) -> None:
        if 'filePath' not in data:
            data['filePath'] = f'{config.FILE_STORAGE_PATH}{fileName}'
        super(CSV, self).__init__(
            name=name, fileName=fileName, **data)

    def testConnection(self) -> bool:
        return exists(self.filePath)

    def generateSample(self) -> pd.DataFrame:
        self.dfSample = pd.read_csv(self.filePath, nrows=1)
        return self.dfSample

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.filePath)


# PostgreSQL class, tableName must be lowerCase
class PostgreSQL(Source):
    tableName = mongo.StringField()
    connection = mongo.ReferenceField(con.Connection)

    def __init__(self, name: str, tableName: str, connection: con.Connection, **data) -> None:
        # data['tableName'] = data['tableName'].lower()
        print('Child constructor')
        super(PostgreSQL, self).__init__(name=name,
                                         tableName=tableName, connection=connection, **data)

    def testConnection(self) -> bool:
        return self.connection.isConnected()

    def generateSample(self) -> pd.DataFrame:
        if not self.testConnection():
            self.connection.connect()

        self.dfSample = pd.read_sql_query(
            f'SELECT * FROM {self.tableName} LIMIT 1;', self.connection.con)
        return self.dfSample

    def extract(self) -> pd.DataFrame:
        if not self.testConnection():
            self.connection.connect()
        return pd.read_sql_query(f'SELECT * FROM {self.tableName};', self.connection.con)


# JOIN AS A SOURCE
class Join(Source):
    s1 = mongo.ReferenceField('Source')
    s2 = mongo.ReferenceField('Source')
    how = mongo.StringField()
    on = mongo.StringField()
    lsuffix = mongo.StringField(default='left')
    rsuffix = mongo.StringField(default='right')

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def join(self) -> pd.DataFrame:
        resDf = self.s1.transformedData.join(
            other=self.s2.transformedData, on=self.on, how=self.how, lsuffix=self.lsuffix, rsuffix=self.rsuffix)
        log.info(resDf)
        return resDf

    def testConnection(self) -> bool:
        return None

    def generateSample(self) -> pd.DataFrame:
        return self.s1.generateSample().join(other=self.s2.generateSample(), on=self.on, how=self.how, lsuffix=self.lsuffix, rsuffix=self.rsuffix)

    def extract(self) -> pd.DataFrame:
        return None
