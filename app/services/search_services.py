from app.models.es_helpers import ESHelpers
from app.models.models import es_settings


async def elastic_wildcard_search(
    search_term: str, search_field: str, search_index: str
):

    async with ESHelpers(async_mode=True) as es:
        query_ = {
            "query": {"wildcard": {search_field: {"value": "*" + search_term + "*"}}}
        }
        resp = await es.query_search(query_=query_, search_index=search_index)
        return resp
