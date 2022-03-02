from etl import config
import etl.models.connections as conn
import etl.models.sources as source
import etl.models.destinations as destination
from etl.models.pipeline import Pipeline
import mongoengine as mongo
import logging as log

mongo.connect('mongotest')
log.basicConfig(format='%(asctime)s - %(message)s', level=log.NOTSET)


def test_csv():
    csv = source.CSV('csv', 'mock.csv').save()
    csvDB = source.CSV.objects(id=csv.id).first()

    assert csv.id == csvDB.id


def test_create_pipeline():

    pipeline = Pipeline('Test pipeline')
    csv = source.CSV('csv', 'mock.csv').save()

    connection = conn.PostgreSQLConnection(
        host='localhost', port=5432, user='smidlma', password='', database='warehouse').save()
    dest = destination.PostgreSQLDest(
        'testDest', 'import', connection=connection).save()

    pipeline.addSource(csv)
    pipeline.setDestination(dest)
    pipeline.save()
    # postgres = source.PostgreSQL(sourceName='Postgres',
    #                              tableName='import', connection=connection).save()
    log.info('hello')
    # assert connection.connect() == True


def test_load_run_pipeline():
    pipeline = Pipeline.objects(name='Test pipeline').first()
    rows = pipeline.run()
    assert rows == 1000