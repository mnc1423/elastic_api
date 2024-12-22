import datetime
from fastapi import APIRouter, status, HTTPException
import app.services.search_services as searchServices
from app.models.es_settings import ESHelpers

search = APIRouter(prefix="/search", tags=["Search"])

@search.get("/wildcard")
async def wildcard_search(request):
    async with ESHelpers(async_mode=True) as es:
        query_ = {
            "query":{
                "wildcard":{
                    request['field']:{
                        "value": "*" + request['search_term'] + "*"
                    }
                }
            }
        }
        resp = await es.query_search(query_=query_, search_index=request['_index'])
        return resp


@search.get("/term")
async def term_search(request):
    async with ESHelpers(async_mode=True) as es:
        query_ = {
            "query":{
                "term":{
                    request['field']:{
                        "value": request['search_term']
                    }
                }
            }
        }
        resp = await es.query_search(query_=query_, search_index=request['_index'])
        return resp


@search.get("vector_search")
async def vector_search(request):
    pass