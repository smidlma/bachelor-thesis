# Data structure
Sample data sturntures used in BE with mongoDB to hold pipeline data.
## Pipelines document
* Multiple sources in one pipeline
* Two types of transformations:
    * Local - used for source table only as rows operations etc.
    * Global - used for joiining the sources, etc.    
```json
{
    "name": "Pipeline",
    "sources": [
        {
            "name": "Sample Source CSV",
            "type": "CSV",
            "filePath": "/file.csv",
            "schema": {},
            "transformations": [
                {}
            ]
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
            "schema": {},
            "transformations": [
                {}
            ]
        }
    ],
    "transformations": [
        {}
    ],
    "destination": {
        "name": "Sample Destination",
        "targetTable": "Table",
        "connection": {}
    }
}
```