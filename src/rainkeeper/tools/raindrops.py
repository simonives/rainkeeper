from fastmcp import FastMCP
from ..client import RaindropClient

_client = RaindropClient()


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    async def list_raindrops(collection_id: int = 0, page: int = 0, per_page: int = 25, sort: str | None = None) -> dict:
        """List bookmarks in a collection. collection_id 0 = All, -1 = Unsorted. sort: -created, title, -title, domain."""
        return await _client.list_raindrops(collection_id, page=page, per_page=per_page, sort=sort)

    @mcp.tool()
    async def get_raindrop(raindrop_id: int) -> dict:
        """Get a single bookmark by id."""
        return await _client.get_raindrop(raindrop_id)

    @mcp.tool()
    async def create_raindrop(link: str, collection_id: int = -1, title: str | None = None, tags: list[str] | None = None, important: bool = False, note: str | None = None) -> dict:
        """Save a new bookmark. collection_id -1 = Unsorted. Tags is a list of strings."""
        return await _client.create_raindrop(link, title=title, collection_id=collection_id, tags=tags, important=important, note=note)

    @mcp.tool()
    async def update_raindrop(raindrop_id: int, title: str | None = None, collection_id: int | None = None, tags: list[str] | None = None, important: bool | None = None, note: str | None = None) -> dict:
        """Update a bookmark. Pass collection_id to move it — uses the correct nested API format."""
        return await _client.update_raindrop(raindrop_id, title=title, collection_id=collection_id, tags=tags, important=important, note=note)

    @mcp.tool()
    async def move_raindrop(raindrop_id: int, target_collection_id: int) -> dict:
        """Move a single bookmark to a different collection. Explicit tool for clarity."""
        return await _client.update_raindrop(raindrop_id, collection_id=target_collection_id)

    @mcp.tool()
    async def delete_raindrop(raindrop_id: int) -> dict:
        """Delete a bookmark permanently."""
        return await _client.delete_raindrop(raindrop_id)
