## Run the server

``
uvicorn main:app --reload
``

A `.env` file is needed with the env variable with the following content:
```
DATABASE_URL=postgresql://**:**@**:5432/**
```
