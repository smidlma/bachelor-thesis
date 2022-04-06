# Bachelor thesis

- Author: Martin Šmídl
- Supervisor: Ing. Vojtěch Kotík

## ETL Tool for Processing Medical Data

Etl tool to process csv files and other formats of data with ability to connect external source or destination. Demo is used to process randomly generated EHR records in txt files. Apply basic transformations and load them to data warehouse.

## Requirements

- Node>=16.14.2LTS
- Python3
- MongoDB>=3.6
- PostgresSQL - optional or use any postgresql connection

## Run project

Instalation steps for backend and frontend

```bash
git clone git@github.com:smidlma/bachelor-thesis.git
```

### Backend Folder

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

> Run server (mongo server has to be runnign on localhost!)

```bash
uvicorn etl.main:app
```

### Frontend Folder

```bash
npm install
```

> Run dev server

```bash
npm run dev
```
