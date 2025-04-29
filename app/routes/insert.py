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
