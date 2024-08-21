# mdcatalog  

## Resources  

Command to build docker image:
```
docker build --pull --rm -f "Dockerfile" -t mdcatalog:latest "." 
```

Command to run docker compose instance:
```
```

## Resources  
https://medium.com/@ryk.kiel/graphql-and-fastapi-the-ultimate-combination-for-building-apis-with-python-f4391bf5505c  

## Alembic Examples  
alembic revision -m "Add new table"  
alembic upgrade head  
alembic revision --autogenerate -m "Add asset keywords model"  

## Complete SQLAlchemy/Alembic Migrations Reset  
1. Empty ./alembic/versions folder.  
2. Empty ./alembic/versions/__pycache__ folder.  
3. Delete alembic_version in database.  
4. Delete object tables if needed.  
