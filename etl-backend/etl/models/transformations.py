import mongoengine as mongo
import pandas as pd


class Transformation(mongo.Document):
    name = mongo.StringField()
    possition = mongo.IntField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self) -> pd.DataFrame:
        pass


class Sort(Transformation):
    columns = mongo.ListField(mongo.StringField())
    ascending = mongo.BooleanField(default=False)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.sort_values(by=self.columns, ascending=self.ascending)


class Remove(Transformation):
    pass


class Filter(Transformation):
    pass


class RemoveDuplicates(Transformation):
    pass
