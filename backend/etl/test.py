import json
from operator import index
import pandas as pd

from pandas.io.json import build_table_schema


def main():
    df = pd.read_csv(
        "file-storage/PatientCorePopulatedTable.txt",
        sep=",|;|\t",
        engine="python",
        index_col=0,
    )
    df2 = pd.read_csv(
        "file-storage/LabsCorePopulatedTable.txt",
        sep=",|;|\t",
        engine="python",
        index_col=0,
    )

    join = df.join(df2)
    # print(build_table_schema(join))
    # print(join.index)

    js = df.reset_index().to_json(orient="records", indent=4)

    print(js)

    # print(df)
    # print(df2.index)

    # print(build_table_schema(df, version=False))
    # print(build_table_schema(df2, version=False))

    # c = CSV(name="asdf", fileName="PatientCorePopulatedTable.txt")
    # print(c.preview())

    # # res = df.join(df2, 'PatientID')
    # print(df.dtypes)

    # df3 = pd.read_csv('file-storage/mock.csv')
    # print(df3.dtypes)
    # a = {"res" : {"operator" : "gt", "value": 50}}
    # print(a.res)


if __name__ == "__main__":
    main()
