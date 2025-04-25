import datetime
from fastapi import APIRouter, status, HTTPException

import app.services.search_services as searchServices
from app.models.es_helpers import ESHelpers
from app.models.models import ElasticSeachRequest, ElasticSearchResponse

search = APIRouter(prefix="/search", tags=["Search"])


@search.get(
    "/wildcard",
    response_model=ElasticSearchResponse,
    status_code=status.HTTP_200_OK,
)
async def wildcard_search(request: ElasticSeachRequest):

    resp = await searchServices.elastic_wildcard_search(
        search_term=request["search_term"],
        search_field=request["search_field"],
        search_index=request["search_index"],
    )
    if resp:
        return resp
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Failed to search "
        )


@search.get(
    "/term",
    response_model=ElasticSearchResponse,
    status_code=status.HTTP_200_OK,
)
async def term_search(request: ElasticSeachRequest):
    async with ESHelpers(async_mode=True) as es:
        query_ = {
            "query": {"term": {request["field"]: {"value": request["search_term"]}}}
        }
        resp = await es.query_search(query_=query_, search_index=request["_index"])
        return resp


@search.get(
    "/vector_search",
    response_model=ElasticSearchResponse,
    status_code=status.HTTP_200_OK,
)
async def vector_search(request: ElasticSeachRequest):
    pass
