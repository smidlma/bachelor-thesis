from abc import ABC,  abstractmethod
from mongoengine import Document, connect, StringField, BooleanField, ListField, ReferenceField

connect(db='mongo-etl')

class Source(Document):
    meta = {'allow_inheritance': True}

    name = StringField()
    
    @abstractmethod
    def getName(self):
        pass
       



class PostgreSQL(Source):
    connector = StringField()
    def getName(self):
        print(self.name, self.connector)


class CSV(Source):
    is_csv = BooleanField()
    def getName(self):
        print(self.name, self.is_csv)


class Pipeline(Document):
    sources = ListField(ReferenceField(Source))

# csv = CSV(name='csv', is_csv=True).save()
# sql = PostgreSQL(name='postgresql', connector='https').save()

# # csv.getName()
# # sql.getName()



# pipeline = Pipeline(sources=[csv, sql]).save()


for p in Pipeline.objects():
    for s in p.sources:
        s.getName()

