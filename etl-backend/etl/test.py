
import logging as log
import pandas as pd
from pandas.io.json import build_table_schema
import psycopg2
from sqlalchemy import create_engine
from schema import *

def main():
    log.basicConfig(format='%(asctime)s - %(message)s', level=log.NOTSET)

    # Test postgres connection
    connection = PostgreSQLConnection('localhost', 5432, 'smidlma', '', 'warehouse')
    # print(connection.is_connected())
    
    # CSV
    csvSource = CSV('Source one', 'mock.csv')
    # print(csv.generateSample())
    
    # create pipelibe
    destination = PostgreSQLDest('My dest', 'importTest', connection)

    pipeline = Pipeline('Move pipeline')

    pipeline.addSource(csvSource)
    pipeline.setDestination(destination)

    pipeline.run()
    


if __name__ == '__main__':
    main()
