"""Thin async HTTP wrapper around the Raindrop.io REST API v1."""
import httpx
from .config import BASE_URL, AUTH_HEADER


class RaindropClient:
    def __init__(self):
        self._client = httpx.AsyncClient(base_url=BASE_URL, headers=AUTH_HEADER)

    async def get(self, path: str, **params) -> dict:
        r = await self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        r.raise_for_status()
        return r.json()

    async def post(self, path: str, body: dict) -> dict:
        r = await self._client.post(path, json=body)
        r.raise_for_status()
        return r.json()

    async def put(self, path: str, body: dict) -> dict:
        r = await self._client.put(path, json=body)
        r.raise_for_status()
        return r.json()

    async def delete(self, path: str, body: dict | None = None) -> dict:
        r = await self._client.request("DELETE", path, json=body)
        r.raise_for_status()
        return r.json()

    # --- Collections ---

    async def list_collections(self) -> list[dict]:
        root = await self.get("/collections")
        children = await self.get("/collections/childrens")
        return root.get("items", []) + children.get("items", [])

    async def get_collection(self, collection_id: int) -> dict:
        data = await self.get(f"/collection/{collection_id}")
        return data.get("item", data)

    async def create_collection(self, title: str, parent_id: int | None = None, public: bool = False, color: str | None = None) -> dict:
        body: dict = {"title": title, "public": public}
        if parent_id is not None:
            body["parent"] = {"$id": parent_id}
        if color:
            body["color"] = color
        data = await self.post("/collection", body)
        return data.get("item", data)

    async def update_collection(self, collection_id: int, title: str | None = None, public: bool | None = None, color: str | None = None) -> dict:
        body: dict = {}
        if title is not None:
            body["title"] = title
        if public is not None:
            body["public"] = public
        if color is not None:
            body["color"] = color
        data = await self.put(f"/collection/{collection_id}", body)
        return data.get("item", data)

    async def delete_collection(self, collection_id: int) -> dict:
        return await self.delete(f"/collection/{collection_id}")

    # --- Raindrops ---

    async def list_raindrops(self, collection_id: int = 0, page: int = 0, per_page: int = 25, sort: str | None = None, search: str | None = None) -> dict:
        return await self.get(f"/raindrops/{collection_id}", page=page, perpage=per_page, sort=sort, search=search)

    async def get_raindrop(self, raindrop_id: int) -> dict:
        data = await self.get(f"/raindrop/{raindrop_id}")
        return data.get("item", data)

    async def create_raindrop(self, link: str, title: str | None = None, collection_id: int = -1, tags: list[str] | None = None, important: bool = False, note: str | None = None) -> dict:
        body: dict = {"link": link, "collection": {"$id": collection_id}, "important": important}
        if title:
            body["title"] = title
        if tags:
            body["tags"] = tags
        if note:
            body["note"] = note
        data = await self.post("/raindrop", body)
        return data.get("item", data)

    async def update_raindrop(self, raindrop_id: int, title: str | None = None, collection_id: int | None = None, tags: list[str] | None = None, important: bool | None = None, note: str | None = None) -> dict:
        body: dict = {}
        if title is not None:
            body["title"] = title
        if collection_id is not None:
            body["collection"] = {"$id": collection_id}  # critical: nested object, NOT flat collectionId
        if tags is not None:
            body["tags"] = tags
        if important is not None:
            body["important"] = important
        if note is not None:
            body["note"] = note
        data = await self.put(f"/raindrop/{raindrop_id}", body)
        return data.get("item", data)

    async def delete_raindrop(self, raindrop_id: int) -> dict:
        return await self.delete(f"/raindrop/{raindrop_id}")

    # --- Bulk ---

    async def bulk_move(self, source_collection_id: int, ids: list[int], target_collection_id: int) -> dict:
        return await self.put(f"/raindrops/{source_collection_id}", {"ids": ids, "collection": {"$id": target_collection_id}})

    async def bulk_tag(self, collection_id: int, ids: list[int], tags: list[str]) -> dict:
        return await self.put(f"/raindrops/{collection_id}", {"ids": ids, "tags": tags})

    async def bulk_mark_important(self, collection_id: int, ids: list[int], important: bool = True) -> dict:
        return await self.put(f"/raindrops/{collection_id}", {"ids": ids, "important": important})

    async def bulk_delete(self, collection_id: int, ids: list[int]) -> dict:
        return await self.delete(f"/raindrops/{collection_id}", {"ids": ids})

    # --- Search ---

    async def search(self, query: str, collection_id: int = 0, page: int = 0, per_page: int = 25) -> dict:
        return await self.get(f"/raindrops/{collection_id}", search=query, page=page, perpage=per_page)

    # --- Tags ---

    async def list_tags(self, collection_id: int | None = None) -> list[dict]:
        params = {"collectionId": collection_id} if collection_id is not None else {}
        data = await self.get("/tags", **params)
        return data.get("items", [])

    async def rename_tag(self, old_tag: str, new_tag: str) -> dict:
        return await self.put("/tags", {"replace": old_tag, "tags": [new_tag]})

    async def delete_tags(self, tags: list[str]) -> dict:
        return await self.delete("/tags", {"tags": tags})
