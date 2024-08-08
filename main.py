import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI
import datetime, os

PG_USER = os.environ.get("POSTGRES_USER")
PG_PASS = os.environ.get("POSTGRES_PASSWORD")
dbconn_string = f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@mdcatalogdb/postgres"
# engine = create_engine(dbconn_string)
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        now = datetime.datetime.now()
        resp = f"ok - {now}"

        return resp


schema = strawberry.Schema(Query)  # new
graphql_app = GraphQLRouter(schema)  # new
api = FastAPI(title="USFS Metadata Catalog API")
api.include_router(graphql_app, prefix="/graphql")  # new


@api.get("/health")
def health():
    now = datetime.datetime.now()
    resp = {"http_status": "ok", "data": now}

    return resp
