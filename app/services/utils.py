import httpx


class _Request:

    async def get(self, endpoint: str, params: dict = None):
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data: dict = None, json: dict = None):
        response = await self.client.post(endpoint, data=data, json=json)
        response.raise_for_status()
        return response.json()

    async def put(self, endpoint: str, json: dict = None):
        response = await self.client.put(endpoint, json=json)
        response.raise_for_status()
        return response.json()

    async def delete(self, endpoint: str):
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
