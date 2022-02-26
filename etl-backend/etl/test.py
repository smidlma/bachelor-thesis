
import logging as log
import pandas as pd
from pandas.io.json import build_table_schema
import psycopg2
from sqlalchemy import create_engine
from schema import *

def main():
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.NOTSET)

    connection = PostgreSQLConnection('localhost', 5432, 'smidlma', '', 'warehouse')
    # CSV
    csvSource = CSV('Source one', 'mock.csv')
    postSource = PostgreSQL('Postgres', 'importest', connection)
    log.debug(postSource.defaultSchema)
    
    # create pipelibe
    destination = PostgreSQLDest('My dest', 'importTest', connection)

    pipeline = Pipeline('Move pipeline')

    pipeline.addSource(postSource)
    pipeline.setDestination(destination)

    pipeline.run()
    


if __name__ == '__main__':
    main()
