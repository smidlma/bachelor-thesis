import json
from operator import index
import pandas as pd

from pandas.io.json import build_table_schema


def convertToPandasTypes(type: str):
    if type == "integer":
        return "int64"
    elif type == "number":
        return "float64"
    elif type == "boolean":
        return "bool"
    elif type == "any":
        return "category"
    elif type == "string":
        return "object"
    elif type == "datetime":
        return "datetime64[ns]"


def main():
    df = pd.read_csv(
        "file-storage/PatientCorePopulatedTable.txt",
        sep=",|;|\t",
        engine="python",
        index_col=0,
    )

    schema = build_table_schema(df)
    # print(schema)
    # s = {'PatientDateOfBirth': 'date'}

    # print(dfTest.dtypes)
    # print(dfTest)
    # print(build_table_schema(dfTest))

    mapped = {
        "fields": [
            {"name": "PatientID", "type": "string"},
            {"name": "PatientGender", "type": "any"},
            {"name": "PatientDateOfBirth", "type": "datetime"},
            # {"name": "PatientRace", "type": "string"},
            {"name": "PatientMaritalStatus", "type": "string"},
            {"name": "PatientLanguage", "type": "string"},
            {"name": "PatientPopulationPercentageBelowPoverty", "type": "number"},
        ],
        "primaryKey": ["PatientID"],
        "pandas_version": "1.4.0",
    }

    fields = mapped["fields"]
    cols = list(map(lambda x: x["name"], fields))
    # types = map(lambda x: {x["name"]: convertToPandasTypes(x["type"])}, fields)
    types = {f["name"]: convertToPandasTypes(f["type"]) for f in fields}
    print(*types)

    dfTest = pd.read_csv(
        "file-storage/PatientCorePopulatedTable.txt",
        sep=",|;|\t",
        engine="python",
        index_col=0,
        dtype=types,
        usecols=cols,
    )
    print(dfTest.dtypes)

    # print(fields)
    # print(cols)
    # df2 = pd.read_csv(
    #     "file-storage/LabsCorePopulatedTable.txt",
    #     sep=",|;|\t",
    #     engine="python",
    #     index_col=0,
    # )

    df_admisionDiagnoses = pd.read_csv(
        "file-storage/AdmissionsDiagnosesCorePopulatedTable.txt",
        sep="\t",
        engine="python",
        index_col=0,
    )
    print("JOIN")
    print(dfTest.join(df_admisionDiagnoses, on="PatientID", how="inner"))
    # print(df2.dtypes)
    # print(df_admisionDiagnoses.dtypes)
    # print(df_admisionDiagnoses.join(df2, on=["AdmissionID", "AdmissionID"]).head())

    # print(pd.merge(df_admisionDiagnoses, df2, on="AdmissionID"))
    # print(df2.join(df_admisionDiagnoses, how="inner", lsuffix="left"))

    # join = df.join(df2)
    # print(build_table_schema(join))
    # print(join.index)

    # js = df.reset_index().to_json(orient="records", indent=4)

    # print(js)

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
