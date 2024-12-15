from elasticsearch import (
    AsyncElasticsearch,
    Elasticsearch,
    NotFoundError,
    ConflictError,
)
from app.models.models import es_settings


class ESHelpers:
    def __init__(self, async_mode: bool = False):
        self.es_client = None
        self.async_mode = async_mode

    async def __aenter__(self):
        if self.async_mode:
            self.es_client = await self._connect_async()
        else:
            self.es_client = self._connect()
        return self

    def _connect(self):
        config = es_settings.es_config
        es_client = Elasticsearch(
            [config.host],
            api_key=config.api_key,
            verify_certs=True,
            ca_certs=config.ca_path,
            ssl_show_warn=False,
        )
        return es_client

    async def _connect_async(self):
        config = es_settings.es_config
        if config.api_key == None:
            es_client = AsyncElasticsearch(
                [config.host],
                basic_auth=(config.user, config.password),
                ssl_show_warn=False,
            )
        else:
            es_client = AsyncElasticsearch(
                [config.host],
                api_key=config.api_key,
                verify_certs=False,
                ssl_show_warn=False,
            )
        return es_client

    async def query_search(self, query_, search_index, size=10):
        try:
            resp = await self.es_client.search(
                index=search_index, body=query_, size=size
            )
        except NotFoundError:
            return None
        return [doc for doc in resp["hits"]["hits"]]

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.es_client:  # Safeguard in case __aenter__ failed
            if self.async_mode:
                await self.es_client.close()
            else:
                self.es_client.close()
