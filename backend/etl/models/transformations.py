import mongoengine as mongo
from numpy import source
import pandas as pd
import logging as log
from bson import ObjectId


class Transformation(mongo.EmbeddedDocument):
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


# Mask single column
class MaskColumn(Transformation):
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
