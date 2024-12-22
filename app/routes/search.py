import datetime
from fastapi import APIRouter, status, HTTPException
import app.services.search_services as searchServices
from app.models.es_settings import ESHelpers

search = APIRouter(prefix="/search", tags=["Search"])

@search.get("/wildcard")
async def wildcard_search(request):
    async with ESHelpers(async_mode=True) as es:
        resp = await.query_search()

    # resp = await  

@search.get("/term")
async def term_search(request):
    pass


@search.get("vector_search")
async def vector_search(request):
    pass