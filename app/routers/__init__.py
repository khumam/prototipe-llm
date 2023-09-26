from fastapi import APIRouter
from .query import route as query_route

routers = APIRouter()

routers.include_router(query_route, prefix="/query", tags=["query"])

