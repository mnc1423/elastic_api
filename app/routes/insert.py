from fastapi import APIRouter, status, HTTPException
import json
from app.models.es_helpers import ESHelpers
from app.models.models import VectorDBRequest


insert = APIRouter(prefix="/insert", tags=["Insert"])


@insert.post(
    "/vectordb_template",
    status_code=status.HTTP_200_OK,
)
async def insert_vectordb_template(request: VectorDBRequest):
    async with ESHelpers(async_mode=True) as es:
        index_name = request.index_name
        # Load JSON file
        with open(request.template_path, "r") as f:
            index_body = json.load(f)
        # Create the index
        if not await es.indices.exists(index=index_name):
            await es.indices.create(index=index_name, body=index_body)
            return f"Index '{index_name}' created from JSON file!"
        else:
            return f"Index '{index_name}' already exists."


@insert.get(
    "/get_collections",
    status_code=status.HTTP_200_OK,
)
async def get_index_List():
    async with ESHelpers(async_mode=True) as es:
        indices = await es.cat.indices(format="json")

        index_name = [
            {"name": i["index"]} for i in indices if not i["index"].startswith(".")
        ]
    for idx in index_name:
        mapping = await es.indices.get_mapping(index=idx["name"])
        props = mapping[idx["name"]]["mappings"].get("properties", {})
        idx["mapping"] = {k: v.get("type", "object") for k, v in props.items()}
    return index_name


@insert.post(
    "/data/list",
    status_code=status.HTTP_200_OK,
)
async def insert_data_list(data: list):
    """
    Input format:
    {
        "id": id,
        "index": Elastic Index,
        "doc": document data
    }
    """
    async with ESHelpers(async_mode=True) as es:
        bulk_payload = []

        for item in data:
            action = {
                "_op_type": "create",
                "_index": item["index"],
                "_source": item["doc"],
            }

            if item["id"]:
                action["index"]["_id"] = item["id"]

            bulk_payload.append(action)

        response = await es.bulk(body=bulk_payload)

        errors = [
            item for item in response.get("items", []) if "error" in item["index"]
        ]

        return {"inserted": len(data), "errors": errors if errors else None}


@insert.post(
    "/data",
    status_code=status.HTTP_200_OK,
)
async def insert_data_list(data: dict):
    """
    Input format:
    {
        "id": id,
        "index": Elastic Index,
        "doc": document data
    }
    """
    async with ESHelpers(async_mode=True) as es:

        action = {
            "_op_type": "create",
            "_index": data["index"],
            "_source": data["doc"],
        }

        if data["id"]:
            action["index"]["_id"] = data["id"]

        response = await es.insert(body=action["doc"], id=action["_id"])

        errors = [
            item for item in response.get("items", []) if "error" in item["index"]
        ]

        return {"inserted": len(data), "errors": errors if errors else None}
