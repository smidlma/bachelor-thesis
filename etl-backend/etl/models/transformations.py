import mongoengine as mongo
from numpy import source
import pandas as pd
import logging as log


class Transformation(mongo.Document):
    name = mongo.StringField()
    position = mongo.IntField()

    meta = {'allow_inheritance': True}

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        pass


class Sort(Transformation):
    columns = mongo.ListField(mongo.StringField())
    ascending = mongo.BooleanField(default=True)

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        log.info(f'RUNNING SORT:,{self.columns}, {self.ascending}')
        return df.sort_values(by=self.columns, ascending=self.ascending)




# Mask single or multiple cols with ####
class MaskColumn(Transformation):
    columns = mongo.ListField(mongo.StringField())

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df[self.columns] = "####"
        return df


# Drop single or multiple cols
class DropColumn(Transformation):
    columns = mongo.ListField(mongo.StringField())

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=self.columns)

class Validate(Transformation):
    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return super().transform(df)

# {"result" : {""}}
class Filter(Transformation):
    columns = mongo.DictField()

    def __init__(self, *args, **values):
        super().__init__(*args, **values)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for key, value in self.columns:
            df = df[df[key]]



class RemoveDuplicates(Transformation):
    pass
