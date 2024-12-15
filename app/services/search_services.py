from app.models.es_helpers import ESHelpers
from app.models.models import es_settings


async def elastic_wildcard_search(search_term: str):
    query_ = {"query": {"wildcard": {"field": {"value": "*" + search_term + "*"}}}}
    async with ESHelpers(async_mode=True) as es:
        resp = es.query_search(
            query_=query_,
            search_index=es_settings.es_index.my_data_index,
        )
