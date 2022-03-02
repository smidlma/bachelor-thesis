import logging as log
import pandas as pd
from pandas.io.json import build_table_schema
import psycopg2
from sqlalchemy import create_engine, table
from models import *
import mongoengine as mongo


def main():
    pass
    # connect to mongo
    # mongo.connect('mongo-etl')
    # init loger
    # log.basicConfig(format='%(asctime)s - %(message)s', level=log.NOTSET)

    # connection = PostgreSQLConnection(
    #     host='localhost', port=5432, user='smidlma', password='', database='warehouse')
    # CSV
    # csvSource = CSV(sourceName='Source one', fileName='mock.csv').save()
    # c = Source.objects().first()
    # print(c.testConnection(), c.filePath)

    # postSource = PostgreSQL(sourceName='Postgres',
    #                         tableName='import', connection=connection)

    # print(postSource.generateSample())
    # log.debug(postSource.defaultSchema)

    # create pipelibe
    # destination = PostgreSQLDest('My dest', 'import', connection)

    # pg = PostgreSQLConnection.objects(host='localhost').first()
    # pg.connect()

    # pipeline = Pipeline('Move pipeline')

    # pipeline.addSource(csvSource)
    # pipeline.setDestination(destination)
    # pipeline.run()


if __name__ == '__main__':
    main()
