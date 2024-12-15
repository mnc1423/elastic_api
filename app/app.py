from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from app.services.es_conn import ESHelpers
import datetime

app = FastAPI()

app.include_router(userinfo.users)

def build_search_args(json_data):
    search_args = {
        "es_index": json_data["index"],
        "field": json_data["field"],
        "vector": json_data["vector"],
    }

    if "size" in json_data:
        search_args["size"] = json_data["size"]

    return search_args


@app.post("/wildcard")
async def wildcard(request: Request):
    es_helper = ESHelpers()
    json_data = await request.json()
    search_args = build_search_args(json_data)
    docs = es_helper.wildcard_search(**search_args)
    return docs


@app.post("/term_search")
async def term_search(request: Request):
    es_helper = ESHelpers()
    json_data = await request.json()
    search_args = build_search_args(json_data)
    docs = es_helper.wildcard_search(**search_args)
    return docs


@app.post("/vector_search")
async def vector_search(request: Request):
    es_helper = ESHelpers()
    json_data = await request.json()
    search_args = build_search_args(json_data)
    docs = es_helper.knn_search(**search_args)
    return docs


@app.post("/insert_one")
async def insert_one(request: Request):
    es_helper = ESHelpers()
    json_data = await request.json()
    _id = json_data.pop("_id")
    es_index = json_data.pop("_index")
    json_data["date"] = datetime.datetime.now()
    resp = await es_helper.insert_one(es_index=es_index, data=json_data, _id=_id)
    return resp
