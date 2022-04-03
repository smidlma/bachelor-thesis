# Data structure

Sample data sturntures used in BE with mongoDB to hold pipeline data.

## Pipeline document

- Multiple sources in one pipeline
- Two types of transformations:
  - Local - used for source table only as rows operations etc.
  - Joins - used for joining the sources

Exmaple pipeline

```json
[
  {
    "_id": {
      "$oid": "62496961fdf22df762c83d5c"
    },
    "name": "Hospital",
    "sources": [
      {
        "_cls": "CSV",
        "id": {
          "$oid": "62496961fdf22df762c83d5a"
        },
        "name": "Pacients",
        "transformations": [
          {
            "_cls": "DateFilter",
            "id": {
              "$oid": "62496a3f9084d788d2571e6c"
            },
            "name": "DateFilter",
            "position": -1,
            "column": "PatientDateOfBirth",
            "op": "lt",
            "datetimes": [-623250772000]
          },
          {
            "_cls": "Sort",
            "id": {
              "$oid": "62496a649084d788d2571e6d"
            },
            "name": "Sort",
            "position": 0,
            "column": "PatientDateOfBirth",
            "ascending": true
          }
        ],
        "mappedSchema": {
          "fields": [
            {
              "name": "PatientID",
              "type": "string"
            },
            {
              "name": "PatientGender",
              "type": "string"
            },
            {
              "name": "PatientDateOfBirth",
              "type": "datetime"
            },
            {
              "name": "PatientRace",
              "type": "string"
            },
            {
              "name": "PatientMaritalStatus",
              "type": "string"
            },
            {
              "name": "PatientLanguage",
              "type": "string"
            },
            {
              "name": "PatientPopulationPercentageBelowPoverty",
              "type": "number"
            }
          ],
          "primaryKey": ["PatientID"]
        },
        "defaultSchema": {
          "fields": [
            {
              "name": "PatientID",
              "type": "string"
            },
            {
              "name": "PatientGender",
              "type": "string"
            },
            {
              "name": "PatientDateOfBirth",
              "type": "string"
            },
            {
              "name": "PatientRace",
              "type": "string"
            },
            {
              "name": "PatientMaritalStatus",
              "type": "string"
            },
            {
              "name": "PatientLanguage",
              "type": "string"
            },
            {
              "name": "PatientPopulationPercentageBelowPoverty",
              "type": "number"
            }
          ],
          "primaryKey": ["PatientID"],
          "pandas_version": "1.4.0"
        },
        "fileName": "PatientCorePopulatedTable.txt",
        "filePath": "file-storage/PatientCorePopulatedTable.txt",
        "separator": "\t"
      },
      {
        "_cls": "CSV",
        "id": {
          "$oid": "62496961fdf22df762c83d5b"
        },
        "name": "Labs",
        "transformations": [
          {
            "_cls": "ValueFilter",
            "id": {
              "$oid": "62496a7e9084d788d2571e6e"
            },
            "name": "ValueFilter",
            "position": -1,
            "column": "LabValue",
            "op": "gt",
            "vals": [3, 0]
          }
        ],
        "mappedSchema": {
          "fields": [
            {
              "name": "PatientID",
              "type": "string"
            },
            {
              "name": "AdmissionID",
              "type": "integer"
            },
            {
              "name": "LabName",
              "type": "string"
            },
            {
              "name": "LabValue",
              "type": "number"
            },
            {
              "name": "LabUnits",
              "type": "string"
            },
            {
              "name": "LabDateTime",
              "type": "datetime"
            }
          ]
        },
        "defaultSchema": {
          "fields": [
            {
              "name": "PatientID",
              "type": "string"
            },
            {
              "name": "AdmissionID",
              "type": "integer"
            },
            {
              "name": "LabName",
              "type": "string"
            },
            {
              "name": "LabValue",
              "type": "number"
            },
            {
              "name": "LabUnits",
              "type": "string"
            },
            {
              "name": "LabDateTime",
              "type": "string"
            }
          ],
          "pandas_version": "1.4.0"
        },
        "fileName": "LabsCorePopulatedTable.txt",
        "filePath": "file-storage/LabsCorePopulatedTable.txt",
        "separator": "\t"
      }
    ],
    "destination": {
      "_cls": "PostgreSQLDest",
      "id": {
        "$oid": "62496961fdf22df762c83d59"
      },
      "destinationName": "Warehouse",
      "targetTable": "hospital",
      "connection": {
        "$oid": "62496961fdf22df762c83d58"
      },
      "insertOption": "replace"
    },
    "joins": [
      {
        "_cls": "Join",
        "id": {
          "$oid": "624969999084d788d2571e6b"
        },
        "name": "Join(Pacients inner Labs)",
        "transformations": [],
        "mappedSchema": {
          "fields": [],
          "primaryKey": []
        },
        "defaultSchema": {
          "fields": [
            {
              "name": "PatientID",
              "type": "string"
            },
            {
              "name": "PatientGender",
              "type": "string"
            },
            {
              "name": "PatientDateOfBirth",
              "type": "string"
            },
            {
              "name": "PatientRace",
              "type": "string"
            },
            {
              "name": "PatientMaritalStatus",
              "type": "string"
            },
            {
              "name": "PatientLanguage",
              "type": "string"
            },
            {
              "name": "PatientPopulationPercentageBelowPoverty",
              "type": "number"
            },
            {
              "name": "AdmissionID",
              "type": "integer"
            },
            {
              "name": "LabName",
              "type": "string"
            },
            {
              "name": "LabValue",
              "type": "number"
            },
            {
              "name": "LabUnits",
              "type": "string"
            },
            {
              "name": "LabDateTime",
              "type": "string"
            }
          ],
          "primaryKey": ["PatientID"],
          "pandas_version": "1.4.0"
        },
        "s1": {
          "_cls": "CSV",
          "id": {
            "$oid": "62496961fdf22df762c83d5a"
          },
          "name": "Pacients",
          "transformations": [
            {
              "_cls": "DateFilter",
              "id": {
                "$oid": "62496a3f9084d788d2571e6c"
              },
              "name": "DateFilter",
              "position": -1,
              "column": "PatientDateOfBirth",
              "op": "lt",
              "datetimes": [-623250772000]
            },
            {
              "_cls": "Sort",
              "id": {
                "$oid": "62496a649084d788d2571e6d"
              },
              "name": "Sort",
              "position": 0,
              "column": "PatientDateOfBirth",
              "ascending": true
            }
          ],
          "mappedSchema": {
            "fields": [
              {
                "name": "PatientID",
                "type": "string"
              },
              {
                "name": "PatientGender",
                "type": "string"
              },
              {
                "name": "PatientDateOfBirth",
                "type": "datetime"
              },
              {
                "name": "PatientRace",
                "type": "string"
              },
              {
                "name": "PatientMaritalStatus",
                "type": "string"
              },
              {
                "name": "PatientLanguage",
                "type": "string"
              },
              {
                "name": "PatientPopulationPercentageBelowPoverty",
                "type": "number"
              }
            ],
            "primaryKey": ["PatientID"]
          },
          "defaultSchema": {
            "fields": [
              {
                "name": "PatientID",
                "type": "string"
              },
              {
                "name": "PatientGender",
                "type": "string"
              },
              {
                "name": "PatientDateOfBirth",
                "type": "string"
              },
              {
                "name": "PatientRace",
                "type": "string"
              },
              {
                "name": "PatientMaritalStatus",
                "type": "string"
              },
              {
                "name": "PatientLanguage",
                "type": "string"
              },
              {
                "name": "PatientPopulationPercentageBelowPoverty",
                "type": "number"
              }
            ],
            "primaryKey": ["PatientID"],
            "pandas_version": "1.4.0"
          },
          "fileName": "PatientCorePopulatedTable.txt",
          "filePath": "file-storage/PatientCorePopulatedTable.txt",
          "separator": "\t"
        },
        "s2": {
          "_cls": "CSV",
          "id": {
            "$oid": "62496961fdf22df762c83d5b"
          },
          "name": "Labs",
          "transformations": [
            {
              "_cls": "ValueFilter",
              "id": {
                "$oid": "62496a7e9084d788d2571e6e"
              },
              "name": "ValueFilter",
              "position": -1,
              "column": "LabValue",
              "op": "gt",
              "vals": [3, 0]
            }
          ],
          "mappedSchema": {
            "fields": [
              {
                "name": "PatientID",
                "type": "string"
              },
              {
                "name": "AdmissionID",
                "type": "integer"
              },
              {
                "name": "LabName",
                "type": "string"
              },
              {
                "name": "LabValue",
                "type": "number"
              },
              {
                "name": "LabUnits",
                "type": "string"
              },
              {
                "name": "LabDateTime",
                "type": "datetime"
              }
            ]
          },
          "defaultSchema": {
            "fields": [
              {
                "name": "PatientID",
                "type": "string"
              },
              {
                "name": "AdmissionID",
                "type": "integer"
              },
              {
                "name": "LabName",
                "type": "string"
              },
              {
                "name": "LabValue",
                "type": "number"
              },
              {
                "name": "LabUnits",
                "type": "string"
              },
              {
                "name": "LabDateTime",
                "type": "string"
              }
            ],
            "pandas_version": "1.4.0"
          },
          "fileName": "LabsCorePopulatedTable.txt",
          "filePath": "file-storage/LabsCorePopulatedTable.txt",
          "separator": "\t"
        },
        "how": "inner",
        "lsuffix": "_left",
        "rsuffix": "_right"
      }
    ]
  }
]
```

## WS communication

- Building pipeline workflow will be managed via ws and updated throw state

```json
{
  "from": "BE",
  "to": "FE",
  "cmd": "PIPELINE | ... | ...",
  "data": {...}
}
```
