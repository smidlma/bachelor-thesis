import csv
from email.policy import default
import json
from os.path import exists
import etl.config as config
import pandas as pd
from pandas.io.json import build_table_schema
import etl.models.transformations as tr
import etl.models.connections as con
import mongoengine as mongo
import logging as log
from bson import ObjectId


def convertToPandasTypes(type: str):
    """
    Util func to convert datatypes to padnas datatypes
    """
    if type == "integer":
        return "int64"
    elif type == "number":
        return "float64"
    elif type == "boolean":
        return "bool"
    elif type == "any":
        return "categorical"
    elif type == "string":
        return "object"
    elif type == "datetime":
        return "datetime64[ns]"


class Source(mongo.EmbeddedDocument):
    """
    Source base class with general functionality
    """

    id = mongo.ObjectIdField(default=ObjectId)
    name = mongo.StringField()
    transformations = mongo.EmbeddedDocumentListField(tr.Transformation)
    mappedSchema = mongo.DictField(default={"fields": [], "primaryKey": []})
    defaultSchema = mongo.DictField()

    meta = {"allow_inheritance": True}

    def __init__(self, **data) -> None:
        super(Source, self).__init__(**data)
        self._dfSample = self.preview()
        self.defaultSchema = build_table_schema(self.dfSample)

    @property
    def dfSample(self) -> pd.DataFrame:
        return self._dfSample

    @dfSample.setter
    def dfSample(self, data: pd.DataFrame):
        self._dfSample = data

    def testConnection(self) -> bool:
        pass

    def preview(self, nrows=5, mapped=False) -> pd.DataFrame:
        pass

    def extract(self) -> pd.DataFrame:
        pass

    def addTransformation(self, transformation: tr.Transformation):
        self.transformations.append(transformation)

    def runTransformations(self):
        dfTemp = self.extract()
        for tr in self.transformations:
            dfTemp = tr.transform(dfTemp)

        # print(dfTemp)
        return dfTemp

    def runTestTransformation(self, to=-1):
        dfTemp = self.preview()

        if to == -1:
            to = len(self.transformations)

        for idx in range(to):
            dfTemp = self.transformations[idx].transform(dfTemp)

        return dfTemp

    def setSchema(self, mappedSchema):
        self.mappedSchema = mappedSchema

    def update(self, data):
        pass

    def json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "defaultSchema": self.defaultSchema,
            "mappedSchema": self.mappedSchema,
            "transformations": [t.json() for t in self.transformations],
            "preview": json.loads(
                self.dfSample.reset_index().to_json(
                    orient="records",
                )
            ),
        }


#
class CSV(Source):
    """
    Class for CSV files
    """

    fileName = mongo.StringField()
    filePath = mongo.StringField()
    separator = mongo.StringField(default="\t")

    def __init__(self, name: str, fileName: str, **data) -> None:
        if "filePath" not in data:
            data["filePath"] = f"{config.FILE_STORAGE_PATH}{fileName}"
        super(CSV, self).__init__(name=name, fileName=fileName, **data)

        f = open(self.filePath)
        self.separator = (
            csv.Sniffer().sniff(f.readline(), [",", ";", "\t", " ", "|"]).delimiter
        )
        f.close()

    def testConnection(self) -> bool:
        return exists(self.filePath)

    def preview(self, nrows=5, mapped=False) -> pd.DataFrame:
        if mapped:
            fields = self.mappedSchema["fields"]
            cols = list(map(lambda x: x["name"], fields))
            types = {f["name"]: convertToPandasTypes(f["type"]) for f in fields}
            self.dfSample = pd.read_csv(
                self.filePath,
                nrows=nrows,
                sep=self.separator,
                engine="python",
                index_col=0,
                dtype=types,
                usecols=cols,
            )
        else:
            self.dfSample = pd.read_csv(
                self.filePath,
                nrows=nrows,
                sep=self.separator,
                engine="python",
                index_col=0,
            )
        return self.dfSample

    def extract(self) -> pd.DataFrame:
        fields = self.mappedSchema["fields"]
        cols = list(map(lambda x: x["name"], fields))
        types = {f["name"]: convertToPandasTypes(f["type"]) for f in fields}
        log.info(cols)
        log.info(types)

        df = pd.read_csv(
            self.filePath,
            sep=self.separator,
            engine="python",
            index_col=0,
            dtype=types,
            usecols=cols,
        ).drop_duplicates()
        log.info(df.shape)
        return df

    def json(self):
        res = super().json()
        res["fileName"] = self.fileName
        return res


class PostgreSQL(Source):
    """
    PostgreSQL class handles postgres as a source
    """

    tableName = mongo.StringField()
    connection = mongo.ReferenceField(con.Connection)

    def __init__(
        self, name: str, tableName: str, connection: con.Connection, **data
    ) -> None:
        # data['tableName'] = data['tableName'].lower()
        # print("Child constructor")
        super(PostgreSQL, self).__init__(
            name=name, tableName=tableName, connection=connection, **data
        )

    def testConnection(self) -> bool:
        return self.connection.isConnected()

    def preview(self, nrows=5, mapped=False) -> pd.DataFrame:
        if not self.testConnection():
            self.connection.connect()

        self.dfSample = pd.read_sql_query(
            f"SELECT * FROM {self.tableName} LIMIT {nrows};", self.connection.con
        )
        return self.dfSample

    def extract(self) -> pd.DataFrame:
        if not self.testConnection():
            self.connection.connect()

        fields = self.mappedSchema["fields"]
        cols = list(map(lambda x: x["name"], fields))
        types = {f["name"]: convertToPandasTypes(f["type"]) for f in fields}

        return pd.read_sql_query(
            f"SELECT * FROM {self.tableName};",
            self.connection.con,
        )

    def json(self):
        res = super().json()
        res["tableName"] = self.tableName
        res["connection"] = self.connection.json()
        return res


class Join(Source):
    """
    Join class its part of the Source family,
    to enable functionality as a source due to joining other sources
    """

    s1 = mongo.EmbeddedDocumentField("Source")
    s2 = mongo.EmbeddedDocumentField("Source")
    how = mongo.StringField()
    on = mongo.StringField()
    lsuffix = mongo.StringField(default="_left")
    rsuffix = mongo.StringField(default="_right")

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def join(self, df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        resDf = df1.join(
            other=df2,
            on=self.on,
            how=self.how,
            lsuffix=self.lsuffix,
            rsuffix=self.rsuffix,
        )
        return resDf

    def testConnection(self) -> bool:
        return None

    def preview(self) -> pd.DataFrame:
        return self.s1.preview().join(
            other=self.s2.preview(),
            on=self.on,
            how=self.how,
            lsuffix=self.lsuffix,
            rsuffix=self.rsuffix,
        )

    def extract(self) -> pd.DataFrame:
        return None

    def update(self, s1, s2, how):
        self.s1 = s1
        self.s2 = s2
        self.how = how

    def json(self):
        res = {
            "s1": self.s1.json(),
            "s2": self.s2.json(),
            "how": self.how,
            "on": self.on,
            "lsuffix": self.lsuffix,
            "rsuffix": self.rsuffix,
        }
        return {**super().json(), **res}
