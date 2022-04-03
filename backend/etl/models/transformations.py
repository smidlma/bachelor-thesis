import mongoengine as mongo
from numpy import source
import pandas as pd
import logging as log
from bson import ObjectId


class Transformation(mongo.EmbeddedDocument):
    """
    Base class for all transformations with general functionality
    """

    id = mongo.ObjectIdField(default=ObjectId)
    name = mongo.StringField()
    position = mongo.IntField()

    meta = {"allow_inheritance": True}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def update(self, data):
        pass

    def json(self):
        return {"id": str(self.id), "name": self.name, "position": self.position}


class Sort(Transformation):
    """
    Sort class sorts dataframe
    """

    column = mongo.StringField()
    ascending = mongo.BooleanField(default=True)

    def __init__(self, *args, **values):
        if "name" not in values:
            values["name"] = "Sort"
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        log.info(f"RUNNING SORT:,{self.column}, {self.ascending}")
        return df.sort_values(by=self.column, ascending=self.ascending)

    def update(self, data):
        self.column = data["column"]
        self.ascending = data["ascending"]

    def json(self):
        res = super().json()
        res["column"] = self.column
        res["ascending"] = self.ascending
        return res


class MaskColumn(Transformation):
    """
    MaskColumn class masks column in dataframe
    """

    column = mongo.StringField()

    def __init__(self, *args, **values):
        if "name" not in values:
            values["name"] = "Mask"
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.column] = "####"
        return df

    def update(self, data):
        self.column = data["column"]

    def json(self):
        res = super().json()
        res["column"] = self.column
        return res


class DateFilter(Transformation):
    """
    Date filter {column: birth, op: gt| ls| between, datetimes: [....]} filter dates columns
    """

    column = mongo.StringField()
    op = mongo.StringField()
    datetimes = mongo.ListField()

    def __init__(self, *args, **values):
        if "name" not in values:
            values["name"] = "DateFilter"
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.op == "gt":
            return df.loc[
                df[self.column] >= pd.to_datetime(self.datetimes[0], unit="ms")
            ]
        elif self.op == "lt":
            return df.loc[
                df[self.column] <= pd.to_datetime(self.datetimes[0], unit="ms")
            ]
        elif self.op == "between":
            return df.loc[
                (df[self.column] >= pd.to_datetime(self.datetimes[0], unit="ms"))
                & (df[self.column] < pd.to_datetime(self.datetimes[1], unit="ms"))
            ]

    def update(self, data):
        self.column = data["column"]
        self.op = data["op"]
        self.datetimes = data["datetimes"]

    def json(self):
        return {
            **super().json(),
            "column": self.column,
            "op": self.op,
            "datetimes": self.datetimes,
        }


class ValueFilter(Transformation):
    """
    Value filter filter numeric columns
    """

    column = mongo.StringField()
    op = mongo.StringField()
    vals = mongo.ListField()

    def __init__(self, *args, **values):
        if "name" not in values:
            values["name"] = "ValueFilter"
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.op == "gt":
            return df.loc[df[self.column] >= self.vals[0]]
        elif self.op == "lt":
            return df.loc[df[self.column] <= self.vals[0]]
        elif self.op == "between":
            return df.loc[
                (df[self.column] >= self.vals[0]) & (df[self.column] < self.vals[0])
            ]

    def update(self, data):
        self.column = data["column"]
        self.op = data["op"]
        self.vals = data["vals"]

    def json(self):
        return {
            **super().json(),
            "column": self.column,
            "op": self.op,
            "vals": self.vals,
        }
