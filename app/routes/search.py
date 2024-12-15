import datetime
from fastapi import APIRouter, status, HTTPException
import app.services.search_services as searchServices

search = APIRouter(prefix="/search", tags=["Search"])

@search.get("/wildcard")
async def wildcard_search(request):
    pass

@search.get("/term")
async def term_search(request):
    pass


@search.get("vector_search")
async def vector_search(request):
    pass