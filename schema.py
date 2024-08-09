import strawberry
from pydantic import typing
# from fastapi import FastAPI
# from strawberry.fastapi import GraphQLRouter
# from sqlalchemy import select
from sqlalchemy.orm import Session

import datetime
from database import get_db, engine
import models

@strawberry.type
class Asset:
    id: int
    title: str
    description: str
    
@strawberry.type
class Query:
    
    @strawberry.field
    async def health(self) -> str:
        return f"ok - {datetime.datetime.now()}"
    
    @strawberry.field
    async def assets(self) -> typing.List[Asset]:
        assets_list = []

        with Session(engine) as session:
            rows = session.query(models.Asset).all()
            if rows:
                for row in rows:                    
                    asset = Asset(id=row.id, title=row.title, description=row.description)
                    assets_list.append(asset)

        return assets_list

schema = strawberry.Schema(Query)
