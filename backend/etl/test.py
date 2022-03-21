import pandas as pd

from pandas.io.json import build_table_schema


def main():
    df = pd.read_csv("file-storage/PatientCorePopulatedTable.txt", sep=",|;|\t")
    # df2 = pd.read_csv('file-storage/LabsCorePopulatedTable.txt', sep='\t')

    print(build_table_schema(df))
    print(df)

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
