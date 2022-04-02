from traceback import print_tb
from turtle import position
from unicodedata import name
from etl import config
import etl.models.connections as conn
import etl.models.sources as source
import etl.models.destinations as destination
import etl.models.transformations as transformation
from etl.models.pipeline import Pipeline
import mongoengine as mongo
import logging as log
import pandas as pd

DATABASE = "mongotest"
db = mongo.connect(DATABASE)
db.drop_database(DATABASE)

log.basicConfig(format="%(asctime)s - %(message)s", level=log.NOTSET)


def test_date_filter():
    f = transformation.DateFilter(
        position=0,
        column="ASDF",
        op="gt",
        datetimes=["1183135260000"],
    )
    log.info(f.json())


def test_create_pipeline():
    pipeline = Pipeline("Pipeline A")
    csv = source.CSV("csv", "mock.csv")
    sortT = transformation.Sort(position=0, column="first_name")
    csv.addTransformation(sortT)
    schema = {
        "fields": [
            {"name": "id", "type": "integer"},
            {"name": "first_name", "type": "string"},
            {"name": "gender", "type": "string"},
        ],
        "primaryKey": ["id"],
    }
    csv.setSchema(schema)
    connection = conn.PostgreSQLConnection(
        host="localhost", port=5432, user="smidlma", password="", database="warehouse"
    ).save()
    dest = destination.PostgreSQLDest(
        destinationName="MyWareHouse",
        targetTable="mock",
        connection=connection,
        insertOption="append",
    )
    pipeline.addSource(csv)
    pipeline.setDestination(dest)
    pipeline.run()
    pipeline.save()


def test_create_pacient_pipeline():
    pipeline = Pipeline("Hospital pipeline")
    connection = conn.PostgreSQLConnection(
        host="localhost", port=5432, user="smidlma", password="", database="warehouse"
    ).save()
    dest = destination.PostgreSQLDest(
        "testDest", "hospital", connection=connection, insertOption="append"
    )
    pipeline.setDestination(dest)
    pipeline.save()


# def test_local_transformation():
#     sortT = transformation.Sort(position=0, column="first_name")
#     sortT2 = transformation.Sort(position=0, column="ip_address")
#     csv = source.CSV("csv", "mock.csv")
#     csv.addTransformation(sortT)
#     csv.addTransformation(sortT2)
#     res = csv.runTransformations()
#     log.info(res)


# def test_global_transformations():
#     pip = Pipeline("My pip")
#     connection = conn.PostgreSQLConnection(
#         host="localhost", port=5432, user="smidlma", password="", database="warehouse"
#     ).save()
#     dest = destination.PostgreSQLDest("testDest", "import", connection=connection)
#     sortT = transformation.Sort(position=0, column="LabUnits")
#     sortT2 = transformation.Sort(position=0, column="PatientLanguage")
#     csv = source.CSV("Labs", "LabsCorePopulatedTable.txt")
#     csv2 = source.CSV("Pacients", "PatientCorePopulatedTable.txt")
#     csv.addTransformation(sortT)
#     csv2.addTransformation(sortT2)
#     join = source.Join(name="Join", s1=csv, s2=csv2, on="PatientID", how="left")
#     pip.setDestination(dest)
#     pip.addJoin(join)
#     pip.addSource(csv)
#     pip.addSource(csv2)
#     pip.save()
#     pip.run()


# def test_load_pip_and_run():
#     pipeline = Pipeline.objects(name="My pip").first()
#     pipeline.run()
