from fastapi import FastAPI, Depends
import datetime
from strawberry.fastapi import GraphQLRouter
from schema import schema

graphql_app = GraphQLRouter(schema)  
api = FastAPI(title="USFS Metadata Catalog API")

@api.get("/health")
def health():
    now = datetime.datetime.now()
    resp = {"http_status": "ok", "data": now}

    return resp

api.include_router(graphql_app, prefix="/graphql")