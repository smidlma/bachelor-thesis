from turtle import position
from etl import config
import etl.models.connections as conn
import etl.models.sources as source
import etl.models.destinations as destination
import etl.models.transformations as transformation
from etl.models.pipeline import Pipeline
import mongoengine as mongo
import logging as log
import pandas as pd

mongo.connect("mongotest")
log.basicConfig(format="%(asctime)s - %(message)s", level=log.NOTSET)


# def test_csv():
# csv = source.CSV('csv', 'mock.csv').save()
# csvDB = source.CSV.objects(id=csv.id).first()

# assert csv.id == csvDB.id


def test_create_pipeline():

    pipeline = Pipeline("Test pipeline")
    csv = source.CSV("csv", "mock.csv")

    connection = conn.PostgreSQLConnection(
        host="localhost", port=5432, user="smidlma", password="", database="warehouse"
    ).save()
    dest = destination.PostgreSQLDest("testDest", "import", connection=connection)

    pipeline.addSource(csv)
    pipeline.setDestination(dest)
    pipeline.save()
    # postgres = source.PostgreSQL(name='Postgres',
    #                              tableName='import', connection=connection).save()
    log.info("hello")
    # assert connection.connect() == True


def test_load_run_pipeline():
    pipeline = Pipeline.objects(name="Test pipeline").first()
    rows = pipeline.runTest()
    assert rows == 1000


def test_local_transformation():
    sortT = transformation.Sort(name="Sort", position=0, columns=["first_name"])
    sortT2 = transformation.Sort(name="Sort", position=1, columns=["ip_address"])
    csv = source.CSV("csv", "mock.csv")
    csv.addTransformation(sortT)
    csv.addTransformation(sortT2)
    res = csv.runTransformations()
    log.info(res)


def test_global_transformations():
    pip = Pipeline("My pip")
    connection = conn.PostgreSQLConnection(
        host="localhost", port=5432, user="smidlma", password="", database="warehouse"
    ).save()
    dest = destination.PostgreSQLDest("testDest", "import", connection=connection)
    sortT = transformation.Sort(name="Sort", position=0, columns=["first_name"])
    sortT2 = transformation.Sort(name="Sort", position=1, columns=["ip_address"])
    csv = source.CSV("Mock", "mock.csv")
    csv2 = source.CSV("CSV", "mock.csv")
    csv.addTransformation(sortT)
    csv2.addTransformation(sortT2)
    join = source.Join(name="Join", s1=csv, s2=csv2, on="id", how="left")
    pip.setDestination(dest)
    pip.addJoin(join)
    pip.addSource(csv)
    pip.addSource(csv2)
    pip.save()
    pip.run()


def test_load_pip_and_run():
    pipeline = Pipeline.objects(name="My pip").first()
    pipeline.run()