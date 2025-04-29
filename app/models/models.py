from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
import datetime

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)
DOTENV_PATH = os.environ.get("DOTENV_PATH", os.path.join(PROJECT_ROOT, ".env"))


class VectorDBRequest(BaseModel):
    index_name: str = "test_index"
    template_path: str = "app/template/vectorDB_template.json"


class _ElasticConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ELASTIC_",
        env_file=DOTENV_PATH,
        extra="ignore",
        env_ignore_empty=True,
    )
    host: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    source: Optional[List[str]] = None
    ca_path: Optional[str] = None


class _ESIndexConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ES_",
        env_file=DOTENV_PATH,
        extra="ignore",
        env_ignore_empty=True,
    )
    my_data_index: Optional[str] = None


class ElasticApp(BaseSettings):
    es_config: _ElasticConfig = _ElasticConfig()
    es_index: _ESIndexConfig = _ESIndexConfig()


class ElasticSeachRequest(BaseModel):
    search_term: str
    search_field: str
    search_index: str


class ElasticSearchResponse(BaseModel):
    docs: List[str]


es_settings = ElasticApp()
