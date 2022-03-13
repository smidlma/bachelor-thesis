# Data structure

Sample data sturntures used in BE with mongoDB to hold pipeline data.

## Pipeline document

- Multiple sources in one pipeline
- Two types of transformations:
  - Local - used for source table only as rows operations etc.
  - Global - used for joiining the sources, etc.

```json
{
  "name": "Pipeline",
  "sources": [
    {
      "name": "Sample Source CSV",
      "type": "CSV",
      "filePath": "/file.csv",
      "defaultSchema": {},
      "transformations": [{}]
    },
    {
      "name": "Sample Source POSTGRES",
      "type": " POSTGRESQL",
      "connection": {
        "host": "address",
        "port": 5522,
        "user": "User",
        "password": "password"
      },
      "defaultSchema": {},
      "transformations": [{}]
    }
  ],
  "joiner": [],
  "destination": {
    "name": "Sample Destination",
    "targetTable": "Table",
    "connection": {}
  }
}
```

## WS communication
* Building pipeline workflow will be managed via ws and updated throw state
```json
{
  "from": "FE",
  "to": "BE",
  "cmd": "GET_STATE",
  "payload": {}
}
```
