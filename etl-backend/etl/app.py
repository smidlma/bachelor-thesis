from schema.sources import *
import pandas as pd
from pandas.io.json import build_table_schema
import psycopg2
from sqlalchemy import create_engine

def main():
    # sources = []
    # csv = CSV('csv', 'mock.csv')
    # sources.append(csv)
    # print(csv.testConnection())

    # df = pd.read_csv('etl/file-storage/mock.csv', nrows=1)
    # schema = build_table_schema(df)
    # print(schema)
    engine = create_engine('postgresql+psycopg2://test:@127.0.0.1', pool_recycle=3600)
    try:
        con = engine.connect()
    except:
        con = None
    print(con)








if __name__ == '__main__':
    main()